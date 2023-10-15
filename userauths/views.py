from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL

def register_view(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hello {username}, Your account was created succesfully.")
            new_user = authenticate(username=form.cleaned_data.get("email"), 
                                    password=form.cleaned_data.get("password1")
            )
            login(request, new_user)
            return redirect("prossyApp:index")
    else:
        form = UserRegisterForm()

    
    context = {
        'form': form,
    }
    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("prossyApp:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
        except:
            messages.warning(request, f"User with {email} does not exist")
            
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in")
            return redirect("prossyApp:index")
        else:
            messages.warning(request, "User does not exist. Please create an account")
            
    context = {
        
    }
            
    return render(request, "userauths/sign-in.html", context)