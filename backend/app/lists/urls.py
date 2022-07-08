from app.lists.views import ListViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("", ListViewSet)

urlpatterns = router.urls
