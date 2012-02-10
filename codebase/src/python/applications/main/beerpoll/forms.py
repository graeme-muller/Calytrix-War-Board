##
# A form for a normal user to edit Exercise instances
#
# We use the auto-create the form using the ModelForm helper class, since we
# don't need to do anything particularly tricky with the form
#
from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput
from main.models import BeerChoice

##
# A form to allow a Score to be created and modified
#
# We use the auto-create the form using the ModelForm helper class, since we
# don't need to do anything particularly tricky with the form
class BeerChoiceForm( ModelForm ):
    class Meta:
        model = BeerChoice
        exclude = [ 'poll' ]
        widgets = { 'value': HiddenInput, }
