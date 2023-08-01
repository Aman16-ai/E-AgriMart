from rest_framework.routers import SimpleRouter
from .views import AccountViewset, FarmerAccountViewSet
accountRouter = SimpleRouter()
accountRouter.register("",AccountViewset)
accountRouter.register("farmer",FarmerAccountViewSet)