from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Trade, Transfer
from .serializers import TradeSerializer, TradeCreateSerializer, TransferSerializer

class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all().order_by("-created_at")

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TradeCreateSerializer
        return TradeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trade = serializer.save()
        read_serializer = TradeSerializer(trade)
        return Response({"success": True, "data": read_serializer.data}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"success": True, "data": serializer.data})

class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all().order_by("-date")
    serializer_class = TransferSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        summary = Transfer.get_summary()

        return Response({
            "success": True,
            "data": {
                "summary": {
                    "totalCapital": f"{summary['total_capital']:,}",
                    "totalDeposits": f"{summary['total_deposits']:,}",
                    "totalWithdrawals": f"{summary['total_withdrawals']:,}"
                },
                "transfers": serializer.data
            }
        }, status=status.HTTP_200_OK)
