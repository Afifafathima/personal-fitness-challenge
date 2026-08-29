from django.contrib import admin

from .models import (
    User,
    Trainer,
    Challenge,
    JoinChallenge,
    Report
)

admin.site.register(User)
admin.site.register(Trainer)
admin.site.register(Challenge)
admin.site.register(JoinChallenge)
admin.site.register(Report)