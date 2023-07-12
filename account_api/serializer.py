from rest_framework import serializers
from account.models import User,UserProfile,Address
from django.contrib.auth.models import Group
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name","last_name","username","email","password")

    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        userobj =  User.objects.create_user(**validated_data)
        userobj.first_name = first_name
        userobj.last_name = last_name
        userobj.save()
        return userobj



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

    def create(self, validated_data):
        addressobj = Address(**validated_data)
        addressobj.save()
        return addressobj


class RegisterationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    address = AddressSerializer()

    class Meta:
        model = UserProfile
        fields = "__all__"


    def create(self, validated_data):
        user = validated_data.pop('user')
        address = validated_data.pop('address')
        user_instance = UserSerializer(data=user)
        address_instance = AddressSerializer(data=address)
        if user_instance.is_valid(raise_exception=True) and address_instance.is_valid(raise_exception=True):
            userObj = user_instance.create(validated_data=user)
            addressObj = address_instance.create(validated_data=address)
            userProfile_instance = UserProfile(user = userObj,address = addressObj,**validated_data)
            userProfile_instance.save()
            if validated_data.get('user_type') == 'Customer':
                group = Group.objects.get(name="Customer")
                userObj.groups.add(group)
                userObj.save()
            return userProfile_instance
        else:
            return None
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    