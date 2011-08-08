from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.generic.simple import direct_to_template

from models import Speaker, Vote

import twitter
import plivohelper
import simplejson


def post_tweet(text):
    try:
        api = twitter.Api(consumer_key=settings.CONSUMER_KEY,
                        consumer_secret=settings.CONSUMER_SECRET,
                        access_token_key=settings.ACCESS_TOKEN_KEY,
                        access_token_secret=settings.ACCESS_TOKEN_SECRET)
        status = api.PostUpdate(text)
        if status.text == text:
            return True
        return False
    except Exception:
        return False

def home(request, template="cluecon_ui/index.html"):
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
def auth_user_dashboard(request, template="cluecon_ui/auth_user_dashboard.html"):
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
                Speaker.objects.filter(currently_speaking=True
                                            ).update(currently_speaking=False)
            except Exception:
                pass

            try: # Now set the requested speaker_id as speaking
                Speaker.objects.filter(id=speaker_id
                                            ).update(currently_speaking=True)
            except Exception:
                return HttpResponseBadRequest()

            results =   {
                            "success" : "True",
                            "id": str(id)
            }
            json = simplejson.dumps(results)
            return HttpResponse(json, mimetype='application/json')
    return HttpResponseBadRequest()


def get_post_param(request, param):
    if param in request.POST:
        return request.POST[param]
    return ""


def create_fail_restxml():
    r = plivohelper.Response()
    g = r.addPreAnswer()
    g.addSpeak("Sorry. Your vote cannot be considered")
    r.addHangup(reason='rejected')
    return r


def create_success_restxml():
    r = plivohelper.Response()
    g = r.addPreAnswer()
    g.addSpeak("Thanks. Your vote has been considered.")
    r.addHangup(reason='rejected')
    return r

def mask_phone(from_no):
    return "%sXX" %from_no[0:-2]

@csrf_exempt
def handle_call_request(request):
    if request.method == 'POST':
        # dont accept requests from any other system
        if request.META['REMOTE_ADDR'] == '127.0.0.1':
            to_no = get_post_param(request, 'To')
            from_no = get_post_param(request, 'From')
            if from_no != "":
                direction = get_post_param(request, 'Direction')
                if to_no == settings.DID and direction == 'inbound':
                    # get current speaker
                    try:
                        speaker = get_object_or_404(Speaker, currently_speaking=True)
                    except Http404:
                        speaker = None
                    if speaker is not None:
                        # check if this vote is already considered
                        try:
                            vote = get_object_or_404(Vote, speaker=speaker,
                                                            phone_no=from_no)
                        except Http404:
                            vote = None
                        if vote is None:
                            speaker.total_votes = speaker.total_votes + 1
                            speaker.save()
                            vote_dict={
                                        "speaker": speaker,
                                        "phone_no": from_no,
                            }
                            vote_obj= Vote(**vote_dict)
                            vote_obj.save()
                            tweet_text = '''Got a vote for "%s" speaking on "%s" from the number "+%s" #cluecon''' % (speaker.name,
                                                                                                            speaker.talk_name,
                                                                                                            mask_phone(from_no))
                            if not post_tweet(tweet_text):
                                pass # do some logging here
                            # return success
                            response = create_success_restxml()
                            return HttpResponse(response, mimetype='text/xml')
    # return fail for all other cases
    response = create_fail_restxml()
    return HttpResponse(response, mimetype='text/xml')
