from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django_filters.views import FilterView
from .models import Barcode, StockinBasic, StockoutBasic, StockbackBasic, StockinDetail
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    CreateView,
    UpdateView,
    FormView
)
from django.views.generic.detail import SingleObjectMixin
from .forms import (
    StockinDetailFormset, 
    StockoutDetailFormset, 
    StockbackDetailFormset, 
    StockinConfirmForm,
    StockoutConfirmForm
)

class StockinCreateView(CreateView):
    model = StockinBasic
    template_name = 'stockin_create.html'
    fields = ['operator', 'memo']

    def form_valid(self, form):

        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'The stockin has been added'
        )

        return super().form_valid(form)

class StockinDetailUpdateView(SingleObjectMixin, FormView):
    model = StockinBasic
    template_name = 'stockin_detail_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=StockinBasic.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=StockinBasic.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return StockinDetailFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('stock:stockin-info', kwargs={'pk': self.object.pk})


class StockinDetailView(DetailView):
    queryset = StockinBasic.objects.all()
    template_name = 'stockin_info.html'

class StockinDeleteView(DeleteView):
    queryset = StockinBasic.objects.all()
    template_name = 'stock_delete.html'

    def get_success_url(self):
        return reverse("stock:stockin-list")

class StockinListView(ListView):
    queryset = StockinBasic.objects.all()
    template_name = 'stockin_list.html'

# stockout
class StockoutCreateView(CreateView):
    model = StockoutBasic
    template_name = 'stockout_create.html'
    fields = ['operator', 'client', 'memo']

    def form_valid(self, form):

        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'The stockout has been added'
        )

        return super().form_valid(form)

class StockoutDetailUpdateView(SingleObjectMixin, FormView):
    model = StockoutBasic
    template_name = 'stockout_detail_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=StockoutBasic.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=StockoutBasic.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return StockoutDetailFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('stock:stockout-info', kwargs={'pk': self.object.pk})

class StockoutDetailView(DetailView):
    queryset = StockoutBasic.objects.all()
    template_name = 'stockout_info.html'

class StockoutDeleteView(DeleteView):
    queryset = StockoutBasic.objects.all()
    template_name = 'stock_delete.html'

    def get_success_url(self):
        return reverse("stock:stockout-list")

class StockoutConfirmView(UpdateView):
    form_class = StockoutConfirmForm
    template_name = 'stock_confirm.html'
    queryset = StockoutBasic.objects.all()

    def form_valid(self, form):
        self.object.confirmed = True
        self.object.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'stockout were confirmed.'
        )

        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        return reverse('stock:stockout-info', kwargs={'pk': self.object.pk})


class StockoutListView(ListView):
    queryset = StockoutBasic.objects.all()
    template_name = 'stockout_list.html'

# stockback
class StockbackCreateView(CreateView):
    model = StockbackBasic
    template_name = 'stockback_create.html'
    fields = ['code', 'operator', 'client', 'memo']

    def form_valid(self, form):

        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'The stockback has been added'
        )

        return super().form_valid(form)

class StockbackDetailUpdateView(SingleObjectMixin, FormView):
    model = StockbackBasic
    template_name = 'stockback_detail_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=StockbackBasic.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=StockbackBasic.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return StockbackDetailFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('stock:stockback-info', kwargs={'pk': self.object.pk})

class StockbackDetailView(DetailView):
    queryset = StockbackBasic.objects.all()
    template_name = 'stockback_info.html'

class StockbackDeleteView(DeleteView):
    queryset = StockbackBasic.objects.all()
    template_name = 'stock_delete.html'

    def get_success_url(self):
        return reverse("stock:stockback-list")

class StockbackListView(ListView):
    queryset = StockbackBasic.objects.all()
    template_name = 'stockback_list.html'

class StockinConfirmView(UpdateView):
    form_class = StockinConfirmForm
    template_name = 'stock_confirm.html'
    queryset = StockinBasic.objects.all()

    def form_valid(self, form):
        self.object.confirmed = True
        self.object.save()
        # form.save()
        for detail in self.object.details.all():
            detail.gen_barcode()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Barcodes were saved.'
        )

        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        return reverse('stock:stockin-info', kwargs={'pk': self.object.pk})


