from rest_framework.routers import SimpleRouter
from .views import CropsViewSet
simpleRouter = SimpleRouter()
simpleRouter.register('crop',CropsViewSet)