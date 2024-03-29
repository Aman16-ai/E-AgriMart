from django.shortcuts import redirect, render,HttpResponse
import pandas as pd
import pickle
from account.models import UserProfile

from farmer.models import Product,Bid
from django.db.models import Q
# Create your views here.
# import MachineLearning.predictor as ML
from MachineLearning.cropQuality.main import get_crop_quality
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
        main_img = request.FILES["img"]
        single_img = request.FILES['img2']
        crop_quantity = request.POST['crop_qunatity']
        crop_price = request.POST["crop_price"]
        print(crop_name,main_img,crop_quantity,crop_price)
        print(main_img,single_img)
        quality = get_crop_quality(main_img,single_img)
        print("crop quailty --------> ",quality)
        farmer = UserProfile.objects.get(user = request.user)
        crop = Product(farmer = farmer,crop_name=crop_name,crop_img=main_img,quantity=crop_quantity,price =crop_price)
        crop.quality = quality
        crop.save()
        return redirect("/farmer/addProduct")
    return HttpResponse("adding ")

def fetchallbids(request):
    userProfile = UserProfile.objects.get(user = request.user)
    if userProfile.user_type == "Farmer":
        
        #getting all bids of the farmer
        lst = []
        userProfile = UserProfile.objects.get(user=request.user)
        allbids = Bid.objects.filter(farmer=userProfile)
        # for b in allbids:
        #     dic = {}
        #     if b.crop.farmer.user.username == userProfile.user.username:
        #         lst.append(b)
        # print(lst)
        
        #getting the crop and its count of a bid
        dic = {}
        for l in allbids: 
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
    context = {'crop':crop,'bids':bids}
    return render(request,"fullcropDetail.html",context=context)