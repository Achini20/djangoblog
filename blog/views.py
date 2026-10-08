from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Category
from .forms import PostForm, RegisterForm


def home(request):
    post_list = (
        Post.objects.filter(status='published')
        .select_related('category')
        .prefetch_related('tags')
        .order_by('-created_at')
    )

    categories = Category.objects.all()
    selected_category = request.GET.get('category')

    if selected_category:
        post_list = post_list.filter(category__name=selected_category)

    paginator = Paginator(post_list, 6)
    posts = paginator.get_page(request.GET.get('page'))

    return render(request, 'blog/home.html', {
        'posts': posts,
        'categories': categories,
        'selected_category': selected_category,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    return render(request, 'blog/post_detail.html', {'post': post})


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})


class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("home")


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "blog/register.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response