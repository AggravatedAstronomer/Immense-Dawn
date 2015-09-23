from django.contrib import admin

from .models import Summoner
from .models import ThreatParameter
from .models import PsychWarfareConfig
from .models import SelfDiagnosticModule
from .models import SelfDiagnosticOverseer
# Register your models here.
admin.site.register(Summoner)
admin.site.register(ThreatParameter)
admin.site.register(PsychWarfareConfig)
admin.site.register(SelfDiagnosticModule)
admin.site.register(SelfDiagnosticOverseer)
