from django.db import models
from django.utils.translation import ugettext_lazy as _

day_choices = ( (1, (1)),
                (2, (2)),
                (3, (3)),
)

class Speaker(models.Model):
    """Speaker Details
    """
    name = models.CharField(_('speaker name'), max_length=50)
    currently_speaking = models.BooleanField(_('currently speaking'))
    total_votes = models.IntegerField(_('total votes'), default=0)
    talk_name = models.CharField(_('talk name'), max_length=255)
    talk_schedule = models.DateTimeField(_('talk schedule'))
    talk_day = models.IntegerField(_('talk day'), choices=day_choices,)

    def __unicode__(self):
        return u"%s" % self.name

    def save(self, *args, **kwargs):
        if self.currently_speaking == True:
            try: # set all other objects as false
                Speaker.objects.filter(currently_speaking=True).update(currently_speaking=False)
            except Exception:
                pass
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
