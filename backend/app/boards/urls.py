from app.boards.views import BoardViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("", BoardViewSet)

urlpatterns = router.urls
