from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.generic.simple import direct_to_template

from models import Speaker

def home(request, template = "cluecon_ui/index.html"):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_user_dashboard'))
    first_day = Speaker.objects.filter(talk_day=1)
    second_day = Speaker.objects.filter(talk_day=2)
    third_day = Speaker.objects.filter(talk_day=3)
    return direct_to_template(request, template,
                                extra_context={ "first_day": first_day,
                                                "second_day": second_day,
                                                "third_day": third_day
                                                 })

@login_required
@never_cache
def auth_user_dashboard(request, template = "cluecon_ui/auth_user_dashboard.html"):
    first_day = Speaker.objects.filter(talk_day=1)
    second_day = Speaker.objects.filter(talk_day=2)
    third_day = Speaker.objects.filter(talk_day=3)
    return direct_to_template(request, template,
                                extra_context={ "first_day": first_day,
                                                "second_day": second_day,
                                                "third_day": third_day
                                                 })

def set_currentspeaker(request):
    if request.method == 'POST':
        if 'speaker_id' in request.POST:
            speaker_id = request.POST['speaker_id']
            try: # set all other objects as false
                Speaker.objects.filter(currently_speaking=True).update(currently_speaking=False)
            except Exception:
                pass

            try: # Now set the requested speaker_id as speaking
                Speaker.objects.filter(id=speaker_id).update(currently_speaking=True)
            except Exception:
                return HttpResponseBadRequest()

            results =   {
                            "success" : "True",
                            "id": str(id)
            }
            json = simplejson.dumps(results)
            return HttpResponse(json, mimetype='application/json')
    return HttpResponseBadRequest()
