from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from taggit.models import Tag

from apps.blog.forms import PostForm, PostUpdateForm, CommentForm
from apps.blog.models import Post, Category, Comment
from apps.services.mixins import AuthorRequiredMixin


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 2
    queryset = Post.custom.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context
    # pagination get_elided... добавить


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title  # объект вызываемый PostDetail
        context['form'] = CommentForm()
        return context


class PostFromCategoryView(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    category = None
    paginate_by = 2

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Post.objects.filter(category__slug=self.category.slug)
        if not queryset:
            sub_category = Category.objects.filter(parent=self.category)
            queryset = Post.objects.filter(category__in=sub_category)
            # дописать, что если постов нет, то вывести сообщение об их отсутствии и вывести все посты
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.category.title
        return context


class CreatePostView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'blog/post_create.html'
    form_class = PostForm
    model = Post
    login_url = 'blog:post_list'
    success_message = 'Запись была успешно добавлена'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class PostUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'blog/post_update.html'
    context_object_name = 'post'
    success_message = 'Запись была успешно обнавлена'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление статьи: {self.object.title}'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)



class CommentCreateView(CreateView):
    form_class = CommentForm
    model=Comment

    def dispatch(self, request, *args, **kwargs):
        print(f"🔹 {request.user} делает запрос на {request.path}")  # Логирование
        return super().dispatch(request, *args, **kwargs)

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_invalid(self, form):
        if self.is_ajax():
            return JsonResponse({'error': form.errors}, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):

        if not self.is_ajax():
            print("Запрос НЕ AJAX! Редирект...")
            return redirect('blog:post_detail', pk=self.kwargs.get('pk'))

        comment = form.save(commit=False)
        comment.post_id = self.kwargs.get('pk')
        comment.author = self.request.user
        comment.parent_id = form.cleaned_data.get('parent')
        print(f"Создаёт комментарий: {self.request.user}")  # Логирование
        print(f"ID поста: {self.kwargs.get('pk')}")  # Логирование
        print(f"Родительский коммент: {form.cleaned_data.get('parent')}")  # Логирование
        comment.save()

        if self.is_ajax():
            return JsonResponse({
                'is_child': comment.is_child_node(),
                'id': comment.id,
                'author': comment.author.username,
                'parent': comment.parent_id,
                'time_create': comment.time_create.strftime('%Y-%m-%d %H:%M:%S'),
                'avatar': comment.author.profile.avatar.url,
                'content': comment.content,
                'get_absolute_url': comment.author.profile.get_absolute_url(),
            }, status=200)
        return redirect(comment.post.get_absolute_url())

    def handle_no_permission(self):
        print(f" Пользователь {self.request.user} не имеет доступа к {self.request.path}")#Логирование
        return JsonResponse({'error': 'Необходимо авторизоваться для добавления комментариев'}, status=403)


class PostByTagListView(ListView):
    template_name = 'blog/post_list.html'
    model = Post
    context_object_name='posts'
    paginate_by = 2
    tag=None

    def get_queryset(self):
        self.tag=get_object_or_404(Tag,slug=self.kwargs['tag'])
        queryset=self.model.custom.filter(tags__slug=self.tag.slug)
        return queryset      #посмореть почему при переходе на пост аж 18 запросов к бд

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']=f'Статьи по тегу {self.tag.name}'
        return context
