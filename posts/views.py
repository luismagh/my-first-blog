from urllib.parse import quote_plus #v30 para incluir boton redes sociales transforma cualquier cadena de texto en
#una cadena que puede compartirse
from django.contrib import messages #añado esta para el video 22 y mensajes flash de "bien editado" o similar
from django.shortcuts import render, get_object_or_404, redirect #añado el get_object para el video 17
#añado el redirect para el v23 y poder ir al listado general tras borrar en el "return"
from django.http import HttpResponse, HttpResponseRedirect, Http404 #añado esto para gestionar las peticiones de pag web a django
#añado el HttpRespondeRedirect solo para la opción de update del video 21, Http404 del v32
from django.utils import timezone #v36 para el filtro de queryset_list por la fecha actual
from django.db.models import Q #v37 búsquedas complejas

# Create your views here.

from .models import Post #esto lo añado en el video 16 para aplicar ya QuerySet.
from .forms import PostForm #esto v20 donde utilizo formularios
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator #v27 paginacion

#def post_home(request):
    #return HttpResponse("<h1>Hello</h1>")

#a partir del video 12 quitamos las dos lineas de arriba de prueba y definimos vistas para
# el método CRUD (incluyendo List también)

def post_create(request): #create #realmente lo edito desde v20
    #form = PostForm() #indico el formulario que se usa. La clase PostForm definida en forms.py
    #if request.method == "POST": #si el metodo de request (la variable que recibe post_create) es un POST...
    #    print (request.POST) #imprime en el terminal ese valor
    #lo de arriba era el ejemplo del video 20 primera parte... pero lo que sigue es lo que realmente debe quedar.
    if not request.user.is_staff or not request.user.is_superuser: #v32 para definir quienes pueden crear/ editar post en el blog
        raise Http404 #v32
    form = PostForm(request.POST or None, request.FILES or None) #para que sea obligatorio que haya contenidos en los campos,
    #  y con request.FILES para el v28 añado que ese conenido sean ficheros
    if form.is_valid():
        instance = form.save(commit=False) # save es el metodo de form para guardar los datos, pero al poner
        # commit=False, aún no lo estoy llevando a la base de datos, por si quiero hacerle algun cambio o si quiero
        #guardarlo de otra manera diferente... en este caso de momento lo grabo justo después con otro save().
        instance.user = request.user #v33 para incluir al usuario en el formulario
        instance.save()
        messages.success(request,"Successfully Created") #del v22 para generar mensaje de confirmacion.
        return HttpResponseRedirect(instance.get_absolute_url())  # lo añado en el video 21 cuando hago update. Es para
        # que tras crear el post me lleve a mostrármelo directamente.
    else: #del v22 para cuando no hay exito creando que genere mensaje
        messages.error(request, "Not Successfully Created") #del v22 para que cuando no hay exito creando genere mensaje

    context = {
        "form":form,
    }
    return render(request, "post_form.html", context)

#def post_detail(request, id=None): #retrieve. #en el video 18 añado id=None,antes no estaba
def post_detail(request, slug=None): #v29 cambio el id por el slug
    # return HttpResponse("<h1>Detail</h1>") antes del video 15 (meter context y template)
    #instance = get_object_or_404(Post,id=2) #añado para el video 17
    # instance = get_object_or_404(Post, id=id) #ahora para el video 18 lo dejo así.
    instance = get_object_or_404(Post, slug=slug) #v29 cambio id por slug
    if instance.draft or instance.publish > timezone.now().date(): #v36 para definir quienes ven un draft o fecha publicacion futura
        if not request.user.is_staff or not request.user.is_superuser: #v36 para definir quienes ven un draft o fecha publicacion futura
            raise Http404
    share_string = quote_plus(instance.content) #v30 compartir redes sociales.
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string" : share_string, #v30 redes sociales

    }
    #return render(request, "index.html", context) #en el video 17 dejo de usar index y uso una web concreta para cada post
    return render(request, "post_detail.html", context) #esta html es la que uso desde el video 17 para los posts

