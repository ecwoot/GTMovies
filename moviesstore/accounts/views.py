from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

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
        return render(request, 'accounts/signup.html', {'template_data': template_data})

    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            user = form.save(commit=False)  # Save without committing
            user.email = form.cleaned_data.get('email')  # Explicitly set the email
            user.save()  # Now save the user with the email
            return redirect('home.index')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'accounts/password_reset_form.html'
