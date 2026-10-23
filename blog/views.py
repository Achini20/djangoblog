from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PostForm, RegisterForm
from .models import Post, Category


def home(request):
    post_list = (
        Post.objects.filter(status='published')
        .select_related('category', 'author')
        .prefetch_related('tags')
        .order_by('-created_at')
    )

    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    query = request.GET.get('q', '').strip()

    if selected_category:
        post_list = post_list.filter(category__name=selected_category)

    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    paginator = Paginator(post_list, 6)
    posts = paginator.get_page(request.GET.get('page'))

    return render(request, 'blog/home.html', {
        'posts': posts,
        'categories': categories,
        'selected_category': selected_category,
        'query': query,
    })


def post_detail(request, slug):
    if request.user.is_authenticated:
        queryset = Post.objects.filter(Q(status='published') | Q(author=request.user))
    else:
        queryset = Post.objects.filter(status='published')
    post = get_object_or_404(queryset, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


def custom_403(request, exception=None):
    return render(request, "blog/403.html", status=403)


def error_505(request):
    return render(request, "505.html", status=505)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post published successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    login_url = "login"
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.get_object().author == self.request.user


class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/my_posts.html"
    paginate_by = 6
    login_url = "login"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by("-created_at")


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "blog/register.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response