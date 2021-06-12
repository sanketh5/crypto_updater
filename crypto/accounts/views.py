from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.forms import UserAdminCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

@login_required
def register(req):
    form = UserAdminCreationForm()
    if req.method == 'POST':
        form = UserAdminCreationForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('register')
    return render(req, 'register.html', {'form': form})



def custom_login(request):
    form = AuthenticationForm()
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("../")
        else:
            return render(request,'accounts/login.html',{'form': form,'error':"wrong credentials"})
    
    return render(request,'accounts/login.html', {'form': form})