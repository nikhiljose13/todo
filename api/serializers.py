from rest_framework import serializers
from django.contrib.auth.models import User

from reminder.models import Todos

class Userserializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","email","password"]
        read_only_fields=["id"]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class Todoserializers(serializers.ModelSerializer):
     class Meta:
        model=Todos
        fields="__all__"
        read_only_fields=["id","date","user"]