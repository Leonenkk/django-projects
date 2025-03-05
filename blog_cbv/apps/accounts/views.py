from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView

from apps.accounts.forms import ProfileUpdateForm, UserUpdateForm, UserRegistrationForm, UserLoginForm
from apps.accounts.models import Profile


class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'accounts/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Профиль пользователя {self.request.user.username}'
        return context


class ProfileUpdateView(UpdateView):
    template_name = 'accounts/profile_edit.html'
    model = Profile
    form_class = ProfileUpdateForm

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']=f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form']=UserUpdateForm(self.request.POST,instance=self.request.user)
        else:
            context['user_form']=UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self,form):#form-та форма что явно указана в get_form_class
        context=self.get_context_data()#контекст в первую очередь словарь
        user_form=context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                form.save()
                user_form.save()
            else:
                context.update({'user_form':user_form})#обновляем чтобы отобразить ошибки и сохр уже ранее введ данные
                return self.render_to_response(context)#ренедерим чтобы показать ошибки валидации
        return super().form_valid(form)

    def get_success_url(self):#тут object так как ссылаемся на только что обновл или созд объект
        return reverse_lazy('accounts:profile_detail',kwargs={'slug':self.object.slug})


class UserRegistrationView(SuccessMessageMixin,CreateView):
    template_name = 'accounts/user_register.html'
    form_class=UserRegistrationForm
    success_url = reverse_lazy('blog:post_list')
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Регистрация пользователя'
        return context


class UserLoginView(SuccessMessageMixin,LoginView):
    template_name = 'accounts/user_login.html'
    form_class = UserLoginForm
    success_message = 'Добро пожаловать на сайт!'
    next_page = 'blog:post_list'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Авторизация пользователя'
        return context

class UserLogoutView(LogoutView):
    next_page = 'blog:post_list'



