from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image", #añadido para el v28 se subir imagenes
            "draft", #v35 borrador de post
            "publish", #v35 fecha de publicación
         ]