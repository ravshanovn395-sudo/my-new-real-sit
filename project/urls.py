from django.urls import path
from .views import login_page, logout_page, home_page, chat_page, SignUpView, create_car, car_view, car_delete

urlpatterns = [
    path("", home_page, name="home_page"),
    path("chat/", chat_page, name="chat_page"),
    path("login/", login_page, name="login_page"),
    path("logout/", logout_page, name="logout_page"),
    path("signup/", SignUpView.as_view(), name="signup_page"),
    path("create/", create_car, name="create_car"),
    path("car/<int:car_id>/", car_view, name="car_view"),        # Batafsil ko'rish URL
    path("car/<int:car_id>/delete/", car_delete, name="car_delete"), # O'chirish URL
]