from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.forms import SingUpForm, LoginForm, UserUpdateForm, ProfileUpdateForm


class SignUpView(CreateView):
    form_class = SingUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'
    initial = None  # начальные данные

    def dispatch(self, request, *args,**kwargs): #внутри происходит проверка метода запроса, так выбирается нужный метод
        if request.user.is_authenticated:
            return redirect(to='/blog/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Account created for {username}')
            return redirect('accounts:login')
        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):  # если чел ввел норм данные
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)  # если не выбрал запомнить меня. то сеанс после выкл браузера закончится
            self.request.session.modified = True  # обновляем данные
        return super(CustomLoginView, self).form_valid(form)  # время такое же как и Cookie session age


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_message = 'Your password has been updated!'
    success_url = reverse_lazy('accounts:profile')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES,
                                         instance=request.user.profile)  # если есть файлы(2)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request,
                  'registration/profile.html',
                  {'user_form': user_form, 'profile_form': profile_form})
