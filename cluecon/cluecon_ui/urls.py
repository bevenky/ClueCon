from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views

from views import auth_user_dashboard, home, set_currentspeaker, handle_call_request

urlpatterns = patterns('',

    url(r'^$', home),
    url(r'^user/login/$', auth_views.login,
                           {'template_name': 'cluecon_ui/login.html'},
                           name='auth_login'),
    url(r'^user/logout/$', auth_views.logout_then_login),
    url(r'^user/dashboard/$', auth_user_dashboard, name = "auth_user_dashboard"),

    url(r'^speaker/currentlyspeaking/$', set_currentspeaker),
    url(r'^speaker/vote/$', handle_call_request),
 )
