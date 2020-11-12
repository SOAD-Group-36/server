from django.shortcuts import render, redirect
from django.views import View

from users.form import UserRegistrationForm


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
