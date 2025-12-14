from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,TaskSerializer
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from api.models import TaskModel
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination

# Create your views here.


class TaskPagination(PageNumberPagination):
  page_size = 5
  page_size_query_param = "page_size"
  max_page_size = 50



class RegisterAPIView(APIView):
  
  def post(self,request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  

class LoginAPIView(APIView):

  def post(self,request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username,password=password)

    if not user:  # user exists with given username and pw so authenticating 
      return Response({'detail':'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)

    return Response({'refresh':str(refresh),
                     'access':str(refresh.access_token)
                    },status=status.HTTP_200_OK
                   )


class RefreshTokenAPIView(APIView):
  
  def post(self,request):
    refresh_token = request.data.get('refresh')

    try:
      refresh = RefreshToken(refresh_token)   # validaiton of refresh token 

      new_access = refresh.access_token      # creating a new access token from the refresh token

      return Response({'access':str(new_access)},status=status.HTTP_200_OK)

    except TokenError:
      return Response({'detail':'Invalid or expired refresh token'},status=status.HTTP_400_BAD_REQUEST)
    


class CreateTaskAPIView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self,request):
    data = request.data.copy()
    
    if not request.user.is_staff:
      data['owner'] = request.user.id
    else:
      if 'owner' not in data:
        data['owner'] = request.user.id

    serializer = TaskSerializer(data=data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ListTaskAPIView(APIView):
  permission_classes = [IsAuthenticated]
  pagination_class = TaskPagination

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
    
    paginator = self.pagination_class()
    page = paginator.paginate_queryset(tasks, request)

    if page is None:
      serializer = TaskSerializer(tasks, many=True)
      return Response(serializer.data)
      
    serializer = TaskSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)
  


class RetrieveTaskAPIView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self,request,id):
    task = TaskModel.objects.filter(id=id).first()
    if not task:
      return Response({"message":"Task not found"},status=status.HTTP_404_NOT_FOUND)
    
    if not request.user.is_staff:
    
      if task.owner_id != request.user.id:
        return Response({"message":"Illegal access"},status=status.HTTP_403_FORBIDDEN)
      
    
    serializer = TaskSerializer(task)
    return Response(serializer.data,status=status.HTTP_200_OK)



class UpdateTaskAPIView(APIView):
  permission_classes = [IsAuthenticated]

  def put(self,request,id):
    data = request.data.copy()
    task = TaskModel.objects.filter(id=id).first()

    if not task:
      return Response({"message":"Task not found"},status=status.HTTP_404_NOT_FOUND)
    

    if not request.user.is_staff:

      if task.owner_id != request.user.id:
        return Response({"message":"Illegal access"},status=status.HTTP_403_FORBIDDEN)
      
      data['owner'] = task.owner_id
    

    serializer = TaskSerializer(task, data=data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return  Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 






class DeleteTaskAPIView(APIView):
  permission_classes = [IsAuthenticated]

  def delete(self,request,id):
    task = TaskModel.objects.filter(id=id).first()

    if not task:
      return Response({"message":"Task not found"},status=status.HTTP_404_NOT_FOUND)
    
    if not request.user.is_staff:

      if task.owner_id != request.user.id:
        return Response({"message":"Illegal access"},status=status.HTTP_403_FORBIDDEN)
    
    
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
  

