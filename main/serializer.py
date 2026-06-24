from rest_framework import serializers
from  .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id' , 'username' , 'password' , 'first_name' , 'last_name' , 'image')

        extra_kwargs = {
            'password' : {'write_only' : True}
        }

    def create(self , validated_data):
        return User.objects.create_user(**validated_data)





class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id' , 'name' , 'details' , 'price' , 'cover' , 'created_at' , 'user' , 'sold' , 'image')



class BookPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id' , 'name' , 'details' , 'price' , 'cover' , 'created_at' , 'user' , 'sold' , 'image')

        extra_kwargs = {
            'user' : {
                'read_only' : True
            }
        }




class BookMarkSoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id' , 'sold')

        extra_kwargs = {
            'sold' :
                {'read_only' : True}
        }



































