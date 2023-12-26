from rest_framework.routers import SimpleRouter
from .views import BidViewSet
bidRouter = SimpleRouter()
bidRouter.register("",BidViewSet)
