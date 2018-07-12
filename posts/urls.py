from django.conf.urls import url
from django.contrib import admin

from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
) #añadido para el video 13 cuando ya he definido todas las vistas CRUD

urlpatterns = [
    # url(r'^$', "posts.views.post_home"), antes del video 13 era sólo esta url definida
    url(r'^list/$', post_list, name='list'), #él hace en lugar de esto: url(r'^$', "posts.views.post_list") #en v23 le doy nombre
    #para que si pongo http://localhost:8000/posts/ no me de error por no estar definida esta vista,pero yo mantengo list
    url(r'^create/$', post_create),
    #url(r'^detail/$', post_detail), cambia en el video 18 donde uso url dinamica para los detalles de cada post
    #url(r'^(?P<id>\d+)/$', post_detail), #esta es la nueva del video 18
    #url(r'^(?P<id>\d+)/$', post_detail, name='detail'), #en el video 19 le doy un nombre
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'), #en v29 para incluir el slug

    #url(r'^update/$', post_update), cambia en el video 21
    #url(r'^(?P<id>\d+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'), #en v29 para usar el slug
    # url(r'^delete/$', post_delete), Antigua que cambia en el v23 donde trabajo delete
    # url(r'^(?P<id>\d+)/delete/$', post_delete),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete), #en v29 para cambiar a slug
]