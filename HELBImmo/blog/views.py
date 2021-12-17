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
from django.http import JsonResponse, request
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post, PostConsult, PostFavorite
from .forms import PostCreateForm, GalleryForm
import datetime

class PaginatedMixin():
    def paginate(self, context):
        data = self.get_queryset()
        paginate_by = self.request.GET.get('paginate_by', 5)
        page = self.request.GET.get('page', 1)

        paginator = Paginator(data, paginate_by)

        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context['per_page_values'] = [5, 10, 25, 50]
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        context[self.context_object_name] = page_obj

class FavoritesMixin():
    def get_user_favorites(self):
        if self.request.user.is_authenticated:
            favs = PostFavorite.objects.filter(user=self.request.user)
            return Post.objects.filter(id__in=favs.values('post'))
        else:
            return None
        


def add_favorite(request):
    if request.user.is_authenticated:
        user = request.user
        post = Post.objects.filter(pk=request.GET.get('postid', None)).first()
        data = {
            'added': True
        }

        fav = PostFavorite.objects.filter(user=user, post=post)

        if fav:
            data['added'] = False
            fav.delete()
        else:
            fav = PostFavorite(user=user, post=post)
            fav.save()
        
        return JsonResponse(data)
    return JsonResponse({'added': 'no'})

def post_consulted(request):
    view = PostConsult(post=Post.objects.filter(pk=request.GET.get('postid', None)).first())

    view.save()
    
    data = { 'good': view.__str__() }

    return JsonResponse(data)

class PostListView(PaginatedMixin, FavoritesMixin, ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.paginate(context)
        context['user_favs'] = self.get_user_favorites()
        return context

class SearchResultsListView(PaginatedMixin, FavoritesMixin, ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        terms = self.request.GET.get('q')
        results = Post.objects.filter(
            Q(content__icontains=terms) | Q(title__icontains=terms) | Q(region_city__icontains=terms)
        ).order_by('-date_posted')

        if ( self.request.GET.get('budgetMax') ):
            results = results.filter(price__lte=self.request.GET.get('budgetMax'))
        if ( self.request.GET.get('budgetMin') ):
            results = results.filter(price__gte=self.request.GET.get('budgetMin'))

        return results

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)

        self.paginate(context)

        context['user_favs'] = self.get_user_favorites()

        context['terms'] = self.request.GET.get('q')
        context['title'] = 'Recherche - ' + self.request.GET.get('q')
        return context

class UserPostListView(PaginatedMixin, FavoritesMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)

        self.paginate(context)

        context['user_favs'] = self.get_user_favorites()

        context['author'] = User.objects.filter(username=self.kwargs.get('username')).first()
        context['title'] = self.kwargs.get('username')
        return context

class FavoritesListView(PaginatedMixin, FavoritesMixin, ListView):
    model = Post
    template_name = 'blog/favorites.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'favs'
    paginate_by = 5

    def get_queryset(self):
        return PostFavorite.objects.filter(user=self.request.user).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(FavoritesListView, self).get_context_data(**kwargs)

        self.paginate(context)
        
        context['user_favs'] = self.get_user_favorites()

        context['title'] = 'Votre Watchlist'

        return context

class PostDetailView(FavoritesMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        
        context['user_favs'] = self.get_user_favorites()
        context['title'] = Post.objects.filter(id=self.kwargs.get('pk')).first().title

        return context

class PostStatsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Post
    template_name = 'blog/post_stats.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostStatsView, self).get_context_data(**kwargs)

        dateTimeStat = datetime.datetime.combine(datetime.datetime.today(), datetime.time.max) - datetime.timedelta(29)
        dateStat = dateTimeStat.date()

        post = Post.objects.filter(pk=self.kwargs.get('pk')).first()
        indivConsults = { 'data': {}, 'height': 0, 'start': dateStat, 'end': datetime.date.today() }
        cumulConsults = { 'data': {}, 'height': 0, 'start': dateStat, 'end': datetime.date.today() }
        indivFavs = { 'data': {}, 'height': 0, 'start': dateStat, 'end': datetime.date.today() }
        cumulFavs = { 'data': {}, 'height': 0, 'start': dateStat, 'end': datetime.date.today() }

        for i in range(30):
            indivConsults['data'][dateStat] = PostConsult.objects.filter(date=dateStat, post=post).count()
            cumulConsults['data'][dateStat] = PostConsult.objects.filter(date__lte=dateStat, post=post).count()
            indivFavs['data'][dateStat] = PostFavorite.objects.filter(date__date=dateStat, post=post).count()
            cumulFavs['data'][dateStat] = PostFavorite.objects.filter(date__lte=dateTimeStat, post=post).count()
            
            if indivConsults['data'][dateStat] > indivConsults['height']:
                indivConsults['height'] = indivConsults['data'][dateStat]

            if cumulConsults['data'][dateStat] > cumulConsults['height']:
                cumulConsults['height'] = cumulConsults['data'][dateStat]

            if indivFavs['data'][dateStat] > indivFavs['height']:
                indivFavs['height'] = indivFavs['data'][dateStat]

            if cumulFavs['data'][dateStat] > cumulFavs['height']:
                cumulFavs['height'] = cumulFavs['data'][dateStat]

            dateTimeStat += datetime.timedelta(1)
            dateStat = dateTimeStat.date()

        indivConsults['height'] += 10 - (indivConsults['height'] % 10)
        cumulConsults['height'] += 10 - (cumulConsults['height'] % 10)
        indivFavs['height'] += 10 - (indivFavs['height'] % 10)
        cumulFavs['height'] += 10 - (cumulFavs['height'] % 10)
        
        context['title'] = "Statistiques de " + post.title
        context['consults'] = PostConsult.objects.filter(post=self.kwargs.get('pk'))
        context['favs'] = PostFavorite.objects.filter(post=self.kwargs.get('pk'))
        context['indivConsults'] = indivConsults
        context['cumulConsults'] = cumulConsults
        context['indivFavs'] = indivFavs
        context['cumulFavs'] = cumulFavs

        #yo = 0 / 0

        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    #success_url = '/'
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