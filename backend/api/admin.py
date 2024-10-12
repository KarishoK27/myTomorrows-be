from django.contrib import admin

from .models import (
    EAP,
    Booking,
    ClinicalTrial,
    CTReferall,
    EAPDossier,
    Hospital,
    Patient,
    Specialist,
    Specialization,
)

admin.site.register(Specialization)
admin.site.register(Hospital)
admin.site.register(Specialist)
admin.site.register(Patient)
admin.site.register(Booking)
admin.site.register(EAP)
admin.site.register(EAPDossier)
admin.site.register(ClinicalTrial)
admin.site.register(CTReferall)
