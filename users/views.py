from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import RegisterUserForm, UpdateUserForm
from django.contrib.auth.models import User
from django.contrib import messages




def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id) # gets current logged in user
        #create instance to prepopulate form on initial load
        form =UpdateUserForm(request.POST or None, instance=current_user)
        
        if form.is_valid():
            form.save()

            # login user again with new information
            login(request, current_user)
            messages.success(request, "User Has Been Updated!")
            return redirect('music:home')
        # if form not valid, rerender current page
        return render(request, "users/update_user.html", {"form": form})
    # if user not logged in
    else:
        messages.warning(request, "Please log in")
        return redirect('music:home')
    
    #return render(request, "users/register.html", {"form": form })



def register_view(request):
    # what to do when posted
    if request.method == "POST":
        #creates dict object instance of the form and adds data submitted through http POST request
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            # form.save()
            # login user and save user after valid
            login(request, form.save())
            return redirect("music:home") #when form is submitted and valid
    else:
        #just create empty form
        form = RegisterUserForm()

    return render(request, "users/register.html", { "form": form})


def login_view(request):
    if request.method == "POST":
        #when a user submits form using POST, the data entered into form fields is sent to server within request dictionary. 
        form = AuthenticationForm(data=request.POST)
        #after instance has data, check for validation
        if form.is_valid():
            # now you can login with form user
            login(request, form.get_user())
            # if hidden field named "next", sent in POST object has value
            # then redirect user to value in "next" field
            if "next" in request.POST:                
                return redirect(request.POST.get('next'))
            else: 
                return redirect("music:home")
    else: 
        # create empty form
        form = AuthenticationForm()
    return render(request, "users/login.html", { "form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("music:home")
    

