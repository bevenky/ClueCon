from django.db import models
from django.utils.translation import ugettext_lazy as _


class Speaker(models.Model):
    """Speaker Details
    """
    name = models.CharField(_('speaker name'), max_length=50)
    currently_speaking = models.BooleanField(_('currently speaking'))
    total_votes = models.IntegerField(_('total votes'), default=0)
    talk_name = models.CharField(_('talk name'), max_length=50)
    talk_schedule = models.DateTimeField(_('talk schedule'))

    def __unicode__(self):
        return u"%s" % self.name

    def save(self, *args, **kwargs):
        if self.currently_speaking == True:
            pass # set all other objects as false
        super(Speaker, self).save(*args, **kwargs)


class Vote(models.Model):
    """Vote Details
    """
    speaker = models.ForeignKey(Speaker)
    time = models.DateTimeField(_('talk schedule'), auto_now_add=True)
    phone_no = models.CharField(_('phone number'), max_length=15)

    def __unicode__(self):
        return u"%s" % self.speaker

    class Meta:
        unique_together = ('speaker', 'phone_no')
