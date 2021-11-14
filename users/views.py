from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404

# Create your views here.

def register(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username, email, password)

        messages.add_message(
            request,
            messages.SUCCESS,
            "You successfully registered a new user: %s" % user.username,
        )

        return redirect('adventures:home')
    else:
        return render(
            request,
            'users/user/register.html',
        )

def profile(request, username):
    user = get_object_or_404(User, username=username)

    return render(
        request,
        'users/user/profile.html',
        { 'user': user },
    )

# View to login
def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    # If user was authenticated, store info in session
    if user is not None:
        request.session['username'] = user.username
        request.session['role'] = user.details.role

        messages.add_message(
            request,
            messages.SUCCESS,
            "You have logged-in successfully as %s" % user.username,
        )

    # Else, not authenticated, invalid user
    else:
        messages.add_message(
            request,
            messages.ERROR,
            "Invalid username or password.",
        )

    return redirect('adventures:adventure_location_list')


# View to logout
def logout_user(request):
    del request.session['username']
    del request.session['role']
    messages.add_message(
        request,
        messages.SUCCESS,
        "You have successfully logged out.",
    )
    return redirect('adventures:home')