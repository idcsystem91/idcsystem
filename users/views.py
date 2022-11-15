from django.views.generic.edit import CreateView, UpdateView
from .forms import ProfileForm
from .models import Profile
from django.urls import reverse_lazy


class ProfileCreateView(CreateView):
    template_name = 'users/profile_form.html'
    form_class = ProfileForm
    success_url = reverse_lazy('')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        return initial


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'users/profile_form.html'
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        return initial
