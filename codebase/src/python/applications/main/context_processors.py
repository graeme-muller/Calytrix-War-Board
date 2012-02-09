##
## When registered in the TEMPLATE_CONTEXT_PROCESSORS setting in settings.py, methods in here
## will 'load' up the template context dictionary with whatever values we need, each time a
## template context is required.
##
## This allows us to avoid having to repeatedly code in common values required to *all*
## templates in the application. Obviously this should not be abused!
##
## For more information, refer to:
## http://docs.djangoproject.com/en/1.3/ref/settings/#template-context-processors
##

from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser

from accounts.models import UserSiteProfile

##
# Provides the template context variable 'user_site_profile', from which can be
# obtained the user's site profile details, such as preferredtheme, timezone,
# and so on...
#
# If there is no 'user' attribute in the request, uses AnonymousUser (from
# django.contrib.auth).
#
# @see accounts.UserSiteProfile
#
def user_site_profile(request):
    # If we access request.user, request.session is accessed, which results in
    # 'Vary: Cookie' being sent in every request that uses this context
    # processor, which can easily be every request on a site if
    # TEMPLATE_CONTEXT_PROCESSORS has this context processor added.  This kills
    # the ability to cache.  So, we carefully ensure these attributes are lazy.
    # We don't use django.utils.functional.lazy() for User, because that
    # requires knowing the class of the object we want to proxy, which could
    # break with custom auth backends.  LazyObject is a less complete but more
    # flexible solution that is a good enough wrapper for 'User'.
    def get_user():
        if hasattr(request, 'user'):
            return request.user
        else:
            return AnonymousUser()

    # Get the user...
    user = SimpleLazyObject(get_user)
    if isinstance(user, AnonymousUser):
        # it's an AnonymousUser, so use a temporary instance
        # which will contain the default settings
        user_site_profile = UserSiteProfile()
    else:
        try:
            # it's a registered user, so get their profile
            # using the standard get_profile() method...
            user_site_profile = user.get_profile()
        except UserSiteProfile.DoesNotExist:
            # This shouldn't happen unless for some reason
            # the UserSiteProfile was manually deleted, but
            # let's be ready for that eventuality, shall we?
            # Regenerate the instance
            user_site_profile = UserSiteProfile()
            user_site_profile.user = user
            user_site_profile.save()

    return {
        'user_site_profile':  user_site_profile,
    }
