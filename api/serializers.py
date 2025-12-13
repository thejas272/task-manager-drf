from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import TaskModel



class RegisterSerializer(serializers.ModelSerializer):

  username = serializers.CharField()
  password = serializers.CharField(write_only=True)
  email    = serializers.EmailField()

  class Meta:
    model = User
    fields = ['username', 'password', 'email']

  def validate_username(self,value):
    if User.objects.filter(username=value).exists():
      raise serializers.ValidationError('Username already exists')
    return value
    
  def validate_email(self,value):
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError("Email already exists")
    return value

  def create(self, validated_data):
    user = User.objects.create_user(username=validated_data['username'],
                                    email=validated_data['email'],
                                    password=validated_data['password']
                                  )
    return user
    


class TaskSerializer(serializers.ModelSerializer):

  class Meta:
    model = TaskModel
    fields = ['id','title','description','status','owner','created_at','updated_at']
    read_only_fields = ['id','created_at','updated_at']



