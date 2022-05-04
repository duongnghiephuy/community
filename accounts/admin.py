from django.contrib import admin
from .models import Community, MemberRole, UserProfile

admin.site.register(Community)
admin.site.register(MemberRole)
admin.site.register(UserProfile)
# Register your models here.
