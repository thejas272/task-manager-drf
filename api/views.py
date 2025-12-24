from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .serializers import RegisterSerializer,LoginSerializer, TaskSerializer, LogoutSerializer
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from api.models import TaskModel
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView


# Create your views here.


class TaskPagination(PageNumberPagination):
  page_size = 5
  page_size_query_param = "page_size"
  max_page_size = 50



class RegisterAPIView(GenericAPIView):

  permission_classes = [AllowAny]
  serializer_class = RegisterSerializer

  def post(self,request):
    serializer = self.serializer_class(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data,status=status.HTTP_201_CREATED)
  
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  

class LoginAPIView(GenericAPIView):

  permission_classes = [AllowAny]
  serializer_class = LoginSerializer

  def post(self,request):

    serializer = self.serializer_class(data=request.data)
    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = authenticate(username=username,password=password)

    if not user:  # user exists with given username and pw so authenticating 
      return Response({'detail':'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)

    return Response({'refresh':str(refresh),
                     'access':str(refresh.access_token)
                    },status=status.HTTP_200_OK
                   )



class LogoutAPIView(GenericAPIView):
  permission_classes = [AllowAny]
  serializer_class = LogoutSerializer

  def post(self,request):
    serializer = self.serializer_class(data=request.data)
    
    if serializer.is_valid():
      serializer.save()
      return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)




class RefreshTokenAPIView(GenericAPIView):
  
  permission_classes = [AllowAny]

  def post(self,request):
    refresh_token = request.data.get('refresh')

    try:
      refresh = RefreshToken(refresh_token)   # validaiton of refresh token 

      new_access = refresh.access_token      # creating a new access token from the refresh token

      return Response({'access':str(new_access)},status=status.HTTP_200_OK)

    except TokenError:
      return Response({'detail':'Invalid or expired refresh token'},status=status.HTTP_400_BAD_REQUEST)
    


class CreateTaskAPIView(GenericAPIView):

  permission_classes = [IsAuthenticated]
  serializer_class = TaskSerializer 

  def post(self,request):

    serializer = self.serializer_class(data=request.data, context={'request':request})

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ListTaskAPIView(GenericAPIView):

  permission_classes = [IsAuthenticated]
  pagination_class = TaskPagination
  serializer_class = TaskSerializer

  def get(self,request):

    if request.user.is_staff:
      # admin has logged in
      tasks = TaskModel.objects.filter().all()
    else:
      #user has logged in
      tasks = TaskModel.objects.filter(owner=request.user)

    if not tasks.exists():
      return Response({"message":"No tasks found",
                       "data":[]},
                       status=status.HTTP_200_OK
                     )
    
    task_status = request.query_params.get('status')
    if task_status is not None:
      if task_status.lower() == "true":
        tasks = tasks.filter(status=True)

      elif task_status.lower() == "false":
        tasks = tasks.filter(status=False)


    owner = request.query_params.get('owner')
    if owner is not None:
      if request.user.is_staff:
        tasks = tasks.filter(owner_id=owner)
      else:
        return Response({"message":"Request not allowed"}, status=status.HTTP_403_FORBIDDEN)
      

    due = request.query_params.get('due_date')
    if due is not None:
      date_field = serializers.DateField()
   
      due_date = date_field.to_internal_value(due)
      try:
        tasks = tasks.filter(due_date=due_date)
      except serializers.ValidationError:
        return Response({"due_date":"Invalid date format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
      

      
    paginator = self.pagination_class()
    page = paginator.paginate_queryset(tasks, request)

    if page is None:
      serializer = self.serializer_class(tasks, many=True)
      return Response(serializer.data)
      
    serializer = self.serializer_class(page, many=True)
    return paginator.get_paginated_response(serializer.data)
  


class RetrieveTaskAPIView(GenericAPIView):

  permission_classes = [IsAuthenticated]
  serializer_class = TaskSerializer

  def get(self,request,id):
    task = TaskModel.objects.filter(id=id).first()
    if not task:
      return Response({"message":"Task not found"},status=status.HTTP_404_NOT_FOUND)
    
    if not request.user.is_staff:
    
      if task.owner_id != request.user.id:
        return Response({"message":"Illegal access"},status=status.HTTP_403_FORBIDDEN)
      
    
    serializer = self.serializer_class(task)
    return Response(serializer.data,status=status.HTTP_200_OK)



class UpdateTaskAPIView(GenericAPIView):

  permission_classes = [IsAuthenticated]
  serializer_class = TaskSerializer

  def put(self,request,id):
    data = request.data.copy()
    task = TaskModel.objects.filter(id=id).first()

    if not task:
      return Response({"message":"Task not found"},status=status.HTTP_404_NOT_FOUND)
    

    if not request.user.is_staff:

      if task.owner_id != request.user.id:
        return Response({"message":"Illegal access"},status=status.HTTP_403_FORBIDDEN)
    

    serializer = self.serializer_class(task, data=data, partial=True, context={"request":request})
    if serializer.is_valid():
      serializer.save()
      return  Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 






class DeleteTaskAPIView(GenericAPIView):

  permission_classes = [IsAuthenticated]
  serializer_class = TaskSerializer

  def delete(self,request,id):
    task = TaskModel.objects.filter(id=id).first()

    if not task:
      return Response({"message":"Task not found"},status=status.HTTP_404_NOT_FOUND)
    
    if not request.user.is_staff:

      if task.owner_id != request.user.id:
        return Response({"message":"Illegal access"},status=status.HTTP_403_FORBIDDEN)
    
    
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
  

