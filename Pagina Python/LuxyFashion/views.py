from django.shortcuts import render


def index (request): 
    return render(request, 'index.html')

def productos(request):
    return render(request, 'PAGINAS_LUXY_PROD/PAGINA_PROD.html')

def error_404(request, exception):
    return render(request, 'error/404.html', status=404)

def error_500(request):
    return render(request, 'error/500.html', status=500)