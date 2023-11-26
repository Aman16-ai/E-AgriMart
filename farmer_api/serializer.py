from rest_framework import serializers
from account.models import CropDetail, UserProfile
from farmer.models import Product
from account_api.serializer import FarmerDetailsSerializer,RegisterationSerializer

class CropsModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = CropDetail


class ProductModelSerializer(serializers.ModelSerializer):
    farmer = RegisterationSerializer(read_only=True)

    # we can directly add this into our fields of meta Class or we can conditionally render using to_representation method.
    def get_averageBidPrice(self,obj):
        # return f"Avrage bid of crop f{obj.id}"
        return obj.get_averageBidPrice()
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if(self.context['request'].method == 'GET'):
            rep['averageBidPrice'] = self.get_averageBidPrice(instance)
            rep['total_bids'] = instance.get_totalBids()
        return rep
    
    class Meta:
        fields = "__all__"
        model = Product

class ProductCreateModelSerializer(serializers.ModelSerializer):

    # Here farmer is already created we don't want to create it again so we didn't use nested seralizer. Instead of that we use PrimaryKeyRelatedField so that we can pass the id of farmer and this field we serialize that id into corresponding farmer object
    # farmer = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    class Meta:
        exclude=("farmer",)
        model=Product

    def create(self, validated_data):
        user = self.context['request'].user
        farmer_profile = UserProfile.objects.get(user=user)
        product =  Product(**validated_data,farmer=farmer_profile)
        product.save()
        return product
    




