from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save #v29 slug. Permite un pre-guardado del post
from django.utils.text import slugify #v20 para generar slugs
from django.conf import settings #v33 para foreign key
from django.utils import timezone #v36 para usar timezone.now en el filtro de fecha de publicación
# Create your models here.
# Es una metodología MVC MODEL VIEW CONTROLLER


class PostManager(models.Manager): #v36 uso models.Manager para definir filtros de draft y fecha publicación
    #def all(self,*args,**kwargs): #v36 defino esta función que va a sobreescribir la función all() que hemos
        # usado hasta ahora por ejemplo en Post.objects.all() y abajo le añado el filtro que quiero.
    def active(self, *args, **kwargs): # al final del v36 cambio el nombre de all() a active.
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now()) #super llama al original all en este caso

def upload_location(instance, filename): #v28 al final para ordenar en carpetas los archivos
    return "%s/%s" %(instance.id, filename)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1) #V33 Foreign Key con el default estoy diciendo que por
    #defecto tendremos al usuario 1 que es el superadmin. Ayuda también para que los post creados hasta la fecha se muestren bien
    title = models.CharField(max_length=120) #título definiendo long máxima
    slug = models.SlugField(unique=True) #v29 creando slugs. por ser unique=True tengo que eliminar la base de datos
    # image = models.FileField(null=True, blank=True) #v28 campo de imagen, la opción null y blank es para permitir que esté vacio
    image = models.ImageField(upload_to=upload_location, #v28 al final cuando creo esta funcion para ordenar donde van los archivos
                              null=True, blank=True,
                              height_field="height_field",
                              width_field="width_field" ) #v28 al final uso ImageField en lugar de FileField
    height_field = models.IntegerField(default=0) #v28 al final
    width_field = models.IntegerField(default=0) #v28 al final

    content = models.TextField()
    draft = models.BooleanField(default=False) #v35 borradores y fecha publicación
    publish = models.DateField(auto_now=False, auto_now_add=False) #v35 borradores y fecha publicacion
    updated = models.DateTimeField(auto_now=True, auto_now_add= False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add= True)
    # auto_now = True hace que cada vez que se actualiza en la base de datos, se marca el valor
    # auto_now_add = True hace que se actualice el valor sólo una vez, por eso tiene sentido
    # para la variable de fecha de creación.


    objects = PostManager() #v36 actualizo el "objects" con PostManager para así que tenga la nueva all() que hemos definido

    def __str__(self):
        return self.title

    def get_absolute_url(self): #esto para v19 con las urls absolutas
        #return reverse("posts:detail", kwargs={"id":self.id})
        return reverse("posts:detail", kwargs={"slug": self.slug}) #v29 cambio introduciendo las páginas con slug

def create_slug(instance, new_slug=None): #v29 chequea si se ha creado el slug y si no se crea.
    slug= slugify(instance.title) #v29 slugify el titulo. convierte un título como "una historia" en un slug "una-historia"
    if new_slug is not None:  #v29 si el nuevo slug no está vacio (igual a "none")
        slug = new_slug #v29 el slug será ese nuevo slug.
    qs = Post.objects.filter(slug=slug).order_by("-id") #v29 si estaba vacío el new_slug, entonces con esta linea y la
    #siguiente chequeo si existe el slug que se ha creado.
    exists = qs.exists()
    if exists: #v29 si existe añado el id a uno nuevo para que sea diferente
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug #v29 si no existe antes, ese será el slug definitivo que devuelva



def pre_save_post_receiver(sender, instance, *args, **kwargs): #v29 *args y *kwargs es por si se reciben más de dos argumentos
    if not instance.slug: #v29 si no tenemos slug todavía... activamos la función create_slug
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post) #uso aquí la función con pre_save con la que se activará la función
#pre_save_post_receiver siempre antes de que vaya a grabar.


