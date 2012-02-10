from django.contrib import admin
from django.db import models
import main.fields as MainFields



# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# MODELS FOR BEER POLL
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

##
#
# Defines the 'Which beer would you like Calytrix to get next" poll.
# Each poll can have up to 5 choices of beer.
#
class Poll( models.Model ):
    question = models.CharField( max_length=200, )
    
    def __unicode__(self):
        return self.question

BEER_CHOICES = (
    ( 'boags_premium',          'Boags Premium' ),
    ( 'coopers_sparking',       'Coopers Sparkling' ),
    ( 'corona',                 'Corona' ),
    ( 'fat_yak',                'Fat Yak' ),
)
BEER_CHOICES_DICT = dict( BEER_CHOICES )

##
#
# User's can add a beer with a name and icon (beer logo) until there are 5 in the list.
# Each beer choice is associated with the poll.
#
class BeerChoice( models.Model ):
    poll        = models.ForeignKey( Poll )
    beername    = models.CharField( max_length=30, 
                                    choices=BEER_CHOICES,
                                    default=BEER_CHOICES[0][0] )
    logo        = models.ImageField( 'logo', upload_to='media/images/beer-logos', blank=True, null=True, )
    votes       = models.IntegerField( default=0 )
    
    ##
    # Display the object in a user friendly manner
    #
    def __unicode__( self ):
        return BEER_CHOICES_DICT.get( self.beername, "!unknown beer!" )

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

##
# This function ensures that the uploaded Exercise logos are named after the UUID of
# the exercise, not by the original filename
# @param instance the model instance - in this case it will always be an Exercise
#        since that's where this function is used
# @param filename the original name of the file
# @return the upload path for the file
#def exercise_logo_image_upload_to( instance, filename ):
#    return 'uploads/exercise/logos/%s%s' % ( instance.uuid, os.path.splitext(filename)[1] );


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
