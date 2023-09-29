from rest_framework.routers import SimpleRouter
from .views import CropsViewSet,ProductViewSet
simpleRouter = SimpleRouter()
simpleRouter.register('crop',CropsViewSet)
simpleRouter.register('product',ProductViewSet)