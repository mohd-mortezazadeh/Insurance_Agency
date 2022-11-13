from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse_lazy
from django.views.generic import ListView,UpdateView
from django.views.generic.edit import  DeleteView
from users.forms import ProfileForm
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.views.generic.edit import FormView
from .forms import GenerateRandomUserForm
from django.contrib.auth.views import PasswordChangeView
from .tasks import create_random_user_accounts
User = get_user_model()





@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class UserListView(ListView):

    model = get_user_model()
    template_name="dashboard/user/list.html"
    context_object_name = 'users'
    paginate_by = 10



class DeleteUserView(SuccessMessageMixin,PermissionRequiredMixin, DeleteView):
    permission_required = "user.delete_user"
    model = User
    template_name = 'dashboard/user/list.html'
    success_url = reverse_lazy('user:list')
    success_message = "user Delete successfully"

    def handle_no_permission(self):
        messages.warning(self.request, "You dont have permission to this page please signin with superuser!")
        return redirect("dashboard:home")

    def get(self, request, *args, **kwargs):
        pk=kwargs.get("pk")
        if pk is not None:
            post_object = User.objects.get_queryset().filter(pk= pk)
            if post_object is not None:
                post_object.delete()
                messages.success(request, 'User was deleted successfully.') 
                return redirect('user:list')
        return redirect('dashboard/user/list.html')
    


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileView(View, PermissionRequiredMixin):
    permission_required = "user.create_user"
    profile = None
    # notification format in create.html
    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile'}
        return render(request, 'dashboard/user/create.html', context)

    def post(self, request):
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=self.profile)
            if form.is_valid():
                profile = form.save()
                profile.user.first_name = form.cleaned_data.get('first_name')
                profile.user.last_name = form.cleaned_data.get('last_name')
                profile.user.email = form.cleaned_data.get('email')
                profile.user.save()

                messages.success(request, 'Profile saved successfully')
                return redirect('user:list')
            else:
                return render(request,'dashboard/user/create.html', {"form":form, })
            
        else:
            form = ProfileForm(request.FILES,)
        return redirect('user:list')
            




@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileUpdateView(SuccessMessageMixin,LoginRequiredMixin, UpdateView):

    form_class = ProfileForm
    model = User
    template_name= 'frontend/accounts/profile.html'
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        user = form.save(commit = False)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.profile.phone = form.cleaned_data['phone']
        user.profile.code = form.cleaned_data['code']
        user.profile.address = form.cleaned_data['address']
        user.profile.city = form.cleaned_data['city']
        user.profile.zip = form.cleaned_data['zip']
        user.profile.avatar = form.cleaned_data['avatar']
        user.save()
        messages.success(self.request, 'پروفایل با موفقیت آپدیت شد!')
        return redirect('user:update_profile', pk=user.pk,)
        


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'frontend/accounts/password_change.html'
    success_message = "پسوردتان با موفقیت تغیرر یافت"
    success_url = reverse_lazy('user:password_change')



class GenerateRandomUserView(FormView):
    template_name = 'dashboard/user/generate_random_users.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delay(total)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return redirect('user:list')

