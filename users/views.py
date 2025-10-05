from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register_view(request):
    # what to do when posted
    if request.method == "POST":
        #creates dict object instance of the form and adds data submitted through http POST request
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("music:home") #when form is submitted and valid
    else:
        #just create empty form
        form = UserCreationForm()
    return render(request, "users/register.html", { "form": form})