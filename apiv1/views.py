from rest_framework import viewsets, routers
from task.models import Task
from .serializers import TaskSerializer
# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        L_id = self.request.query_params.get('id')

        if L_id:
            queryset = queryset.filter(id=L_id)
        return queryset
