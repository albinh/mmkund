from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout
from kunder.forms import EmailForm

from django.template import loader


def home(request):
    return HttpResponse("Hello, Django!"+request.user.username)

def my_deliveries(request):
    return HttpResponse("Hello, Django!"+request.user.username)

def login_customer(request):
    logout(request)

    if request.method == 'POST':
        form = EmailForm(request.POST)

        if form.is_valid():
            
            return HttpResponseRedirect('/kolla_epost.html')
    else:
        form = EmailForm()
    

    template = loader.get_template('kunder/login_customer.html')
    context = {'form':form}   

    return HttpResponse(template.render(context, request))
