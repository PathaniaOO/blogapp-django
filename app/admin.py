from profile import Profile
from django.contrib import admin

from app.models import Comments, Post, Tag,Profile, WebsiteMeta

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
    
admin.site.register(Post,PostAdmin)
admin.site.register(Tag)
admin.site.register(Comments)
admin.site.register(Profile)
admin.site.register(WebsiteMeta)