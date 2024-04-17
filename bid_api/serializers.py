from rest_framework import serializers
from farmer.models import Bid,Product
from account.models import UserProfile
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from account_api.serializer import UserDetailsSerializer
class BidModelSerializer(serializers.ModelSerializer):

    farmer = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    crop = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['profit'] = instance.profit
        return data
    class Meta:
        exclude = ('status','customer',)
        model = Bid
        depth = True

    def create(self, validated_data):
       
        userObj = self.context['request'].user
        customer = UserProfile.objects.get(user=userObj)
        # if(Bid.objects.filter(Q(customer=customer) & Q(crop = validated_data.get('crop'))).exists()):
        #     raise ValidationError(detail={"error":"Bid already exists"})
        if validated_data.get('farmer').user.id == validated_data.get('crop').farmer.user.id:

            # userObj = self.context['request'].user
            # customer = UserProfile.objects.get(user=userObj)
            bidObj = Bid(**validated_data,customer=customer,status="Pending")
            bidObj.save()
            return bidObj
        else:
            raise ValidationError(detail={'error':"Crop must be of same farmer"}) 
    
class GetBidModelSerializer(serializers.ModelSerializer):
    farmer = UserDetailsSerializer()
    customer = UserDetailsSerializer()
    profit = serializers.ReadOnlyField()
    class Meta:
        fields = "__all__"
        model = Bid
        depth = True

# class UpdateBidModelSerializer(serializers.ModelSerializer):

#     class Meta:
#         fields