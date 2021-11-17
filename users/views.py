from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404


# Create your views here.
from actions.models import Action


# View to register a new account
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

        # Log them in
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        # If user was authenticated, store info in session
        if user is not None:
            request.session['username'] = user.username
            request.session['role'] = user.details.role

        return redirect('adventures:home')
    else:
        return render(
            request,
            'users/user/register.html',
        )


# View for the profile page
def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_id = user.id
    actions = Action.objects.filter(user_id__exact=user_id).order_by('-created')

    return render(
        request,
        'users/user/profile.html',
        {'user': user,
         'actions': actions},
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


# View for admin list of users
def user_list(request):
    username = request.session.get('username')
    user = get_object_or_404(User, username=username)
    role = user.details.role

    # Display list of users to admin
    if role == 'admin':
        users = User.objects.all()
        return render(request,
                      'users/user/userList.html',
                      {'users': users},
                      )

    else:
        return redirect('adventures:home')


# View for editing user for admin
def edit_user(request, username):
    user = get_object_or_404(User, username=username)

    # Change the users role
    if request.method == 'POST':

        role = request.POST.get('role')
        password = request.POST.get('password')
        user.first_name = request.POST.get('firstName')
        user.last_name = request.POST.get('lastName')
        user.email = request.POST.get('email')

        # If there's a new password, change it
        if password != '':
            user.password = password

        # If there's a new role, change it
        if role != 'same':
            user.details.role = role
            session_user = User.objects.get(username=request.session.get('username'))
            action = Action(
                user=session_user,
                verb="changed user role of:",
                target=user,
            )
            action.save()

        user.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            "%s's account successfully updated!" % username,
        )
        return redirect('users:list')

    # Else, render the edit page
    else:
        return render(request,
                      'users/user/userEdit.html',
                      {'user': user}
                      )