from django.shortcuts import render,HttpResponse
from farmer.models import Product ,Bid
from account.models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.db.models import Q
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
            farmer = crop.farmer
            bid = Bid(customer = userProfile,farmer=farmer,crop=crop,status="Pending",bid_price = request.POST["bidamount"])
            bid.save()
            
            return redirect(f"/customer/crop/{pk}")
        else:
        
            return HttpResponse("Usertype is not valid")
    else:
        return HttpResponse("failed")
    
    
    
def crop_detail(request,pk):
    crop = Product.objects.get(pk = pk)
    bids = Bid.objects.filter(crop = crop)
    user = UserProfile.objects.get(user = request.user)
    user_bid = Bid.objects.filter(Q(customer = user) & Q(crop = crop))
    print("user bid",user_bid)
    print(crop,bids)
    context = {'crop':crop,'bids':bids,"bidAdded":len(user_bid),"user_bid":user_bid}
    return render(request,"cropDetail.html",context=context)

def updateBid(request,pk):
    if request.method == 'POST':
        try:
            amount = request.POST['bidamount']
            bid = Bid.objects.get(pk = pk)
            bid.bid_price = amount
            bid.save()
            return redirect(f"/customer/crop/{bid.crop.id}")
        except Exception as e:
            return HttpResponse("something went wrong")
    else:
        return HttpResponse("Not a valid request")