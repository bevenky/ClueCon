import sys
import os

#Add the virtual Python environment site-packages directory to the path
import site
site.addsitedir('/usr/src/django1.3_env/lib/python2.6/site-packages/')

#Add project to PYTHONPATH
WSGI_FILE_LOCATION = os.path.dirname(__file__)
sys.path.append(os.path.join(WSGI_FILE_LOCATION, "../cluecon"))

#Add django settings file to environment path
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

#This import should be here as it will only work after virtual python env is set
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
