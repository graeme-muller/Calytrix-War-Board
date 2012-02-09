import datetime, time, calendar

import settings

from django.forms.fields import IntegerField as DjangoFormsIntegerField
from django.forms.util import ValidationError as FormValidationError
from django.forms.widgets import MultiWidget, DateInput, TimeInput, Select, TextInput

from django.core import exceptions

from django.utils.safestring import mark_safe
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _

from django.db.models import Field, SubfieldBase, CharField, PositiveIntegerField

try:
    import uuid
except ImportError:
    from django_extensions.utils import uuid

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

##
# UUID Version Error Exception definition
#
class UUIDVersionError(Exception):
    pass

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

##
#  UUIDField
#
#  By default uses UUID version 4 (generate from host ID, sequence number and
#  current time). The field supports all uuid versions which are natively
#  supported by the uuid python module.
#  For more information see: http://docs.python.org/lib/module-uuid.html
#
#  Modified to allow user specification of the UUID by setting optional argument
#  auto_if_unset to True
#
#
class UUIDField(CharField):
    def __init__(self, verbose_name=None, name=None, auto_if_unset=True, version=4, node=None, clock_seq=None, namespace=None, **kwargs):
        kwargs['max_length'] = 512
        if auto_if_unset:
            kwargs['blank'] = True
            kwargs.setdefault('editable', False)
        self.auto_if_unset = auto_if_unset
        self.version = version
        if version == 1:
            self.node, self.clock_seq = node, clock_seq
        elif version == 3 or version == 5:
            self.namespace, self.name = namespace, name
        CharField.__init__(self, verbose_name, name, **kwargs)

    def get_internal_type(self):
        return CharField.__name__ #@UndefinedVariable

    def create_uuid(self):
        if not self.version or self.version == 4:
            return uuid.uuid4()
        elif self.version == 1:
            return uuid.uuid1(self.node, self.clock_seq)
        elif self.version == 2:
            raise UUIDVersionError("UUID version 2 is not supported.")
        elif self.version == 3:
            return uuid.uuid3(self.namespace, self.name)
        elif self.version == 5:
            return uuid.uuid5(self.namespace, self.name)
        else:
            raise UUIDVersionError("UUID version %s is not valid." % self.version)

    def pre_save(self, model_instance, add):
        # default behaviour here is to create a UUID if none has been set
        value = getattr(model_instance, self.attname)
        if self.auto_if_unset and not value:
            value = unicode(self.create_uuid())
            setattr(model_instance, self.attname, value)
        return value


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

