from rest_framework import serializers
from .models import Job, Application
from django.contrib.auth import get_user_model

User = get_user_model()


class EmployerSerializer(serializers.ModelSerializer):
    """Serializer for employer details in job listings"""
    
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'city')


class WorkerSerializer(serializers.ModelSerializer):
    """Serializer for worker details in applications"""
    
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'city', 'profile_photo')


class JobCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating jobs"""
    
    class Meta:
        model = Job
        fields = ('title', 'description', 'daily_wage', 'required_workers')
    
    def create(self, validated_data):
        """Create job with employer from request"""
        request = self.context.get('request')
        validated_data['employer'] = request.user
        return super().create(validated_data)


class JobListSerializer(serializers.ModelSerializer):
    """Serializer for listing jobs"""
    employer = EmployerSerializer(read_only=True)
    available_slots = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Job
        fields = ('id', 'employer', 'title', 'description', 'daily_wage', 
                  'required_workers', 'filled_slots', 'available_slots', 
                  'status', 'created_at')
        read_only_fields = ('id', 'filled_slots', 'status', 'created_at')


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating applications"""
    
    class Meta:
        model = Application
        fields = []  # No fields needed, job and worker are set automatically
    
    def validate(self, attrs):
        """Validate application constraints"""
        request = self.context.get('request')
        job = self.context.get('job')
        
        # Check if job is closed
        if job.status == 'closed':
            raise serializers.ValidationError("This job is no longer accepting applications")
        
        # Check if user has already applied
        if Application.objects.filter(job=job, worker=request.user).exists():
            raise serializers.ValidationError("You have already applied for this job")
        
        return attrs


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for application details"""
    worker = WorkerSerializer(read_only=True)
    job = JobListSerializer(read_only=True)
    
    class Meta:
        model = Application
        fields = ('id', 'job', 'worker', 'status', 'applied_at', 'updated_at')
        read_only_fields = ('id', 'applied_at', 'updated_at')


class ApplicationStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating application status"""
    status = serializers.ChoiceField(choices=['accepted', 'rejected'])
