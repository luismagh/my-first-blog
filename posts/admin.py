from django.contrib import admin

# Register your models here.

from .models import Post #importo la clase Post desde models

# estas líneas ahora son del video 8 para customizar el admin.
#defino una clase nueva que usa la función admin.ModelAdmin para cambiar el aspecto del admin.:
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title","updated","timestamp"] #explicación en 8/38. Añade campos a la
    #info que aparece en la pantalla de administración de las entradas de Post
    list_display_links = ["updated"] #aqui paso la posibilidad de que sea link a este campo en lugar de al nombre
    # esto me permite con lo de abajo poder editar el nombre.
    list_editable = ["title"] #aquí pongo campos que puedo editar desde el administrador de posts.
    list_filter = ["updated","timestamp"] #aqui defino filtros a la derecha para buscar posts por estos campos.
    search_fields = ["title","content"] #añade una zona de búsqueda donde podré buscar dentro de estos campos.
    class Meta: #la clase Meta la uso aquí para definir que el model que uso es Post y no el que se define por defecto
    #para Model.Admin que es el "admin". Así los cambios se aplican al modelo de Post y no al original de admin
        model = Post


#esta linea sigue siendo para cuando registro la clase Post en el admin site
admin.site.register(Post, PostModelAdmin) #registro el modulo Post en nuestro admin site. La opción PostModelAdmin
# solo la he añadido cuando he creado arriba la clase PostModelAdmin para poder variar el
# aspecto del administrador.