from django.shortcuts import redirect, render,HttpResponse
import pandas as pd
import pickle
from account.models import UserProfile

from farmer.models import Product,Bid
# Create your views here.
# import MachineLearning.predictor as ML
def index(request):
    return render(request,"farmerpanel.html")

def predictProduction(request):
    return render(request,"cropprediction.html")

def handlepredictedProduction(request):
    
    if request.method == 'POST':
        
        #statename,cropnum,seasonnum,cropname,tempnum,huminum,soil,areaname
        state = request.POST["statename"]
        crop_year = request.POST["cropnum"]
        season = request.POST["seasonnum"]
        crop = request.POST["cropname"]
        temp = request.POST["tempnum"]
        humi = request.POST["huminum"]
        soil = request.POST["soil"]
        area = request.POST["areaname"]
        
        print(state,crop_year,season,crop,temp,humi,soil,area)
        data = {"State_Name":[state],"Crop_Year":[crop_year],"Season":[season],"Crop":[crop],"Temperature":[temp],"humidity":[humi],"soil moisture":[soil]," area":[area]}
        
        # print(ML.predict_crop_production(data))
        with open("crop_model_pkl.pkl","rb") as files:
            mlmodel = pickle.load(files)
            result = mlmodel.predict(pd.DataFrame(data))
            print(result)
            context = {"result":result}
            return render(request,"predictionresult.html",context)
    return HttpResponse("handleing prediction")

def addProduct(request):
    if request.method == 'POST':
        crop_name = request.POST["crop_name"]
        img = request.FILES["img"]
        crop_quantity = request.POST['crop_qunatity']
        crop_price = request.POST["crop_price"]
        print(crop_name,img,crop_quantity,crop_price)
        
        farmer = UserProfile.objects.get(user = request.user)
        crop = Product(farmer = farmer,crop_name=crop_name,crop_img=img,quantity=crop_quantity,price =crop_price)
        crop.save()
        return redirect("/farmer/addProduct")
    return HttpResponse("adding ")

def fetchallbids(request):
    userProfile = UserProfile.objects.get(user = request.user)
    if userProfile.user_type == "Farmer":
        lst = []
        allbids = Bid.objects.all()
        for b in allbids:
            if b.crop.farmer.user.username == userProfile.user.username:
                lst.append(b)
        print(lst)
        return render(request,"farmersbids.html",{"bids":lst})
    else:
        return HttpResponse("Not a valid user")