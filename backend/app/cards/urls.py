from app.cards.views import CardViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("", CardViewSet)

urlpatterns = router.urls
