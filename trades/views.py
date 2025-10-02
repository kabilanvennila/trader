from rest_framework import viewsets
from .models import Trade
from .serializers import TradeSerializer

class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all().order_by("-created_at")
    serializer_class = TradeSerializer