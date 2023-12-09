# vendor_app/models.py

from django.db import models
from django.db.models import Avg, Count
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    def calculate_on_time_delivery_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now())
        total_completed_pos = completed_pos.count()

        return (on_time_deliveries.count() / total_completed_pos) * 100 if total_completed_pos else 0

    def calculate_quality_rating_avg(self):
        completed_pos_with_rating = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
        return completed_pos_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

    def calculate_average_response_time(self):
        acknowledged_pos = self.purchaseorder_set.filter(acknowledgment_date__isnull=False)
        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in acknowledged_pos]
        total_response_times = len(response_times)

        return sum(response_times) / total_response_times if total_response_times else 0

    def calculate_fulfillment_rate(self):
        total_pos = self.purchaseorder_set.all()
        successfully_fulfilled_pos = total_pos.filter(status='completed')
        total_pos_count = total_pos.count()

        return (successfully_fulfilled_pos.count() / total_pos_count) * 100 if total_pos_count else 0
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    po_number = models.CharField(max_length=20, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO {self.po_number} - {self.vendor.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.vendor:
            self.vendor.on_time_delivery_rate = self.vendor.calculate_on_time_delivery_rate()
            self.vendor.quality_rating_avg = self.vendor.calculate_quality_rating_avg()
            self.vendor.average_response_time = self.vendor.calculate_average_response_time()
            self.vendor.fulfillment_rate = self.vendor.calculate_fulfillment_rate()
            self.vendor.save()

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"Performance Record - {self.vendor.name} - {self.date}"
    
@receiver(post_save, sender=PurchaseOrder)
@receiver(post_delete, sender=PurchaseOrder)
def update_metrics_on_purchase_order_change(sender, instance, **kwargs):
    if instance.vendor:
        instance.vendor.on_time_delivery_rate = instance.vendor.calculate_on_time_delivery_rate()
        instance.vendor.quality_rating_avg = instance.vendor.calculate_quality_rating_avg()
        instance.vendor.average_response_time = instance.vendor.calculate_average_response_time()
        instance.vendor.fulfillment_rate = instance.vendor.calculate_fulfillment_rate()
        instance.vendor.save()    
