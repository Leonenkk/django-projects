from django.urls import path

from apps.accounts.views import ProfileUpdateView, ProfileDetailView, UserRegistrationView, UserLoginView, \
    UserLogoutView

app_name='accounts'
urlpatterns=[
    path('user/edit/',ProfileUpdateView.as_view(),name='profile_edit'),
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('user/<slug:slug>/',ProfileDetailView.as_view(),name='profile_detail'),
]