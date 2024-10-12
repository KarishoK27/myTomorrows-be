from unittest import TestCase

import pytest
from api.models import Booking, CTReferall, EAPDossier, Patient
from api.test.factories import ClinicalTrialFactory, EAPFactory, PatientFactory
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


@pytest.mark.django_db
class ModelsTestCase(TestCase):
    def setUp(self):
        self.patient = PatientFactory()

    def test_multiple_bookings(self):
        for i in range(5):
            Booking.objects.create(
                patient=self.patient,
                booking_date=f"2024-01-{i+1}",
                reminder_date=f"2024-01-{i+2}",
            )
        assert self.patient.booking_set.count() == 5

    def test_assign_multiple_eaps(self):
        # Create multiple EAPs
        eap1 = EAPFactory()
        eap2 = EAPFactory()
        eap3 = EAPFactory()

        # Assign EAPs to the patient
        EAPDossier.objects.create(
            patient=self.patient, eap=eap1, eap_enrollment_date="2024-01-01"
        )
        EAPDossier.objects.create(
            patient=self.patient, eap=eap2, eap_enrollment_date="2024-02-01"
        )
        EAPDossier.objects.create(
            patient=self.patient, eap=eap3, eap_enrollment_date="2024-03-01"
        )

        # Verify that all three EAPs are assigned
        assigned_eaps = set(
            EAPDossier.objects.filter(patient=self.patient).values_list(
                "eap", flat=True
            )
        )
        expected_eaps = {eap1.id, eap2.id, eap3.id}
        self.assertEqual(assigned_eaps, expected_eaps)

        # Verify that each EAP has only one assignment
        self.assertEqual(EAPDossier.objects.filter(eap=eap1).count(), 1)
        self.assertEqual(EAPDossier.objects.filter(eap=eap2).count(), 1)
        self.assertEqual(EAPDossier.objects.filter(eap=eap3).count(), 1)

    def test_assign_multiple_ct(self):
        # Create multiple clinical trials
        ct1 = ClinicalTrialFactory()
        ct2 = ClinicalTrialFactory()
        ct3 = ClinicalTrialFactory()

        # Assign clinical trials to the patient
        CTReferall.objects.create(
            ct=ct1, patient=self.patient, eligible=True, ct_referral_date="2024-01-01"
        )
        CTReferall.objects.create(
            ct=ct2, patient=self.patient, eligible=True, ct_referral_date="2024-02-01"
        )
        CTReferall.objects.create(
            ct=ct3, patient=self.patient, eligible=True, ct_referral_date="2024-03-01"
        )

        # Verify that all three clinical trials are assigned
        assigned_cts = set(
            CTReferall.objects.filter(patient=self.patient).values_list("ct", flat=True)
        )
        expected_cts = {ct1.id, ct2.id, ct3.id}
        self.assertEqual(assigned_cts, expected_cts)

        # Verify that each clinical trial has only one assignment per patient
        self.assertEqual(
            CTReferall.objects.filter(ct=ct1, patient=self.patient).count(), 1
        )
        self.assertEqual(
            CTReferall.objects.filter(ct=ct2, patient=self.patient).count(), 1
        )
        self.assertEqual(
            CTReferall.objects.filter(ct=ct3, patient=self.patient).count(), 1
        )


class PatientViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.patient = PatientFactory()

    def test_list_patients(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("patient-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count = Patient.objects.all().count()
        self.assertEqual(len(response.data), count)

    def test_authentication_required(self):
        response = self.client.get(reverse("patient-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