def post_list(request): #list items
    today = timezone.now().date() #v36 para operar con fecha de ublicación también en la post_list.html
    # return HttpResponse("<h1>List</h1>") #antes de video 14 con templates
    # return render(request, "index.html",{}) #antes del video 15 con contexto
    # queryset_list = Post.objects.all() #.order_by("-timestamp") #añado en video 16 sobre QuerySet #añado el order_by en el v27
    # y lo quito en el v36. también arriba cambio el nombre a queryset_list en el v27 pero no explica por qué. Lo quité al inicio del
    #v36 poniendo lo de abajo, pero despues de definir el Model Manager para all() lo vuelvo a colocar.
    #queryset_list = Post.objects.filter(draft=False).filter(publish__lte=timezone.now()) #v36 ahora filtro lo que aparece en la lista de artículos
    # con el filtro de que la fecha de publicación sea "lest than or equal to" la fecha actual y no sea draft
    #esto de abajo es para la paginación y se añade en el v27
    queryset_list = Post.objects.active() #v36 al final cambio all() por active() para evitar confusión
    if request.user.is_staff or request.user.is_superuser: #v36 si soy staff o superusuario uso el all() sin filtro
        queryset_list = Post.objects.all()
    query = request.GET.get('q') #v37 archiva el contenido de la búsqueda de artículo.
    if query: #v37 si hay búsqueda activo un filtro de lo que mostrará la función post_list
        # queryset_list = queryset_list.filter(title__icontains=query) #v37 filtro aplicado por búsqueda
        queryset_list = queryset_list.filter( #v37 nueva búsqueda usando Q objetcs "|" es el "or"
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)).distinct()  #v37 distinct es para que no duplique resultados
    paginator = Paginator(queryset_list, 3)  # v27 lo adapto usando queryset_list y 3 por pagina
    page_request_var = "page" #v27 al final lo añado para incluirlo en context (ver apuntes)
    page = request.GET.get(page_request_var)  #antes de la expresion de arriba era page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger: #if page is not an integer deliver first page
        queryset = paginator.page(1)
    except EmptyPage: #if page is out of range, deliver last page
        queryset = paginator.page(paginator.num_pages) #v27 en lugar de contact pongo queryset (aquí se mantiene sin list como en el context
    #hasta aquí el añadido de paginación

    context = {         # se añade para el video 15 de contexto
        "object_list": queryset,  #esta linea es por el video 16 sobre Queryset
        "title":"List",
        "page_request_var": page_request_var,
        "today": today, #v36 envío el día de hoy a la web para trabajar con la fecha de publicación
    }
    # return render(request, "index.html", context)
    # return render(request, "base.html", context) #en V24 cambio index.html por base.html para siempre.
    return render(request, "post_list.html", context) #de nuevo en V24 creo post_list y quito base.html


#def post_update(request, id=None): #update #en el video 21 actualizo esta función
def post_update(request, slug=None): #v29 cambio id por slug
    if not request.user.is_staff or not request.user.is_superuser: #v32 para definir quienes pueden crear/ editar post en el blog
        raise Http404 #v32
     #instance = get_object_or_404(Post, id=id) #utilizo como en post_detail para obtener la info anterior
    instance = get_object_or_404(Post, slug=slug) #v29 cambio el id por slug
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)  # idem como post_create para poder actualizarla,
    # el atributo "instance" da acceso a ese específica instancia, en este caso, al get_object_or_404, lo que
    # me permite esta vez ver el contenido del post en el mismo formulario cuando voy a editarlo
    # el atributo request.FILES se añade en el v28 para poder cargar imágenes.
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Updated")  # del v22 para generar mensaje de confirmacion.
        return HttpResponseRedirect(instance.get_absolute_url()) #con esto tras editar vuelve a mostrar el post ya editado
        #entre parentesis va la dirección a la que debe volver, usamos el get_absolute_url que definimos en models.py
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context) #uso el mismo html que en el formulario

#def post_delete(request): #delete al principio.. estas dos lineas... en el v23 lo transformo en la versión definitiva
    #return HttpResponse("<h1>Delete</h1>")

#def post_delete(request, id=None): #lo realizo en el v23
def post_delete(request, slug=None): #v29 cambio el id por slug
    if not request.user.is_staff or not request.user.is_superuser: #v32 para definir quienes pueden crear/ editar post en el blog
        raise Http404 #v32
    #instance = get_object_or_404(Post, id=id) #aquí cargo la instancia (entrada del blog)
    instance = get_object_or_404(Post, slug=slug) #v29 cambio el id por slug
    instance.delete() #con esto borro la instancia cargada
    messages.success(request, "Successfully Deleted")  # del v22 para generar mensaje de confirmacion lo aplico aqui
    return redirect("posts:list") #uso redirect para volver a una pagina que quiero (la lista de entradas)

