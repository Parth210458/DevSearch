from django.db import models
import uuid
from users.models import Profile
# Create your models here.
 
class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    demo_link = models.CharField(max_length=2000, blank=True, null = True)
    source_link = models.CharField(max_length=2000,null = True, blank=True)
    featured_img = models.ImageField(blank=True, null=True, default='default.jpg')
    tags = models.ManyToManyField('Tag', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    vote_total  = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio =  models.IntegerField(default=0, null=True, blank=True)
    id= models.UUIDField(default=uuid.uuid4, editable=False, unique=True,primary_key=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ["-vote_ratio", '-vote_total','title']

    @property
    def reviewrs(self):
        queryset = self.review_set.all().values_list('owner__id',flat=True)
        return queryset
    
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes/totalVotes)*100

        self.vote_total = totalVotes
        self.vote_ratio = ratio
        
        self.save()
    @property
    def imageURL(self):
        try:
            url = self.featured_img.url
        except:
            url = ""
        return url

class Review(models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True) 
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    VOTE_TYPE = (
        ('up','up_vote'),
        ('down','down_vote')
    )
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4, editable=False, unique=True,primary_key=True)

    class Meta:
        unique_together = [['owner','project']]

    def __str__(self):
        return self.value
    

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4, editable=False, unique=True,primary_key=True)
    def __str__(self):
        return self.name
