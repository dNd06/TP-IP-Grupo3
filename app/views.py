# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from app.layers.transport import transport
from django.contrib import messages

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    images = services.getAllImages(None)
    
    # Extraemos solo las URLs de los favoritos
    favourite_list = [favourite['url'] for favourite in services.getAllFavourites(request)]

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })


def search(request):
    search_msg = request.POST.get('query', '')

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):
        resultados = services.getAllImages(search_msg)
        return render(request, 'home.html', {'images': resultados})
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    # Llamamos a la capa de servicios para obtener los favoritos del usuario.
    favourite_list = services.getAllFavourites(request)
    
    # Renderizamos la plantilla con la lista de favoritos.
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    if request.method == 'POST':
        success = services.saveFavourite(request)
        if success:
            messages.success(request, "Favorito añadido correctamente.")
        else:
            messages.error(request, "El favorito ya existe o no pudo guardarse.")
        return redirect('home')
@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        success = services.deleteFavourite(request)
        if success:
            messages.success(request, "Favorito eliminado correctamente.")
        else:
            messages.error(request, "No se pudo eliminar el favorito.")
        return redirect('favoritos')


@login_required
def exit(request):
    logout(request)
    return redirect('exit')