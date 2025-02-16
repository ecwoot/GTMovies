from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',{'template_data' : template_data})
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

# class CustomPasswordResetView(PasswordResetView):
#     email_template_name = 'accounts/password_reset_email.html'
#     success_url = reverse_lazy('password_reset_done')
#     template_name = 'accounts/password_reset_form.html'
    
    
    
class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    
    


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()

    # 
def form_valid(self, form):
    # Get the email from the form
    email = form.cleaned_data['email']
    
    try:
        # Get the user by email
        user = User.objects.get(email=email)
        
        # Generate the token for password reset
        token = default_token_generator.make_token(user)
        
        # URL encoding the user’s ID to safely pass it as part of the URL
        uidb64 = urlsafe_base64_encode(user.pk.encode())

        # Build the reset URL
        reset_link = self.request.build_absolute_uri(
            reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        )
        
        # Create the email content
        subject = 'Your Password Reset Request'
        message = f'''
        Hi {user.username},
        
        You have requested to reset your password. Please click the link below to set a new password:
        
        {reset_link}
        
        If you did not request a password reset, please ignore this email.
        '''
        
        # Send the email
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        
    except User.DoesNotExist:
        # Handle case where user does not exist
        form.add_error('email', 'No user found with this email address.')

    # Return success response
    return super().form_valid(form)

# def resend_password_reset_email(request):
#     template_data = {}
#     template_data['title'] = 'Resend Password Reset Email'

#     if request.method == "POST":
#         email = request.POST.get("email")

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             template_data["error"] = "If an account exists, an email will be sent."
#             return render(request, "accounts/resend_password_reset.html", {"template_data": template_data})

#         # Direct password reset URL (where users enter their email again)
#         reset_url = request.build_absolute_uri(reverse_lazy("password_reset"))

#         # Email content
#         subject = "Password Reset Request"
#         email_body = (
#             f"Hello {user.username},\n\n"
#             "We received a request to reset your password. Click the link below to reset it:\n"
#             f"{reset_url}\n\n"
#             "If you did not request this, please ignore this email.\n\n"
#             "Best,\nYour Website Team"
#         )

#         # Send email
#         send_mail(subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email])

#         template_data["success"] = "If an account exists, a password reset email has been sent."
#         return render(request, "accounts/resend_password_reset.html", {"template_data": template_data})

#     return render(request, "accounts/resend_password_reset.html", {"template_data": template_data})

