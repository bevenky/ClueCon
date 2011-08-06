from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.generic.simple import direct_to_template


def home(request, template = "cluecon_ui/index.html"):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_user_dashboard'))
    return direct_to_template(request, template)


@login_required
@never_cache
def auth_user_dashboard(request, template = "cluecon_ui/auth_user_dashboard.html"):
    response_dict = {}
    return direct_to_template(request, template)
