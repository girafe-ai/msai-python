from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView

from leads.forms import LeadForm
from leads.models import Lead


# function-based view
#
# def index(request):
#     if request.method == 'GET':
#         return render(request, 'index.html')
#     else:
#         return HttpResponse(status=405)


# class-based view
#
# class IndexView(View):
#     def get(self, request):
#         return render(request, 'index.html')


# generic view
#
# class IndexView(TemplateView):
#     template_name = 'index.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs['time'] = str(datetime.now())
#         return kwargs


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        form = LeadForm(request.POST)
        if form.is_valid():
            print(form.data)
            Lead.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'].lower()
            )
            return render(request, 'index.html', context={'message': 'Success!'})
        else:
            print(form.errors)
            return render(request, 'index.html', context={'message': 'Data is incorrect'})


class LeadsView(TemplateView):
    template_name = 'leads.html'

    def get_context_data(self, **kwargs):
        kwargs['leads'] = Lead.objects.all()
        return kwargs
