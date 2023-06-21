from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


from .models import Profile

#@receiver(post_save,sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username = user.username,
            email = user.email,
            name = user.first_name
        )
        

def updateUser(sender, instance,created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.username = profile.username
        user.first_name = profile.name
        user.email = profile.email
        user.save()

#def deleteUser(sender, instance, **kwargs):
    #user = instance.user
    #user.delete()


#post_delete.connect(deleteUser,sender=Profile)

post_save.connect(updateUser,sender=Profile)
post_save.connect(createProfile, sender= User )