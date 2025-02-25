from django.contrib.auth.models import User
from django.contrib.postgres.search import TrigramSimilarity, TrigramWordSimilarity
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.db.models import Count
from blog.forms import EmailForm, CommentForm, SearchForm
from blog.models import Post
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from mysite import settings


def post_list(request, tag_slug=None):
    posts = Post.publish.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags=tag)
    paginator = Paginator(posts, 3)  # 1-что раскидать на стр, 2-кол-во объектов на стр
    page_number = request.GET.get('page', 1)  # 1-всегда, 2- параметр по умолчанию, в случ. отст.
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # num_pages-последняя страница
    return render(request, 'blog/post/list.html', {'posts': page_obj, 'tag': tag, })


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=slug,
                             published__year=year,
                             published__month=month,
                             published__day=day)
    comments = post.comments.filter(active=True)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.publish.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', 'published')[:4]
    form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})

#не надо
class PostListView(ListView):
    queryset = Post.publish.all()
    paginate_by = 3
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'


def share_post(request, post_id):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, id=post_id)
    sent = False
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            link_on_post = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd['name']} recommends you to read {post.title}'
            message = f"Read {post.title} at {link_on_post}\n\n" \
                      f"{cd['name']} ({cd['email']}) comments: {cd['comments']}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailForm()
    return render(request, 'blog/post/email.html', {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment_post=request.POST.copy() #делаем копию,которую сможет изменять т.к объект QueryDict является неизменяемым
    if request.user.is_authenticated:
        comment_post['name'] = request.user.username #добавл имя и почту в копию данных post запроса
        comment_post['email'] = request.user.email
    form = CommentForm(data=comment_post)#отправл классический пост запрос, но уже с почтой и именем
    comment = None
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET: #Триграммный поиск
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']  # стремминг-преобразование слова к словообраз. форме
            A = 1.0                             # Триграмма – это группа из трех следующих друг за другом символов
            B = 0.4
            results = Post.publish.annotate(
                similarity=(A / (A + B) * TrigramSimilarity('title', query)
                            + B / (A + B) * TrigramWordSimilarity(query, 'body'))
            ).filter(similarity__gte=0.1).order_by('-similarity')
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})

#не используется пока что
def user_total_posts(request,user_id=None):
    total_posts = Post.publish.count()
    user=None
    if user_id:
        user=get_object_or_404(User, id=user_id)
        total_posts=user.blog_posts.count()
    return render(request,'blog/base.html',{'total_posts':total_posts,'user':user})

