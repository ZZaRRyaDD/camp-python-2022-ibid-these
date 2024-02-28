from typing import Any, Optional

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q, QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View, generic

from apps.lots import forms

from . import models


class FavoritesLotActionView(LoginRequiredMixin, generic.edit.FormMixin, View):
    """Actions with favorite lots."""

    def get_success_url(self):
        """Get url to lot detail page after add lot in favorites."""
        return reverse("lots:details", kwargs={"pk": self.kwargs["pk"]})

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        """Handle POST requests.

        After request, lot remove or add (depending on the previous state)
        from set of favorite lots of user.
        """
        lot = get_object_or_404(models.Lot, id=self.kwargs["pk"])
        if lot in self.request.user.favorite_lots.all():
            self.request.user.favorite_lots.remove(lot)
        else:
            self.request.user.favorite_lots.add(lot)
        return redirect(self.get_success_url())


class BaseLotListView(generic.list.ListView):
    """BaseList view for Lots."""

    paginate_by = 8
    context_object_name = "lots"
    queryset = models.Lot.objects.exclude(status=models.Lot.Status.DRAFT)
    ordering_fields = [
        "start_price",
        "name",
    ]

    def get_context_data(self, **kwargs) -> dict:
        """Get categories list."""
        data = super().get_context_data(**kwargs)
        data["categories"] = models.Category.objects.all()
        return data

    def search_queryset(self, object_list) -> QuerySet:
        """Get queryset with search query."""
        query_search = self.request.GET.get("search")
        if query_search:
            return object_list.filter(
                    Q(name__icontains=query_search) |
                    Q(description__icontains=query_search),
            )
        return object_list

    def order_queryset(self, object_list) -> QuerySet:
        """Get ordered queryset."""
        query_order = self.request.GET.get("order")
        if query_order:
            field = self.get_ordering()
            if field:
                return object_list.order_by(field)
        return object_list

    def filter_queryset_category(self, object_list) -> QuerySet:
        """Get filtered queryset."""
        query_filter = self.request.GET.get("category")
        if query_filter:
            category_name = get_object_or_404(
                models.Category,
                name=query_filter,
            )
            return object_list.filter(category=category_name)
        return object_list

    def filter_queryset_status(self, object_list) -> QuerySet:
        """Get filtered queryset."""
        query_filter = self.request.GET.get("status")
        if query_filter:
            return object_list.filter(status=query_filter)
        return object_list

    def get_ordering(self) -> Optional[str]:
        """Get key for ordering queryset."""
        query_order = self.request.GET.get("order")
        if query_order.lstrip("-") in self.ordering_fields:
            return query_order
        return None

    def get_queryset(self) -> QuerySet:   # pylint: disable=arguments-differ
        """Get search result."""
        object_list = self.queryset
        object_list = self.search_queryset(object_list)
        object_list = self.order_queryset(object_list)
        object_list = self.filter_queryset_category(object_list)
        object_list = self.filter_queryset_status(object_list)
        return object_list


class LotListView(BaseLotListView):
    """List view for Lots."""

    template_name = "lots/list_lots.html"


class FavoritesLotsView(LoginRequiredMixin, BaseLotListView):
    """List view for favorites Lots of current user."""

    template_name = "lots/favorites_lots.html"

    def get_queryset(self) -> QuerySet:  # pylint: disable=arguments-differ
        """Get favorites lots of user."""
        return super().get_queryset().filter(
            id__in=self.request.user.favorite_lots.values("id"),
        )


