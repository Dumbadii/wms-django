from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from extra_views import CreateWithInlinesView, ModelFormSetView, UpdateWithInlinesView, InlineFormSetFactory
from .models import StockinBasic, StockinDetail, Barcode
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    CreateView,
    FormView
)
from django.views.generic.detail import SingleObjectMixin
from .forms import StockinDetailFormset

# Create your views here.
class StockinDetailInline(InlineFormSetFactory):
    model = StockinDetail
    fields = ['item', 'barcode_count', 'amount', 'price']

class StockinCreateView(CreateView):
    model = StockinBasic
    template_name = 'stockin_create.html'
    fields = ['code', 'operator', 'memo']

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
        return reverse('stockin:stockin-info', kwargs={'pk': self.object.pk})


class StockinDetailView(DetailView):
    queryset = StockinBasic.objects.all()
    template_name = 'stockin_info.html'

class StockinDeleteView(DeleteView):
    queryset = StockinBasic.objects.all()
    template_name = 'stockin_delete.html'

    def get_success_url(self):
        return reverse("stockin:stockin-list")

class StockinListView(ListView):
    queryset = StockinBasic.objects.all()
    template_name = 'stockin_list.html'