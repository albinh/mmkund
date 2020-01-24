from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, Django!"+request.user.username)
