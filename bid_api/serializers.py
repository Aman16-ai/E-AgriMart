from rest_framework import serializers
from farmer.models import Bid,Product
from account.models import UserProfile
from rest_framework.exceptions import ValidationError

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
        # Todo : add validation that crop belongs to the same farmer 
        if validated_data.get('farmer').user.id == validated_data.get('crop').farmer.user.id:

            userObj = self.context['request'].user
            customer = UserProfile.objects.get(user=userObj)
            bidObj = Bid(**validated_data,customer=customer,status="Pending")
            bidObj.save()
            return bidObj
        else:
            raise ValidationError(detail={'error':"Crop must be of same farmer"}) 
    
class GetBidModelSerializer(serializers.ModelSerializer):

    profit = serializers.ReadOnlyField()
    class Meta:
        fields = "__all__"
        model = Bid
        depth = True
