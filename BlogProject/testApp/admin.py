from django.contrib import admin
from testApp.models import Post,Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','body','publish','created','updated','status','tags']
    list_filter=('status','author','publish')
    search_fields=('title','body')
    ordering=['status','publish']
    raw_id_fields=('author',)
    prepopulated_fields={'slug':('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display=['name','email','post','body','created','updated','active',]
    list_filter=['active','created','updated']
    search_fields=['name','email','body']


admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
