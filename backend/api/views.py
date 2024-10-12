from api.models import Patient, Specialist
from api.permissions import IsAdminOrCreateReadOnly
from api.serializers import PatientSerializer, SpecialistSerializer
from rest_framework import permissions, viewsets


class SpecialistViewSet(viewsets.ModelViewSet):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer
    permission_classes = [permissions.IsAuthenticated]


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminOrCreateReadOnly]
