from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CriteriaForm
from .models import Notification

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now log in!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def criteria(request):
    if request.method == 'POST':
        c_form = CriteriaForm(request.POST, instance=request.user.criteria)

        if c_form.is_valid():
            c_form.save()

            messages.success(request, f'Vos critères on été mis à jour!')
            return redirect('blog-home')
    else:
        c_form = CriteriaForm(instance=request.user.criteria)

    context = {
        'c_form': c_form
    }

    return render(request, 'users/criteria.html', context)

def notif_read(request):
    notif = Notification.objects.filter(id=request.GET.get('notifid', None)).first()

    notif.read = True
    notif.save()

    return JsonResponse({})

class NotficationsView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'users/notifs.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'notifs'
    ordering = ['-date_recieved']
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-date_recieved')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        notif_count = self.get_queryset().filter(read=False).count()

        if notif_count > 0:
            messages.warning(self.request, f'Vous avez {notif_count} nouvelle(s) notification(s) !')

        context['title'] = 'Notifications'
        return context