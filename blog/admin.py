from django.contrib import admin
from .models import BlogPost, Comment

# Register your models here.
# I can also change the admin titles here...

admin.site.register((BlogPost, Comment))

