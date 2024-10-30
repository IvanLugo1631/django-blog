from django.contrib import admin
from .models import Post
# admin.site.register(Post)
# Register your models here.

#Customize admin site
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author'] #Add filter to the right side of the admin page
    search_fields = ['title', 'body'] # Add search bar to the top of the admin page
    prepopulated_fields = {'slug': ('title',)} # Automatically generate the slug field based on the title field
    raw_id_fields = ['author'] # Add a lookup widget to the author field
    date_hierarchy = 'publish' # Add a date-based drilldown navigation by that field
    ordering = ['status', 'publish'] # Sort the posts by status and publish fields