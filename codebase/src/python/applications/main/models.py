from django.db import models
from django.contrib import admin

import main.fields as MainFields

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

##
# Defines a Thing
#
class Thing(models.Model):
    uuid = MainFields.UUIDField('uuid', primary_key=True)
    name = models.CharField('A Name', max_length=15,)
    date_time = models.DateTimeField('Date and Time', max_length=15,)
    unix_time = MainFields.UnixTimeField('A UNIX Time', auto_now_add=True)

    ##
    # Display the inert object in a user friendly manner
    #
    def __unicode__(self):
        return u'%s' % (self.uuid)

    class Meta:
        verbose_name = 'Thing'
        verbose_name_plural = 'Things'
        ordering = ['unix_time']

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

##
#  Thing administration class definition and registration
#
class ThingAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'date_time', 'unix_time',)
admin.site.register(Thing, ThingAdmin)
