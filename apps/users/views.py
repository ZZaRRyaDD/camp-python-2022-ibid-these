from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from apps.lots.models import Bid

from . import forms, models


class RegistrationView(CreateView):
    """View for user registration."""

    template_name = "users/registration.html"
    form_class = forms.RegistrationForm
    success_url = reverse_lazy("users:login")


class UserDetailView(LoginRequiredMixin, DetailView):
    """View for user page with its lots and bids."""

    model = models.User
    template_name = "users/user_detail.html"
    context_object_name = "user"
    queryset = models.User.objects.prefetch_related(
        "lot__images",
        Prefetch(
            "bids",
            Bid.objects.order_by("-created").prefetch_related(
                Prefetch(
                    "lot__bids",
                    Bid.objects.order_by("-created"),
                ),
            ),
        ),
    )

    def get_context_data(self, **kwargs):
        """Get context for page."""
        context = super().get_context_data(**kwargs)
        context["lots"] = self.object.lot
        if self.request.user == self.object:
            context["bids"] = self.object.bids
        return context


class UserEditView(LoginRequiredMixin, UpdateView):
    """View for editing user information."""

    template_name = "users/profile_edit.html"
    form_class = forms.UserEditForm
    success_url = reverse_lazy("users:login")

    def get_object(self, queryset=None):
        """Get user object from request."""
        return self.request.user