class SplitUNIXTimeWidget(MultiWidget):
    class Media:
        js = (settings.ADMIN_MEDIA_PREFIX + "js/core.js",
              settings.ADMIN_MEDIA_PREFIX + "js/calendar.js",
              settings.ADMIN_MEDIA_PREFIX + "js/admin/DateTimeShortcuts.js")

    """
    A Widget that splits UNIX time input into two <input type="text"> boxes and a timezone
    selection dropdown.
    """
    date_format = DateInput.format
    time_format = TimeInput.format
    default_timezones = (
                         (-12*60,  'GMT -1200'),
                         (-11*60,  'GMT -1100'),
                         (-10*60,  'GMT -1000'),
                         (-9.5*60, 'GMT -0930'),
                         (-9*60,   'GMT -0900'),
                         (-8*60,   'GMT -0800'),
                         (-7*60,   'GMT -0700'),
                         (-6*60,   'GMT -0600'),
                         (-5*60,   'GMT -0500'),
                         (-4.5*60, 'GMT -0430'),
                         (-4*60,   'GMT -0400'),
                         (-3.5*60, 'GMT -0330'),
                         (-3*60,   'GMT -0300'),
                         (-2*60,   'GMT -0200'),
                         (-1*60,   'GMT -0100'),
                         (0,       'GMT +0000'),
                         (1*60,    'GMT +0100'),
                         (2*60,    'GMT +0200'),
                         (3*60,    'GMT +0300'),
                         (3.5*60,  'GMT +0330'),
                         (4*60,    'GMT +0400'),
                         (4.5*60,  'GMT +0430'),
                         (5*60,    'GMT +0500'),
                         (5.5*60,  'GMT +0530'),
                         (5.75*60, 'GMT +0545'),
                         (6*60,    'GMT +0600'),
                         (6.5*60,  'GMT +0630'),
                         (7*60,    'GMT +0700'),
                         (8*60,    'GMT +0800'),
                         (8.75*60, 'GMT +0845'),
                         (9*60,    'GMT +0900'),
                         (9.5*60,  'GMT +0930'),
                         (10*60,   'GMT +1000'),
                         (10.5*60, 'GMT +1030'),
                         (11*60,   'GMT +1100'),
                         (11.5*60, 'GMT +1130'),
                         (12*60,   'GMT +1200'),
                         (12.75*60,'GMT +1245'),
                         (13*60,   'GMT +1300'),
                         (14*60,   'GMT +1400'),
                         )

    def __init__(self, attrs=None, date_format=None, time_format=None, timezones=None):
        widgets = (DateInput(attrs={'class': 'vDateField', 'size': '10'}, format=date_format), # Date
                   TimeInput(attrs={'class': 'vTimeField', 'size': '8'}, format=time_format), # Time
                   Select(choices= (timezones and timezones or self.default_timezones) ), # Timezone Selection
                   TextInput(attrs={'hidden':'hidden'}) # hidden, holds the actual UNIX time value
                   )
        super(SplitUNIXTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            # DATE, TIME, TIMEZONE, UNIXTIME
            return [value.date(), value.time(), 0, int(calendar.timegm(value.utctimetuple()))]
        return [None,None,None,None]

    def render(self, name, value, attrs=None, choices=()):
        output = [super(SplitUNIXTimeWidget, self).render(name, value, attrs)]
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        output.append(u'<script type="text/javascript">\n')
        output.append(u'var update_%s_value=function(){\n' % name)
        output.append(u'    try{\n')
        output.append(u'        var dmy=document.getElementById("%s_0").value.split("-");\n' % (id_))
        output.append(u'        for(i=0;i<dmy.length;i++){dmy[i]=parseInt(dmy[i]);}\n')
        output.append(u'        var hms=document.getElementById("%s_1").value.split(":");\n' % (id_))
        output.append(u'        for(i=0;i<hms.length;i++){hms[i]=parseInt(hms[i]);}\n')
        output.append(u'        var tzOffsetMins=parseInt(document.getElementById("%s_2").value);\n' % (id_))
        output.append(u'        var utcDate=new Date();\n')
        output.append(u'        utcDate.setUTCFullYear(dmy[0],dmy[1]-1,dmy[2]);\n')
        output.append(u'        utcDate.setUTCHours(hms[0],hms[1],hms.length>2?hms[2]:0);\n')
        output.append(u'        if (tzOffsetMins!=0)\n')
        output.append(u'            utcDate=new Date(utcDate.getTime()-(tzOffsetMins*60000));\n')
        output.append(u'        document.getElementById("%s_3").value=Math.floor(utcDate.getTime()/1000);\n' % (id_))
        output.append(u'    }catch(err){\n')
        output.append(u'        document.getElementById("%s_3").value=-1;\n' % (id_))
        output.append(u'    }\n')
        output.append(u'}\n')
        output.append(u'addEvent(document.getElementById("%s_0"),"blur",update_%s_value);\n' % (id_, name))
        output.append(u'addEvent(document.getElementById("%s_1"),"blur",update_%s_value);\n' % (id_, name))
        output.append(u'addEvent(document.getElementById("%s_2"),"change",update_%s_value);\n' % (id_, name))
        output.append(u'</script>\n')
        return mark_safe(u''.join(output))

    def format_output(self, rendered_widgets):
        return mark_safe(u'<p class="unixdatetime">%s %s<br />%s %s<br />%s %s%s%s</p>' % \
                            (_('Date:'), rendered_widgets[0],
                             _('Time:'), rendered_widgets[1],
                             _('Timezone:'), rendered_widgets[2],
                             '', rendered_widgets[3]) # hidden, holds the actual UNIX time value
                         )


# Custom form field
class UnixTimeFormField(DjangoFormsIntegerField):

    def __init__(self, *args, **kwargs):
        self.max_length = 10
        kwargs.update({'widget':SplitUNIXTimeWidget})
        super(UnixTimeFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # what comes in here is ['YYYY-MM-DD','HH:MM:SS','TZ_OFFSET','UNIXTIME']
        # we are only interested in the UNIXTIME part
        try:
            print value[3]
            value = super(DjangoFormsIntegerField, self).clean(value[3])
            try:
                datetime.datetime.fromtimestamp(float(value))
            except:
                try:
                    raise FormValidationError('%s is not a valid UNIX time value.' % value)
                except:
                    raise FormValidationError('No value for UNIX time.')
        except FormValidationError:
            raise FormValidationError('Enter a valid date.')
        return value

##
#  UnixTimeField
#
class UnixTimeField(PositiveIntegerField):
    __metaclass__ = SubfieldBase

    auto_now = False
    auto_now_add = False

    def __init__(self, *args, **kwargs):
        if kwargs.get('auto_now', False):
            self.auto_now = True
            kwargs.pop('auto_now')
        if kwargs.get('auto_now_add', False):
            self.auto_now_add = True
            kwargs.pop('auto_now_add')
        Field.__init__(self, *args, **kwargs)

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            now = datetime.datetime.utcnow()
            unixtime = int(calendar.timegm(now.utctimetuple()))
            setattr(model_instance, self.attname, unixtime)
            return unixtime
        else:
            return super(UnixTimeField, self).pre_save(model_instance, add)

    def get_prep_value(self, value):
        # Casts dates into the format expected by the backend for
        # comparisons etc (i.e. an integer value)
        if value == None:
            return None
        if type(value) in (int, long,):
            return value
        if type(value) is float:
            return int(value)
        # assume it's a date, convert to UNIX time
        return int(calendar.timegm(value.utctimetuple()))

    def get_db_prep_value(self, value, connection, prepared=False):
        # Casts dates into the format expected by the backend
        # (i.e. an integer value)
        if not prepared:
            value = self.get_prep_value(value)
        return value

    def to_python(self, value):
        # convert the raw UNIX time from the database to the
        # type expected from the field - this is a bit more
        # involved than it might need to be because it tries to
        # be backward compatible with older style date/times
        # which were potentially represented as strings
        if value == None or value == '':
            return None
        # already a date?
        if type(value) == datetime.datetime:
            # done!
            return value
        # int or float value?
        elif type(value) in (float, int, long):
            # convert from float, int or long UNIX time value
            return datetime.datetime.fromtimestamp(value)
        # text?
        elif type(value) in (str, unicode):
            try:
                # attempt to convert the text to a int to use as a UNIX
                # time value
                return datetime.datetime.fromtimestamp(int(value))
            except ValueError:
                # Probably a date/time string such as '2011-12-25 10:30:45'
                # Attempt to parse the text - because dates in this format have
                # no timezone detail, the resulting date/time will reflect the
                # *current* timezone setting being used, which may or may not be
                # the timezone in which the date/time was recorded. All of which
                # is to say that if a text based date/time passed in the field
                # will revert to the "standard" Django DateTimeField behaviour
                # and we will be no worse off. Also useful for backward
                # compatibility as it allows import of 'old' style dates from
                # (say) JSON dumps of database content where models may have used a
                # DateTimeField instead of a UnixTimeField
                value = smart_str(value)
                # split usecs, because they are not recognized by strptime.
                if '.' in value:
                    try:
                        value, usecs = value.split('.')
                        usecs = int(usecs)
                    except ValueError:
                        raise exceptions.ValidationError(self.error_messages['invalid'])
                else:
                    usecs = 0
                kwargs = {'microsecond': usecs}
                try: # Seconds are optional, so try converting seconds first.
                    return datetime.datetime(*time.strptime(value, '%Y-%m-%d %H:%M:%S')[:6],
                                             **kwargs)
                except ValueError:
                    try: # Try without seconds.
                        return datetime.datetime(*time.strptime(value, '%Y-%m-%d %H:%M')[:5],
                                                 **kwargs)
                    except ValueError: # Try without hour/minutes/seconds.
                        try:
                            return datetime.datetime(*time.strptime(value, '%Y-%m-%d')[:3],
                                                     **kwargs)
                        except ValueError:
                            raise exceptions.ValidationError(self.error_messages['invalid'])


    def formfield(self, **kwargs):
        defaults = {'form_class': UnixTimeFormField,
                    'help_text': 'Enter date/time',
                    }
        defaults.update(kwargs)
        return super(UnixTimeField, self).formfield(**defaults)
