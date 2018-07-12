"""trydjango19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings #para el v25 de static files
from django.conf.urls.static import static #para el v25 de static files


from django.conf.urls import url, include #include para el video 13 y los cambios abajo
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^posts/', include("posts.urls", namespace='posts')), #usada en video 19 para introducir el space
    # url(r'^posts/', include("posts.urls")), #usada hasta video 18.  #introduzco esto para definir todas las ursls que
    #seguiran a  posts... como posts.create, posts.update... que defino en urls.py de la app posts

    # url(r'^posts/$', "posts.views.post_home"), usada hasta el video 13, despues cambia al usar include
    #url(r'^NOMBRE/$', "<APPNAME>.views.<FUNCTION_NAME>"), se hace de esta forma, entre comillas
    # porque realmente
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #v28 añadir imagenes
