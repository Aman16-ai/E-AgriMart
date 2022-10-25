from django.shortcuts import render,HttpResponse
from farmer.models import Product ,Bid
from account.models import UserProfile
# Create your views here.
def index(request):
    allproduct = Product.objects.all().order_by("-price")
    print(allproduct)
    context = {"allproducts":allproduct}
    for p in allproduct:
        print(p.crop_name)
    return render(request,"customerpanel.html",context=context)


def addBid(request,pk):
    if request.method == "POST":
        userProfile = UserProfile.objects.get(user = request.user)
        if userProfile.user_type == "Customer":
            crop = Product.objects.get(pk = pk)
            bid = Bid(customer = userProfile,crop=crop,status="Pending",bid_price = request.POST["bidamount"])
            bid.save()
            
            return HttpResponse("bid successfully added")
        else:
        
            return HttpResponse("Usertype is not valid")
    else:
        return HttpResponse("failed")