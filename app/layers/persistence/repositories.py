# capa DAO de acceso/persistencia de datos.

from app.models import Favourite

def saveFavourite(image):
    try:
        # Verificamos si ya existe un favorito con los mismos datos para este usuario.
        existing = Favourite.objects.filter(
            user=image.user,
            url=image.url,
            name=image.name,
            status=image.status,
            last_location=image.last_location,
            first_seen=image.first_seen
        ).exists()

        if existing:
            print("El favorito ya existe, no se guarda duplicado.")
            return None  # O algún indicador de que no fue necesario guardar.

        # Si no existe, lo creamos.
        fav = Favourite.objects.create(
            url=image.url,
            name=image.name,
            status=image.status,
            last_location=image.last_location,
            first_seen=image.first_seen,
            user=image.user
        )
        return fav
    except Exception as e:
        print(f"Error al guardar el favorito: {e}")
        return None

def getAllFavourites(user):
    # Filtra los favoritos por usuario y devuelve los datos necesarios.
    favourite_list = Favourite.objects.filter(user=user).values(
        'id', 'url', 'name', 'status', 'last_location', 'first_seen'
    )
    return list(favourite_list)


def deleteFavourite(id):
    try:
        favourite = Favourite.objects.get(id=id)
        favourite.delete()
        return True
    except Favourite.DoesNotExist:
        print(f"El favorito con ID {id} no existe.")
        return False
    except Exception as e:
        print(f"Error al eliminar el favorito: {e}")
        return False