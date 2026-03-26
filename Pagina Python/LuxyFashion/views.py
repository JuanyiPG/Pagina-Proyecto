from django.shortcuts import render


def index (request): 
    return render(request, 'index.html')

def productos(request):
    return render(request, 'PAGINAS_LUXY_PROD/PAGINA_PROD.html')
