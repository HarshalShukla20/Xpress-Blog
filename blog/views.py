from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post


def home(request):      #function based views
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

#class based views look for a template with naming convention as: <app>/<model>_<viewtype>.html
#so we need to make a template of the same name otherwise it won't work
#else we can change the template that it looks for which is what we'll be doing here
class PostListView(ListView):
    model = Post  #tells us which model to query(here we are working on post so using Post model)
    template_name = 'blog/home.html'   #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    #the variable used in templates for posts is 'posts' but ListView by default uses a different variable so we have to change it
    ordering = ['-date_posted'] #orders the posts from newest to oldest(- sign at front)
    paginate_by = 5 #paginated our posts so that there are only two posts per page

class UserPostListView(ListView): #class based view for displaying the posts by a specific user
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #mixins have to be at the left
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object() #method to get the object of the current post we're trying to update
        if (self.request.user == post.author):
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if (self.request.user == post.author):
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
