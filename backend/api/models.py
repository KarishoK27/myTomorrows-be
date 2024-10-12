import uuid

from django.db import models


class MedicalCondition(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    abbreviation = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return f"{self.name} ({self.city})"


class Contact(models.Model):
    contactid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    firstname = models.CharField(max_length=100, blank=False, null=False)
    lastname = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.email})"


class Specialist(Contact):
    PHYSICIAN = "PHYSICIAN"
    PHARMACISTS = "PHARMACISTS"

    CONTACT_TYPE_CHOICES = {PHYSICIAN: "Physician", PHARMACISTS: "Pharmacist"}

    contact_type = models.CharField(
        max_length=20, choices=CONTACT_TYPE_CHOICES, blank=False, null=False
    )
    job_title = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.ForeignKey(
        Specialization, on_delete=models.PROTECT, blank=True, null=True
    )
    medical_license_number = models.CharField(max_length=100, blank=True, null=True)
    hospital = models.ForeignKey(
        Hospital, on_delete=models.PROTECT, blank=True, null=True
    )


class Patient(Contact):
    is_lead = models.BooleanField(default=False)
    first_contact_date = models.DateTimeField(blank=True, null=True)
    initial_consult_date = models.DateTimeField(blank=True, null=True)
    medical_condition = models.ForeignKey(
        MedicalCondition, on_delete=models.PROTECT, blank=True, null=True
    )
    physician = models.ForeignKey(
        Specialist, on_delete=models.PROTECT, blank=True, null=True
    )


class Booking(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, blank=False, null=False
    )
    booking_date = models.DateTimeField()
    reminder_date = models.DateTimeField()

    def __str__(self):
        return f"{self.patient} - {self.booking_date}"


class EAP(models.Model):
    eap_number = models.CharField(max_length=100, blank=False, null=False)
    patients = models.ManyToManyField(Patient, through="EAPDossier")

    def __str__(self):
        return {self.eap_number}


class EAPDossier(models.Model):
    eap_dossier_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, blank=False, null=False
    )
    eap = models.ForeignKey(EAP, on_delete=models.PROTECT, blank=False, null=False)
    eap_enrollment_date = models.DateTimeField()

    def __str__(self):
        return f"{self.eap} - {self.patient}"


class ClinicalTrial(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    patients = models.ManyToManyField(Patient, through="CTReferall")

    def __str__(self):
        return {self.name}


class CTReferall(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, blank=False, null=False
    )
    ct = models.ForeignKey(
        ClinicalTrial, on_delete=models.PROTECT, blank=False, null=False
    )
    eligible = models.BooleanField(blank=False, null=False)
    ineligible_reason = models.CharField(max_length=200, blank=True, null=True)
    ct_referral_date = models.DateTimeField()
    ct_outcome = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.ct} - {self.patient}"
