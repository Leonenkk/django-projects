
from django.views.generic import ListView, DetailView, CreateView

from apps.blog.forms import PostForm
from apps.blog.models import Post, Category


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 2
    queryset=Post.custom.all()

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Главная страница'
        return context
    #pagination get_elided... добавить


class PostDetailView(DetailView):
    model=Post
    template_name='blog/post_detail.html'
    context_object_name='post'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['title']=self.object.title #объект вызываемый PostDetail
        return context


class PostFromCategoryView(ListView):
    template_name='blog/post_list.html'
    context_object_name='posts'
    category=None
    paginate_by=2

    def get_queryset(self):
        self.category=Category.objects.get(slug=self.kwargs['slug'])
        queryset=Post.objects.filter(category__slug=self.category.slug)
        if not queryset:
            sub_category=Category.objects.filter(parent=self.category)
            queryset=Post.objects.filter(category__in=sub_category)
            #дописать, что если постов нет, то вывести сообщение об их отсутствии и вывести все посты
        return queryset


    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['title']=self.category.title
        return context


class CreatePostView(CreateView):
    template_name='blog/post_create.html'
    form_class=PostForm
    model=Post

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи на сайт'
        return context

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)