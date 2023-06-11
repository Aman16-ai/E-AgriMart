from rest_framework.routers import SimpleRouter
from .views import AccountViewset
accountRouter = SimpleRouter()
accountRouter.register("",AccountViewset)