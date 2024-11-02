from django.db import models
from django.utils import timezone
from django.conf import settings

class PublishedManager(models.Manager):
    def get_queryset(self):
        return(
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )

# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250) #A slug is a short label for something, containing only letters, numbers, underscores, or hyphens. They’re generally used in URLs. It creates an index on the slug field by default because of SlugField
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        #The choices attribute, which is required for choices, is an iterable of iterables where the first element in each iterable is the actual value to be set on the model, and the second element is the human-readable name.
        choices=Status,
        default=Status.DRAFT,
    )
    #The author field is a ForeignKey, which means that it is a many-to-one relationship with the User model. 
    # We specify the on_delete parameter to tell Django to delete the related blog posts when a user is deleted. 
    # The related_name attribute allows us to name the attribute that we use for the relation from the related object 
    # back to this one. We set it to blog_posts, which means that we can access the related objects using the user.blog_posts syntax.
    author = models.ForeignKey( #It creates an index on the author field by default because of ForeignKey
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    objects = models.Manager() #The default manager
    published = PublishedManager()
    class Meta:
        #Ordering in descending order using hyphen
        ordering = ['-publish']
        #Indexing the publish field so that the database can retrieve the data faster
        indexes = [
            models.Index(fields=['-publish']),
        ]
    #This method is used to return the title of the post
    def __str__(self):
        return self.title