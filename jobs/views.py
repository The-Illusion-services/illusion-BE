from rest_framework import viewsets
from jobs.models import Job, Application
from serializers.serializers import JobSerializer, ApplicationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import JobFilter
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobFilter


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

    @action(detail=False, methods=['get'])
    def my_applications(self, request):
        my_apps = Application.objects.filter(applicant=request.user)
        serializer = self.get_serializer(my_apps, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        application = self.get_object()
        if application.applicant != request.user:
            return Response({"detail": "You can only withdraw your own applications."},
                            status=status.HTTP_403_FORBIDDEN)
        application.status = 'withdrawn'
        application.save()
        return Response({"detail": "Application withdrawn successfully."},
                        status=status.HTTP_200_OK)
    
    
