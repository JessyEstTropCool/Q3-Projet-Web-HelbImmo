from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
    )
from django.http import JsonResponse
from .models import Post, PostConsult
from .forms import PostCreateForm, GalleryForm
import datetime

"""def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)"""

def add_favorite(request):
    if request.user.is_authenticated:
        user = request.user
        post = Post.objects.filter(pk=request.GET.get('postid', None)).first()
        data = {
            'added': True
        }

        if ( user.profile in post.profile_set.all() ):
            data['added'] = False
            post.profile_set.remove(user.profile)
        else:
            post.profile_set.add(user.profile)

        data['count'] = post.profile_set.count()
        
        return JsonResponse(data)
    return JsonResponse({'added': 'no'})

def post_consulted(request):
    view = PostConsult(post=Post.objects.filter(pk=request.GET.get('postid', None)).first())

    view.save()
    
    data = { 'good': view.__str__() }

    return JsonResponse(data)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['author'] = User.objects.filter(username=self.kwargs.get('username')).first()
        context['title'] = self.kwargs.get('username')
        return context

class FavoritesListView(ListView):
    model = Post
    template_name = 'blog/favorites.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return self.request.user.profile.favorites.all()

class PostDetailView(DetailView):
    model = Post

class PostStatsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Post
    template_name = 'blog/post_stats.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostStatsView, self).get_context_data(**kwargs)

        post = Post.objects.filter(pk=self.kwargs.get('pk')).first()
        indivConsults = {}
        cumulConsults = {}
        indivMax = 0
        cumulMax = 0
        dateConsult = datetime.date.today() - datetime.timedelta(29)

        context['dateStart'] = dateConsult
        context['dateEnd'] = datetime.date.today()

        for i in range(30):
            indivConsults[dateConsult] = PostConsult.objects.filter(date=dateConsult, post=post).count()
            cumulConsults[dateConsult] = PostConsult.objects.filter(date__lte=dateConsult, post=post).count()
            
            if indivConsults[dateConsult] > indivMax:
                indivMax = indivConsults[dateConsult]

            if cumulConsults[dateConsult] > cumulMax:
                cumulMax = cumulConsults[dateConsult]

            dateConsult += datetime.timedelta(1)
        
        context['title'] = "Statistiques de " + post.title
        context['consults'] = PostConsult.objects.filter(post=self.kwargs.get('pk'))
        context['indivConsults'] = indivConsults
        context['cumulConsults'] = cumulConsults
        context['indivGraphHeight'] = indivMax + 10 - (indivMax % 10)
        context['cumulGraphHeight'] = cumulMax + 10 - (cumulMax % 10)


        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    success_url = '/'
    form_class = PostCreateForm
    gallery_form_class = GalleryForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)

    """def post(self, request, *args, **kwargs):
        main_form = self.form_class(request.POST)
        gall_form = self.gallery_form_class(request.POST, prefix='gall_form')
        print(main_form.errors)
        return render(request, self.template_name, {'form': main_form, 'gall_form': gall_form})"""

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    #fields = ['title', 'content']
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})