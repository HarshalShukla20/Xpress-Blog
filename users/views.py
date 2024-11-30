from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid(): #checks if the form is valid or not eg username already exists passwords don't match
            form.save() #saves the user that we have cretaed using the form
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has  been created. You are now able to login.')
            return redirect('login') #after successfully registering the user, redirecting them to login page so they can log in to their newly created account
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)       #user update form instance is created
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)    #profile update form instance is created

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {         #created a context to pass the form instances into templates
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
