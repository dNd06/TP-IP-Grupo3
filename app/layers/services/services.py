# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from ..transport import transport
from app.models import Favourite  # Asegúrate de importar el modelo

def getAllImages(input=None):
    # Obtiene un listado de datos "crudos" desde la API, usando a transport.py.
    json_collection = transport.getAllImages(input)

    # Recorre cada dato crudo de la colección anterior, lo convierte en una Card y lo agrega a images.
    images = []
    for elemento in json_collection:
        images.append(translator.fromRequestIntoCard(elemento))

    return images

# Añadir favoritos
def saveFavourite(request):
    from ..utilities.translator import fromTemplateIntoCard
    user = get_user(request)
    
    # Convertimos los datos del formulario en una Card.
    card = fromTemplateIntoCard(request)
    card.user = user  # Asignamos el usuario autenticado.

    # Guardamos la Card en la base de datos.
    result = repositories.saveFavourite(card)
    if result:
        print("Favorito guardado exitosamente.")
        return True
    else:
        print("No se pudo guardar el favorito.")
        return False

# Obtener todos los favoritos
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        # Obtenemos todos los favoritos del usuario desde la capa de repositorio.
        favourite_list = repositories.getAllFavourites(user)

        # Transformamos cada favorito en una Card para enviarlo a la plantilla.
        mapped_favourites = []
        for favourite in favourite_list:
            card = {
                'id': favourite['id'],
                'url': favourite['url'],
                'name': favourite['name'],
                'status': favourite['status'],
                'last_location': favourite['last_location'],
                'first_seen': favourite['first_seen']
            }
            mapped_favourites.append(card)

        return mapped_favourites

# Eliminar favorito
def deleteFavourite(request):
    fav_id = request.POST.get('id')  # Obtenemos el ID desde el formulario.

    try:
        # Validamos que el favorito pertenece al usuario logueado.
        user = get_user(request)
        favourite = Favourite.objects.get(id=fav_id, user=user)  # Filtramos por usuario y ID.

        favourite.delete()
        print("Favorito eliminado correctamente.")
        return True
    except Favourite.DoesNotExist:
        print(f"El favorito con ID {fav_id} no existe o no pertenece al usuario.")
        return False
    except Exception as e:
        print(f"Error al eliminar el favorito: {e}")
        return False

