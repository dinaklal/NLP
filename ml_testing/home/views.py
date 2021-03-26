from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth

import json
from django.conf import settings
# Create your views here.
def home(request):
    username = request.user.username
    takeaway =[{
         'id': 288,
        'name': 'TigerByte'
    },{
         'id': 2,
        'name': 'Tasty Shrooms'
    },{
         'id': 3,
        'name': 'FisherMans Cove'
    }]







    #items = [{"id" :"1","name":"Pizza"},{"id":"2","name":"Meals"}]
    #output_customers = [{'customer':'71343247','items':['burger','pizza']},{'customer':'71343246','items':['meals<br>','pizza<br>','meals<br>','pizza','meals','pizza','meals','pizza']}]

    return render(request, 'home.html')
def logout(request):
    auth.logout(request)
    return redirect('/')
