from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from authenticate.forms import SignUpForm
from django.contrib.auth.models import User

# Create your views here.


def home(request): 
	return render(request, 'home.html')

def login_user(request):
	if request.method == 'POST': #if someone fills out form , Post it
		username = request.POST['username']
		password = request.POST['password']
		try:
			user = authenticate(request, username=User.objects.get(email= username), password=password)
		except:
			user = authenticate(request, username=username, password=password)
		if user is not None:# if user exist
			login(request, user)
			messages.success(request,('Login Successful!!'))
			return redirect('home') #routes to 'home' on successful login  
		else:
			messages.success(request,('Email or Password is Incorrect!!'))
			return redirect('login') #re routes to login page upon unsucessful login
	else:
		return render(request, 'login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request,('Logged Out Successfully!'))
	return redirect('home')

def register_user(request):
	if request.method =='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ('Successfully Registered!'))
			return redirect('home')
	else: 
		form = SignUpForm() 

	context = {'form': form}
	return render(request, 'register.html', context)
