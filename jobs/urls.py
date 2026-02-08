from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'jobs', views.JobViewSet, basename='job')

urlpatterns = [
    # Application management
    path('applications/status', views.update_application_status, name='update-application-status'),
    path('applications/my', views.my_applications, name='my-applications'),
    path('jobs/<int:job_id>/applications/<int:worker_id>', views.remove_worker_from_job, name='remove-worker'),
    
    # Job routes (includes apply endpoint as action)
    path('', include(router.urls)),
]
