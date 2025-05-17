from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import ContactForm
from .models import Contact
from django.shortcuts import render
from .models import Contact
from django.shortcuts import get_object_or_404

def home_view(request):
    return render(request, 'contact_app/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'contact_app/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'contact_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            return render(request, 'contact_app/contact_success.html', {'contact': contact})
    else:
        form = ContactForm()
    return render(request, 'contact_app/contact.html', {'form': form})

def contact_list_view(request):
    if request.user.is_authenticated:
        contacts = Contact.objects.all().order_by('-id')
        return render(request, 'contact_app/contact_list.html', {'contacts': contacts})
    else:
        messages.error(request, "You need to log in to view contacts.")
        return redirect('login')
def contact_list_view(request):
    contacts = Contact.objects.all().order_by('-id') if request.user.is_authenticated else None
    return render(request, 'contact_app/contact_list.html', {'contacts': contacts})


def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contact_app/edit_contact.html', {'form': form})


def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'contact_app/delete_confirm.html', {'contact': contact})

def home(request):
    return render(request, 'home.html')