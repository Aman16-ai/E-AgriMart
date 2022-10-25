from django.shortcuts import redirect, render,HttpResponse
from account.models import Address,UserProfile
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request,"register.html")

def handleRegister(request):
    if request.method == 'POST':
        firstname = request.POST["fname"]
        lastname = request.POST["lname"]
        email = request.POST["email"]
        username = request.POST["uname"]
        password = request.POST["password"]
        contact_num = request.POST["cnum"]
        usertype = request.POST["usertype"]
        
        pincode = request.POST["pinname"]
        cityname = request.POST["cityname"]
        statename = request.POST["statename"]
        landmark = request.POST["landname"]
        
        address = Address(pincode = pincode,city=cityname,state=statename,landmark=landmark)
        if address is not None:
            address.save()
            user = User.objects.create_user(username = username,email=email,password = password)
            user.first_name = firstname
            user.last_name = lastname
            if user is not None:
                userProfile = UserProfile(user = user,user_type = usertype,address = address,contact_no = contact_num)
                userProfile.save()
                user.save()
                
                # if usertype == "Farmer":
                #     return redirect("/farmer/page")
                # elif usertype == "Customer":
                #     return redirect("/customer/page")
                return redirect("/")
        
    return HttpResponse("failed to register")
        
        #firstname,lname,email,uname,gender,usertype
        #pinname,cityname,statename,landname
        
def loginpage(request):
    return render(request,"login.html")

def handleLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST["password"]
        
        user = authenticate(request,username=username,password = password)
        print(user)
        if user is not None:
            login(request,user)
            userProfile = UserProfile.objects.get(user = user)
            print(userProfile)
            if userProfile.user_type == "Farmer":
                return redirect("/farmer/page")
            elif userProfile.user_type == "Customer":
                return redirect("/customer/page")
            else:
                return redirect("/")
    return HttpResponse("failed")


def logoutuser(request):
    logout(request)
    return redirect("/")