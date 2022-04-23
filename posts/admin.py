from django.contrib import admin
from .models import Order, Post

# Register your models here.
admin.site.register(Post)
admin.site.register(Order)
