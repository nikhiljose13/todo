from django.shortcuts import render
from api.serializers import Userserializers,Todoserializers
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import authentication,permissions
# Create your views here.
from reminder.models import Todos
from api.serializers import Todoserializers


class SignupView(APIView):

    def post(self,requset,*args,**kwargs):
        serializer=Userserializers(data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
class   TodosView(ViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def list(self,requset,*args,**kwargs):
        qs=Todos.objects.filter(user=requset.user)
        serializer=Todoserializers(qs,many=True)
        return Response(data=serializer.data)
    
    
    def create(self,requset,*args,**kwargs):
        
        serializer=Todoserializers(data=requset.data)
        if serializer.is_valid():
            serializer.save(user=requset.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    def retrieve(self,requset,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todos.objects.get(id=id)
        serializer=Todoserializers(qs)
        return Response(data=serializer.data)
     
    def destroy(self,requset,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todos.objects.get(id=id)
        if qs.user==requset.user:
             qs.delete()
        else:
             raise serializers.ValidationError("poda mone")

        return Response(data={"message":"deleted"})
    
    def update(self,request,*args,**kwargs):
            id=kwargs.get("pk")
            todo_object=Todos.objects.get(id=id)
            Serializers=Todoserializers(data=request.data,instance=todo_object)
            if Serializers.is_valid():
                  Serializers.save()
                  return Response(data=Serializers.data)
            else:
                  return  Response(data=Serializers.errors)