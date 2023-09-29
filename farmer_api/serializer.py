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
    




