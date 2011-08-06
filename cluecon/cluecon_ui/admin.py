from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin
from django.utils.translation import ugettext_lazy as _

from models import *



class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'currently_speaking', 'talk_name', 'talk_schedule',
                                                            'total_votes')
    list_filter = ['currently_speaking']
    search_fields = ['name']
    list_per_page = 50
admin.site.register(Speaker, SpeakerAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('speaker', 'time', 'phone_no')
    list_filter = ['speaker']
    search_fields = ['speaker__name', 'phone_no']
    list_per_page = 50
admin.site.register(Vote, VoteAdmin)
