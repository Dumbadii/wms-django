from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Employee

class Login(APIView):
  def post(self,request):
    try:
      user = request.POST.get('username',None)
      pwd = request.POST.get('password',None)
      #Verify password
      obj = auth.authenticate(request,username=user,password=pwd)
      if obj:
        return Response({'token': 'hello'})
    except:
        return Response ({'code': 'no', 'message': 'verification failed'})

class Register(View):
  def post(self, request):
    try:
      username = request.POST.get('username',None)
      password = request.POST.get('password',None)
      last_name = request.POST.get('last_name',None)
      first_name = request.POST.get('first_name',None)
      department = request.POST.get('department')
      print(department)
      user = User.objects.create_user(
        username=username,
        password=password,
        last_name=last_name,
        first_name=first_name, 
        )
      user.save()
      emp = Employee.objects.create(user=user)
      emp.department_id = department
      emp.save()

    except:
      return JsonResponse ({'code': 'no', 'message': 'registration failed'})
    return JsonResponse ({'code':'ok','message ':'registration succeeded'})