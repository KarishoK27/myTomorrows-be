import factory
from api.models import (
    EAP,
    ClinicalTrial,
    Contact,
    Hospital,
    MedicalCondition,
    Patient,
    Specialist,
    Specialization,
)
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText


class MedicalConditionFactory(DjangoModelFactory):
    class Meta:
        model = MedicalCondition

    name = FuzzyText(length=10)
    abbreviation = FuzzyText(length=10)


class SpecializationFactory(DjangoModelFactory):
    class Meta:
        model = Specialization

    name = FuzzyText(length=10)


class HospitalFactory(DjangoModelFactory):
    class Meta:
        model = Hospital

    name = FuzzyText(length=10)
    city = FuzzyText(length=10)


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact
        abstract = True

    firstname = FuzzyText(length=10)
    lastname = FuzzyText(length=10)
    email = f"{FuzzyText(length=5)}@text.com"


class SpecialistFactory(ContactFactory):
    class Meta:
        model = Specialist

    contact_type = factory.Faker(
        "random_element", elements=["PHYSICIAN", "PHARMACISTS"]
    )
    job_title = FuzzyText(length=10)
    specialization = factory.SubFactory(SpecializationFactory)
    medical_license_number = FuzzyText(length=10)
    hospital = factory.SubFactory(HospitalFactory)


class PatientFactory(ContactFactory):
    class Meta:
        model = Patient


class EAPFactory(DjangoModelFactory):
    class Meta:
        model = EAP

    eap_number = factory.Faker("bothify", text="EAP####")


class ClinicalTrialFactory(DjangoModelFactory):
    class Meta:
        model = ClinicalTrial

    name = factory.Faker("company")
