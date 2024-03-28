from energy_base.api.routers import OptionalSlashRouter

from energy_base.q_api.views import TaskViewSet, ScheduleViewSet

router = OptionalSlashRouter()
router.register('tasks', TaskViewSet, basename='tasks')
router.register('schedules', ScheduleViewSet, basename='schedules')

urlpatterns = [
]

urlpatterns += router.urls