class UpdateLotView(PermissionRequiredMixin, generic.edit.UpdateView):
    """View for Lot update."""

    template_name = "lots/lot_update_form.html"
    form_class = forms.LotCreateForm
    model = models.Lot
    queryset = models.Lot.objects.all()

    def get_success_url(self) -> str:
        """Get url to lot detail page after bid creation."""
        return reverse_lazy(
            "lots:details",
            kwargs={"pk": self.get_object().pk},
        )

    def has_permission(self) -> bool:
        """Only owner can edit lot."""
        return all([
            self.request.user.id == self.get_object().user.id,
            self.get_object().status == "DRAFT",
        ])

    def get_context_data(self, **kwargs):
        """Get context for page."""
        self.object = (  # pylint: disable=attribute-defined-outside-init
            self.get_object()
        )
        context = super().get_context_data(**kwargs)
        context["form"].fields["status"].choices = [
            ("IN_PROCCESS", _("In Proccess")),
            ("DRAFT", _("Draft")),
        ]
        context["lot_images_formset"] = forms.ImageLotFormSet(
            instance=self.object,
        )
        return context

    def post(self, request, *args, **kwargs):
        """Handle POST requests."""
        form = forms.LotCreateForm(
            request.POST,
            instance=self.get_object(),
        )
        lot_images_formset = forms.ImageLotFormSet(
            request.POST,
            request.FILES,
            instance=self.get_object(),
        )
        if form.is_valid() and lot_images_formset.is_valid():
            return self.form_valid(form, lot_images_formset)
        return self.form_invalid(form, lot_images_formset)

    def form_valid(
        self,
        form,
        lot_images_formset,
    ):  # pylint: disable=arguments-differ
        """Overridden for save form and formset when update lot."""
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        lot_images_formset.instance = obj
        lot_images_formset.save()
        return redirect(self.get_success_url())

    def form_invalid(
        self,
        form,
        lot_images_formset,
    ):  # pylint: disable=arguments-differ
        """Overridden for reload context for retry update load."""
        return self.render_to_response(
            self.get_context_data(
                form=form,
                lot_images_formset=lot_images_formset,
            ),
        )


class CreateLotView(PermissionRequiredMixin, generic.edit.FormView):
    """View for Lot create."""

    template_name = "lots/lot_create_form.html"
    form_class = forms.LotCreateForm

    def get_success_url(self) -> str:
        """Get url to lot detail page after bid creation."""
        return reverse_lazy("lots:details", kwargs={"pk": self.object.pk})

    def has_permission(self) -> bool:
        """Only owner can edit lot."""
        return self.request.user.can_create_lots

    def get_context_data(self, **kwargs):
        """Get context for page."""
        context = super().get_context_data(**kwargs)
        context["form"].fields["status"].choices = [
            ("IN_PROCCESS", _("In Proccess")),
            ("DRAFT", _("Draft")),
        ]
        context["lot_images_formset"] = forms.ImageLotFormSet()
        return context

    def post(self, request, *args, **kwargs):
        """Handle POST requests."""
        self.object = None  # pylint: disable=attribute-defined-outside-init
        form = self.get_form()
        lot_images_formset = forms.ImageLotFormSet(
            data=request.POST,
            files=request.FILES,
        )
        if form.is_valid() and lot_images_formset.is_valid():
            return self.form_valid(form, lot_images_formset)
        return self.form_invalid(form, lot_images_formset)

    def form_valid(
        self,
        form,
        lot_images_formset,
    ):  # pylint: disable=arguments-differ
        """Overridden for save form and formset when creating lot."""
        self.object = (  # pylint: disable=attribute-defined-outside-init
            form.save(commit=False)
        )
        self.object.user = self.request.user
        self.object.save()
        lot_images_formset.instance = self.object
        lot_images_formset.save()
        return redirect(self.get_success_url())

    def form_invalid(
        self,
        form,
        lot_images_formset,
    ):  # pylint: disable=arguments-differ
        """Overridden for reload context for retry create load."""
        return self.render_to_response(
            self.get_context_data(
                form=form,
                lot_images_formset=lot_images_formset,
            ),
        )


class DetailLotView(
    PermissionRequiredMixin,
    generic.DetailView,
    generic.edit.FormMixin,
):
    """View for Lot details."""

    model = models.Lot
    template_name = "lots/lot.html"
    context_object_name = "lot"
    form_class = forms.BidCreateForm

    def has_permission(self) -> bool:
        """Solve, get user special permissions or not."""
        obj = self.get_object()
        return any([
            obj.status != "DRAFT",
            self.request.user == obj.user,
        ])

    def handle_no_permission(self) -> HttpResponseRedirect:
        """Method call if user has no permissions."""
        return redirect("lots:list")

    def get_success_url(self):
        """Get url to lot detail page after bid creation."""
        return reverse("lots:details", kwargs={"pk": self.get_object().pk})

    def get_form_kwargs(self) -> dict[str, Any]:
        """Method for get kwargs in form."""
        kwargs = super().get_form_kwargs()
        kwargs["lot"] = self.object
        return kwargs

    def form_valid(self, form) -> HttpResponse:
        """Method for save object with form data."""
        bid = form.save(commit=False)
        bid.user = self.request.user
        bid.lot = self.object
        bid.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Handle POST requests."""
        self.object = self.get_object()  # pylint: disable=W0201
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)
