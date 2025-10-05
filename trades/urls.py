from rest_framework.routers import DefaultRouter
from .views import TradeViewSet, TransferViewSet

router = DefaultRouter()
router.register(r"trades", TradeViewSet)
router.register(r"transfers", TransferViewSet, basename="transfers")

urlpatterns = router.urls