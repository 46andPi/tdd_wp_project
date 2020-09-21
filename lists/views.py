from django.http import HttpResponse


def home_page(http_request):
    return HttpResponse('<html><title>To-Do lists</title></html>')
