from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.shortcuts import redirect

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
                      {'template_data' : template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password'],
        )
        if user is None:
            template_data['error'] = 'The username or password is inorrect.'
            return render(request, 'accounts/login.html',
                          {'template_data' : template_data})
        else:
            auth_login(request, user)
            return redirect('accounts.login')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
                      {'template_data' : template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('home.index')
        else :
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                          {'template_data' : template_data})

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'accounts/password_reset_form.html'
