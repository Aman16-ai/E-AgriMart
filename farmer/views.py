from django.shortcuts import redirect, render,HttpResponse
import pandas as pd
import pickle
from account.models import UserProfile

from farmer.models import Product,Bid
from django.db.models import Q
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
        
        #getting all bids of the farmer
        lst = []
        allbids = Bid.objects.all()
        for b in allbids:
            dic = {}
            if b.crop.farmer.user.username == userProfile.user.username:
                lst.append(b)
        print(lst)
        
        #getting the crop and its count of a bid
        dic = {}
        for l in lst: 
            if l.crop.crop_name in dic:
                dic[l.crop.crop_name]['count'] += 1
            else:
                dic[l.crop.crop_name] = {'crop':l.crop,'count':1}
            
        print(dic)
        
        return render(request,"farmersbids.html",{"bids":lst,"crops":dic})
    else:
        return HttpResponse("Not a valid user")
    

def cropDetail(request,pk):
    crop = Product.objects.get(pk = pk)
    farmer = UserProfile.objects.get(user = request.user)
    bids = []
    for b in Bid.objects.filter(crop = crop):
        if b.crop.farmer.user.username == farmer.user.username:
            bids.append(b)
    print(bids)
    return HttpResponse(f"crop detail  {pk}")