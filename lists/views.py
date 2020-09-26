from django.shortcuts import render


def home_page(http_request):
    return render(http_request, 'lists/home.html')
