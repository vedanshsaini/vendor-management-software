# vendor_app/views.py

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceView(APIView):
    def get(self, request, vendor_id):
        vendor = generics.get_object_or_404(Vendor, pk=vendor_id)
        serializer = VendorSerializer(vendor)
        return Response({
            'on_time_delivery_rate': serializer.data['on_time_delivery_rate'],
            'quality_rating_avg': serializer.data['quality_rating_avg'],
            'average_response_time': serializer.data['average_response_time'],
            'fulfillment_rate': serializer.data['fulfillment_rate'],
        })
