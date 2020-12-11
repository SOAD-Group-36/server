from re import L
from django.http import response
from django.http.request import HttpRequest

from django.http.response import Http404
from users.models import ApiKey, Business
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from users.form import BusinessLoginForm, UserRegistrationForm


class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'home/register.html', context={'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save()
            return redirect('/login')
        else:
            return render(request, 'home/register.html', context={'form': form})


class BusinessLoginView(View):
    def get(self, request: HttpRequest):
        return render(request, 'home/business_login.html')

    def post(self, request):
        form = BusinessLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = Business.objects.get(email=email)
            except Business.DoesNotExist:
                return Http404()
            if user.check_password(password):
                response = redirect('api_keys')
                response.set_cookie('business', email, max_age=600, samesite='Lax')
                return response
        return render(request, 'home/business_login.html')


class APIKeyGenerateView(View):
    def get(self, request):
        context = {}
        try:
            email = request.COOKIES['business']
            user = Business.objects.get(email=email)
            context = {'api_keys': user.api_keys.all() }
        except:
            return redirect('home:home')
        return render(request, 'apikeys.html', context=context)
    
    def post(self, request):
        context = {}

        from django import forms
        class APIForm(forms.Form):
            name = forms.CharField(max_length=80, required=False)
        
        form = APIForm(request.POST)

        try:
            email = request.COOKIES['business']
            user = Business.objects.get(email=email)
            print(user)
            if form.is_valid():
                name=form.cleaned_data.get('name', '')
                api_key = ApiKey.objects.create(business=user, name=name)
            context = {'api_keys': user.api_keys.all() }
            print (user.api_keys.all())
        except:
            return redirect('home:home')
        return render(request, 'apikeys.html', context=context)
    
class DeleteAPIKey(View):
    def get(self, request, api_key):
        context = {}
        try:
            email = request.COOKIES['business']
            user = Business.objects.get(email=email)
            ApiKey.objects.get(key=api_key, business=user).delete()
            context = {'api_keys': user.api_keys.all() }
        except:
            return redirect('home:home')
        return render(request, 'apikeys.html', context=context)


