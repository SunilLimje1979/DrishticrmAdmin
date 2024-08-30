from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
import json
import datetime
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def hello(request):
    return HttpResponse("Hello Drishti CRM Admin...")


def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass1']
        print(username, password)

        user = authenticate(request, username=username, password=password)
        print(user)

        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect(Login)

        else:
            login(request,user)
            # messages.success(request, "You have successfully signed in")
            return redirect(index)
        
    return render(request, 'login.html')

def index(request):
    return render(request, 'index.html', context={})
def base(request):
    return render(request, 'base.html', context={})

def Logout(request):
    logout(request)
    messages.success(request, "You have successfully signed out")
    return redirect(Login)



def allRegistered(request):
    url="https://drishtis.app/DrishticrmMaster/api/get_all_appmasters/"
    res=requests.get(url)
    # print(res.text)
    if(res.json().get('message_code')==1000):
        all_data=res.json().get('message_data')
        # print(all_data)
        city_response = requests.post("http://13.233.211.102/masters/api/get_cities_by_state_id/",json={"state_id":22})
        cities = (city_response.json().get("message_data", [])).get('cities',[])
        # print(cities)
        # return render(request,'main/allRegistered.html',{'all_doctors':all_doctors})
        return render(request,'main/demo.html',{'all_data':all_data,"cities": cities})

def get_appmaster_details(request,id):
    print("app_id",id)

    api_url="https://drishtis.app/DrishticrmMaster/api/get_appmaster_by_id/"
    response=requests.post(api_url,json={'app_id':id})
    appdata=response.json().get("message_data",{})
    print(appdata)

    sub_res = requests.post("https://drishtis.app/DrishticrmMaster/api/validate_subscription/", json={"app_id":id})
    print(sub_res.text)
    subdata=sub_res.json().get('message_data',{})
    subdata['validity'] = sub_res.json().get('message_text')
    print(subdata)
     
        
    return render(request,'main/appDetails.html',{'appdata':appdata,'subdata':subdata})

@csrf_exempt
def reset_password(request):
    response_data = {
        'message_code': 999,
        'message_text': 'Error occurred.'
    }
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            new_password = data.get('new_password')
            print(user_id,new_password)
            
            #Call the external API to reset the password
            api_response = requests.post('https://drishtis.app/DrishticrmMaster/api/change_password/', json={
                'user_id': user_id,
                'new_password': new_password
            })

            print(api_response.text)
            #Parse the API response
            api_data = api_response.json()
            
            if api_data['message_code'] == 1000:
                response_data['message_code'] = 1000
                response_data['message_text'] = 'Password reset successfully.'
            else:
                response_data['message_text'] = api_data.get('message_text', 'Unknown error.')
        
        except Exception as e:
            response_data['message_text'] = str(e)
    
    return JsonResponse(response_data)

@csrf_exempt
def toggle_subscription_status(request):
    response_data = {
        'message_code': 999,
        'message_text': 'Error occurred.'
    }
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            subscription_id = data.get('appMasterSubscriptionId')
            new_status = data.get('newStatus')
            print(subscription_id,new_status)

            # Ensure the subscription_id and status are provided
            if not subscription_id or not new_status:
                response_data['message_text'] = 'Subscription ID and Status are required.'
                return JsonResponse(response_data)
            
            if(new_status=='block'):
                sub_status=1
            else:
                sub_status=0
            #Call the external API to toggle the subscription status
            api_response = requests.post('https://drishtis.app/DrishticrmMaster/api/update_subscription_status/', json={
                'appmaster_subscription_id': subscription_id,
                'subscription_status': sub_status
            })

            # # Parse the API response
            api_data = api_response.json()
            print(api_data)
            if api_data['message_code'] == 1000:
                response_data['message_code'] = 1000
                response_data['message_text'] = f'App {new_status} successfully!'
                response_data['new_status'] = sub_status
            else:
                response_data['message_text'] = api_data.get('message_text', 'Unknown error.')
        
        except Exception as e:
            response_data['message_text'] = str(e)
    
    return JsonResponse(response_data)

def filter_doctors(request):
    if request.method == 'GET':
        city = request.GET.get('city')
        start_date = request.GET.get('startDate')
        end_date = request.GET.get('endDate')
        print(city)
        print(start_date,'start_date')
        print(end_date,'end_date')
        data=[]
        res=requests.post("http://13.233.211.102/doctor/api/fillter_doctors/",json={"city_id": city,"start_date":start_date,"end_date":end_date})
        data=res.json().get('message_data',[])
        print(data)
        return JsonResponse({'doctors': data})

    return JsonResponse({'error': 'Invalid request'}, status=400)
    


