from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse

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
      user = User.objects.create_user(username=username,password=password)
      user.save()
    except:
      return JsonResponse ({'code': 'no', 'message': 'registration failed'})
    return JsonResponse ({'code':'ok','message ':'registration succeeded'})