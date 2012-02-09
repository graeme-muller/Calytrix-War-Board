import logging

from django.http import HttpResponse
from django.template import RequestContext, loader

from qrcoder import *
from contrib import fileutils

LOGGER = logging.getLogger(__name__)

##
#  This is the login page
#
def home(request):
    # Show the QR code main page
    template = 'qrcode/index.html'
    t = loader.get_template(template)
    c = RequestContext(request, {
    });
    return HttpResponse(t.render(c))

##
#  This is the login page
#
def qrcode(request, type=20, level=QRErrorCorrectLevel.L, boxsize=2, offset=0):
    # qr = QRCode(20, QRErrorCorrectLevel.L)
    qr = QRCode(int(type), int(level))
    qr.addData('BEGIN:VCARD\n')
    qr.addData('N:Brett;Mobsby;;Mr\n')
    qr.addData('FN:Andrew Laws\n')
    qr.addData('EMAIL;TYPE=PREF,INTERNET:andrew.laws@calytrix.com\n')
    qr.addData('TITLE:Senior Software Engineer\n')
    qr.addData('TEL;TYPE=WORK,CELL,VOICE:+61 402 223 041\n')
    qr.addData('ORG:Calytrix Technologies\n')
    qr.addData('ADR;TYPE=WORK:;;110 William Street;Perth;WA;6000;Australia\n')
    qr.addData('TEL;TYPE=PREF,WORK,VOICE:+61 8 9226 4288\n')
    qr.addData('TEL;TYPE=WORK,FAX:+61 8 9226 0311\n')
    qr.addData('VERSION:3.0\n')
    qr.addData('END:VCARD\n')
    qr.make()
    im = qr.makeImage(int(boxsize), int(offset))
    return image_in_httpresponse(im, 'png')

def image_in_httpresponse(image, image_type):
    # ContentFile class to hold image in a 'pseudo-file'
    from StringIO import StringIO
    class ContentFile (StringIO) :
        def __init__ (self, content, name=None) :
            StringIO.__init__(self, content)
            self.name = name
        def read (self, size=None) :
            o = StringIO.read(self, size)
            if not size :
                self.seek(0)
            return o

    tmp = ContentFile("", name="image.%s"%image_type)
    image.save(tmp, **image.info)
    tmp.seek(0)
    response = HttpResponse(
        tmp.read(),
        mimetype=fileutils.get_mimetype(image_type)
    )
    return response