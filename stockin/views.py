from ast import operator
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import StockinBasic, StockoutBasic, StockbackBasic, StockinDetail
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    CreateView,
    UpdateView,
    FormView
)
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from .forms import (
    StockinDetailFormset, 
    StockoutDetailFormset, 
    StockbackDetailFormset, 
    StockinConfirmForm,
    StockoutConfirmForm,
    StockbackConfirmForm
)

from django.http import FileResponse
import io
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .filters import StockinFilterSet, StockoutFilterSet, StockbackFilterSet

class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        queryset = super().get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context

class StockinPdfView(View):
    def get(self, request, *args, **kwargs):
        buf = io.BytesIO()
        elements = []

        obj = get_object_or_404(StockinBasic,pk=self.kwargs['pk'])

        pdfmetrics.registerFont(TTFont('SimSun', 'SimSun.ttf'))  #注册字体
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(fontName='SimSun', name='Song', leading=20, fontSize=12))  #自己增加新注册的字体
        styles.add(ParagraphStyle(fontName='SimSun', name='Song_title', leading=20, fontSize=14))  #自己增加新注册的字体
        style = styles['Title']
        style.fontName='SimSun'

        title = '入库清单'
        elements.append(Paragraph(title, style))
        basic_info = "单号：%s 日期：%s 操作员：%s" %(obj.code, obj.create_date, obj.operator)
        elements.append(Paragraph(basic_info, styles['Song']))
        elements.append(Paragraph('\n', styles['Song']))
        
        detail_data = []
        head = ['序号','品名','数量','单位','条码']
        detail_data.append(head)

        for i, d in enumerate(obj.details.all()):
            detail_data.append([i+1, d.item.name, d.amount, d.item.unit.name, d.list_barcodes()])

        pdf = SimpleDocTemplate(buf, rightMargin=72,
                            leftMargin=72, topMargin=72, bottomMargin=18)
        table_style = [
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONT', (0,0), (-1,-1), 'SimSun')
        ]
        report_table = Table(data=detail_data, style=table_style, hAlign="CENTER")
        elements.append(report_table)
        pdf.build(elements)

        pdf_name = "%s.pdf" % obj.code
        buf.seek(0)
        return FileResponse(buf, as_attachment=True, filename=pdf_name)

class StockoutPdfView(View):
    def get(self, request, *args, **kwargs):
        buf = io.BytesIO()
        elements = []

        obj = get_object_or_404(StockoutBasic,pk=self.kwargs['pk'])

        pdfmetrics.registerFont(TTFont('SimSun', 'SimSun.ttf'))  #注册字体
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(fontName='SimSun', name='Song', leading=20, fontSize=12))  #自己增加新注册的字体
        styles.add(ParagraphStyle(fontName='SimSun', name='Song_title', leading=20, fontSize=14))  #自己增加新注册的字体
        style = styles['Title']
        style.fontName='SimSun'

        title = '出库清单'
        elements.append(Paragraph(title, style))
        basic_info = "单号：%s 日期：%s 操作员：%s 领用人：%s" \
            %(obj.code, obj.create_date, obj.operator, obj.client)
        elements.append(Paragraph(basic_info, styles['Song']))
        elements.append(Paragraph('\n', styles['Song']))
        
        detail_data = []
        head = ['序号','品名','数量','单位','条码']
        detail_data.append(head)

        for i, d in enumerate(obj.details.all()):
            b = d.barcode
            detail_data.append([i+1, b.item.name, b.amount, b.item.unit.name, b.code])

        pdf = SimpleDocTemplate(buf, rightMargin=72,
                            leftMargin=72, topMargin=72, bottomMargin=18)
        table_style = [
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONT', (0,0), (-1,-1), 'SimSun')
        ]
        report_table = Table(data=detail_data, style=table_style, hAlign="CENTER")
        elements.append(report_table)
        pdf.build(elements)

        pdf_name = "%s.pdf" % obj.code
        buf.seek(0)
        return FileResponse(buf, as_attachment=True, filename=pdf_name)

class StockbackPdfView(View):
    def get(self, request, *args, **kwargs):
        buf = io.BytesIO()
        elements = []

        obj = get_object_or_404(StockbackBasic,pk=self.kwargs['pk'])

        pdfmetrics.registerFont(TTFont('SimSun', 'SimSun.ttf'))  #注册字体
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(fontName='SimSun', name='Song', leading=20, fontSize=12))  #自己增加新注册的字体
        styles.add(ParagraphStyle(fontName='SimSun', name='Song_title', leading=20, fontSize=14))  #自己增加新注册的字体
        style = styles['Title']
        style.fontName='SimSun'

        title = '返库清单'
        elements.append(Paragraph(title, style))
        basic_info = "单号：%s 日期：%s 操作员：%s 领用人：%s" \
            %(obj.code, obj.create_date, obj.operator, obj.client)
        elements.append(Paragraph(basic_info, styles['Song']))
        elements.append(Paragraph('\n', styles['Song']))
        
        detail_data = []
        head = ['序号','品名','数量','单位','条码']
        detail_data.append(head)

        for i, d in enumerate(obj.details.all()):
            b = d.barcode
            detail_data.append([i+1, b.item.name, b.amount, b.item.unit.name, b.code])

        pdf = SimpleDocTemplate(buf, rightMargin=72,
                            leftMargin=72, topMargin=72, bottomMargin=18)
        table_style = [
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONT', (0,0), (-1,-1), 'SimSun')
        ]
        report_table = Table(data=detail_data, style=table_style, hAlign="CENTER")
        elements.append(report_table)
        pdf.build(elements)

        pdf_name = "%s.pdf" % obj.code
        buf.seek(0)
        return FileResponse(buf, as_attachment=True, filename=pdf_name)



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
    paginate_by = 2

class StockinFilterListView(FilteredListView):
    queryset = StockinBasic.objects.all()
    filterset_class = StockinFilterSet
    paginate_by = 2
    template_name = 'stockin_list_filtered.html'

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
        for detail in self.object.details.all():
            detail.barcode.status = 1
            detail.barcode.save()


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
    fields = ['operator', 'client', 'memo']

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

class StockbackConfirmView(UpdateView):
    form_class = StockbackConfirmForm
    template_name = 'stock_confirm.html'
    queryset = StockbackBasic.objects.all()

    def form_valid(self, form):
        self.object.confirmed = True
        self.object.save()
        for detail in self.object.details.all():
            detail.barcode.status = 2
            detail.barcode.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'stockback were confirmed.'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('stock:stockback-info', kwargs={'pk': self.object.pk})
