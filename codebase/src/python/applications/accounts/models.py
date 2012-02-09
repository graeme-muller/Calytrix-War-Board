from django.db import models
from django.dispatch import receiver
from django.contrib import admin
from django.contrib.auth.models import User

#--------------------------------------------------------------------------------------------------
#                    'STATIC' VARIABLES
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
#                    CLASSES
#--------------------------------------------------------------------------------------------------

##
# From: http://www.djangobook.com/en/1.0/chapter12/
#   In a nutshell, many sites need to store more user information than is
#   available on the standard User object. To compound the problem, most sites
#   will have different "extra" fields. Thus, Django provides a lightweight way
#   of defining a "profile" object that's linked to a given user. This profile
#   object can differ from project to project, and it can even handle different
#   profiles for different sites served from the same database.
#
#   Django needs to know where to look for this profile object. This is done by
#   setting the AUTH_PROFILE_MODULE setting to the identifier for your model.
#   So, if your model lives in an application called 'myapp', and the model class
#   name is MySiteProfile', you'd put this in your settings file:
#
#     AUTH_PROFILE_MODULE = "myapp.mysiteprofile"
#
#   Once that's done, you can access a user's profile by calling
#   user.get_profile(). This function could raise a SiteProfileNotAvailable
#   exception if AUTH_PROFILE_MODULE isn't defined, or it could raise a
#   DoesNotExist exception if the user doesn't have a profile already (you'll
#   usually catch that exception and create a new profile at that time).
#
# @see http://docs.djangoproject.com/en/1.3/ref/settings/#auth-profile-module
# @see http://docs.djangoproject.com/en/1.3/topics/auth/#auth-profiles
#
# NOTE: The user site profile instance for a User is automatically loaded into
# template context dictionaries by a context processor we've registered in the
# TEMPLATE_CONTEXT_PROCESSORS setting in settings.py for this site, otherwise
# this wouldn't happen automatically...
#
# @see main.context_processors.user_site_profile
#
class UserSiteProfile(models.Model):
    # This is the only required field
    user = models.ForeignKey(User, unique=True)
    # The remaining fields define the information to be stored for the user's profile:
    # theme - colour, fonts etc for the site

    ##
    #  The purpose of this static method is to ensure that a UserSiteProfile
    #  is created each time a new User is created.
    #
    #  This method is triggered via the Django signals framework so that it
    #  is run after a User is saved. The method checks to make sure it was
    # a user creation before proceeding.
    #
    #  See: http://docs.djangoproject.com/en/1.3/topics/signals/
    #
    @staticmethod
    @receiver(models.signals.post_save, sender=User)
    def _create_for_user(sender, **kwargs):
        # we only want to create an instance when a User is created
        # for the very first time
        if kwargs.get('created', False):
            # it's signal from a user creation
            user_instance = kwargs.get('instance', None)
            if user_instance:
                # create the site profile for the user
                user_site_profile = UserSiteProfile()
                user_site_profile.user = user_instance
                user_site_profile.save()

    ##
    # Display the instance in a user friendly manner
    #
    def __unicode__(self):
        return u'%s' % (self.user.username)

    class Meta:
        verbose_name = 'User Site Profile'
        verbose_name_plural = 'User Site Profiles'
        ordering = ['user']

##
#  Administration class definition and registration
#
class UserSiteProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ( None, {'fields': ( 'user', )} ),
    )
    list_display = ('user', )
    list_filter = ('user', )
    search_fields = ('user__username','user__firstname', 'user__lastname')
    ordering = ('user__username',)

admin.site.register(UserSiteProfile, UserSiteProfileAdmin)
