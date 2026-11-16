from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic
from .models import Car, ChatMessage


# 1. urls.py so'ragan SignUpView klassi qo'shildi
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login_page')
    template_name = 'register/signup.html'  # O'zingizdagi signup shablon yo'lini yozing


def login_required_decorator(func):
    return login_required(func, login_url='login_page')

@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect('login_page')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}!")
            return redirect('home_page')

        messages.error(request, 'Noto\'g\'ri foydalanuvchi nomi yoki parol.')

    return render(request, 'register/login.html')
            
@login_required_decorator
def home_page(request):
    search_query = request.GET.get('q', '').strip()
    cars = Car.objects.all()
    if search_query:
        cars = cars.filter(
            Q(name__icontains=search_query) | Q(about__icontains=search_query)
        )
    return render(
        request,
        'register/index.html',
        {'cars': cars, 'search_query': search_query},
    )


@login_required_decorator
def chat_page(request):
    if request.method == 'POST':
        text = (request.POST.get('text') or '').strip()
        if not text:
            messages.error(request, 'Xabar bo‘sh bo‘lishi mumkin emas.')
        elif len(text) > 500:
            messages.error(request, 'Xabar 500 ta belgidan oshmasligi kerak.')
        else:
            ChatMessage.objects.create(user=request.user, text=text)
            return redirect('chat_page')

    chat_messages = ChatMessage.objects.select_related('user').all()
    return render(request, 'register/chat.html', {'chat_messages': chat_messages})


@login_required_decorator
def create_car(request):
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        name = request.POST.get('name')
        about = request.POST.get('about')
        image = request.FILES.get('image')

        car = Car(name=name, about=about, image=image)
        car.save()
        return redirect('home_page')

    return render(request, 'register/create_car.html')


@login_required_decorator
def car_view(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        return redirect('home_page')

    return render(request, 'register/car_view.html', {'car': car})


@login_required_decorator
def car_delete(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        return redirect('home_page')

    car.delete()
    return redirect('home_page')