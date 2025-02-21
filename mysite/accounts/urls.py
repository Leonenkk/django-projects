from django.contrib.auth.views import LogoutView
from django.urls import path
import accounts.views as views

app_name='accounts'

urlpatterns=[
    path('signup/',views.SignUpView.as_view(), name='signup'),
    path('login',views.CustomLoginView.as_view(redirect_authenticated_user=True,#авториз пользователь не сможет на стр входа
                                         template_name='registration/login.html'),
                                         name='login'),
    path('logout/',LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('profile/',views.profile, name='profile'),
    path('change_password/',views.ChangePasswordView.as_view(), name='change_password'),
]