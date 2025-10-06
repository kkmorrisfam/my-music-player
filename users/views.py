from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Create your views here.
def register_view(request):
    # what to do when posted
    if request.method == "POST":
        #creates dict object instance of the form and adds data submitted through http POST request
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # form.save()
            # login user and save user after valid
            login(request, form.save())
            return redirect("music:home") #when form is submitted and valid
    else:
        #just create empty form
        form = UserCreationForm()
    return render(request, "users/register.html", { "form": form})


def login_view(request):
    if request.method == "POST":
        #when a user submits form using POST, the data entered into form fields is sent to server within request dictionary. 
        form = AuthenticationForm(data=request.POST)
        #after instance has data, check for validation
        if form.is_valid():
            # now you can login with form user
            login(request, form.get_user())
            return redirect("music:home")
    else: 
        # create empty form
        form = AuthenticationForm()
    return render(request, "users/login.html", { "form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("music:home")