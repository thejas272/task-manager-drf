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
    fields = ['id','title','description','status','owner','due_date','created_at','updated_at']
    read_only_fields = ['id','owner','created_at','updated_at']


  def _get_owner(self):  # helper method to configure owner of a task 
    request = self.context['request']

    if request.user.is_staff:
      owner_id = self.initial_data.get('owner')
      if owner_id:
        try:
          return User.objects.filter(id=owner_id)
        except User.DoesNotExist:
          raise serializers.ValidationError({"owner":"User with this ID does not exist"})
      else:
        return request.user
    else:
      return request.user



  def validate(self, attrs):
    title  = attrs.get("title")
    owner = self._get_owner()

    task_query_set = TaskModel.objects.filter(title=title,owner=owner)   # checking for duplication attempt of a task

    if self.instance:   # in case of updation
      task_query_set = task_query_set.exclude(id=self.instance.id)
    
    if task_query_set.exists():
      raise serializers.ValidationError({"title":"A task with the same title already exists"})

    return attrs



  def create(self, validated_data):
    request = self.context['request']

    validated_data['owner'] = self._get_owner()
    return super().create(validated_data)


  def update(self,instance,validated_data):
    request = self.context['request']

    if not request:
      raise serializers.ValidationError("Request context is required")
    
    if request.user.is_staff and 'owner' in self.initial_data:
      validated_data['owner'] = self._get_owner()

    for attr,value in validated_data.items():
      setattr(instance, attr, value)
    
    instance.save()
    return instance

