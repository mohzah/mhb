# -*- coding: utf-8 -*-

from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse


import mimetypes
import os


class serveGeneratedFiles(View):

    """A simple stand-in view to serve
    generated files. Should be replaced by uwsgi
    webserver integration.
    """

    def get(self, request, filename):

        mimetypes.init()

        print filename
        fp = os.path.join(settings.MEDIA_ROOT, filename)
        fsock = open(fp, 'rb')

        mime_type_guess = mimetypes.guess_type(filename)
        resp = HttpResponse(fsock, content_type=mime_type_guess[0])

        resp['Content-Disposition'] = "filename=%s" % filename

        return resp
