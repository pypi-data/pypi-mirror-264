from django_q.models import Schedule
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from energy_base.q_api.permissions import IsSuperUser
from energy_base.q_api.serializers import ScheduleSerializer


@extend_schema(tags=['admin/schedules'])
class ScheduleViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch']
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsSuperUser]
