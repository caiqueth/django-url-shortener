import json

from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse

from urlshortener.services import url_generator
from urlshortener.models import UrlRegister

from django.contrib import messages

def index(request):
    return TemplateResponse(request, template="home.html")

def new(request):

    if request.method != "POST":
        return HttpResponse(status=400)
    
    original_url = request.POST.get("original_url")
    url = url_generator(original_url, url_root=request.META["HTTP_ORIGIN"])

    return TemplateResponse(request, template="success.html", context={
        "url": url,
    })

def redirect(request, hash_url: str) -> HttpResponse:
    if request.method != "GET":
        return HttpResponse(status=400)

    url_to_redirect = UrlRegister.objects.filter(new_url__contains=hash_url)
    if not url_to_redirect:
        messages.add_message(request, messages.ERROR, 'Sorry, URL not found!')
        return HttpResponseRedirect("/")

    url_to_redirect = url_to_redirect[0].original_url
    if not url_to_redirect.startswith(("http://", "https://")):
        url_to_redirect = "https://" + url_to_redirect

    return HttpResponseRedirect(url_to_redirect)
