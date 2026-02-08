from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Job(models.Model):
    """Job posting model"""
    
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posted_jobs',
        limit_choices_to={'role': 'employer'}
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    daily_wage = models.DecimalField(max_digits=10, decimal_places=2)
    required_workers = models.PositiveIntegerField()
    filled_slots = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.employer.full_name}"
    
    def clean(self):
        """Validate that filled_slots doesn't exceed required_workers"""
        if self.filled_slots > self.required_workers:
            raise ValidationError('Filled slots cannot exceed required workers')
    
    def save(self, *args, **kwargs):
        """Auto-close job if all slots are filled"""
        if self.filled_slots >= self.required_workers:
            self.status = 'closed'
        super().save(*args, **kwargs)
    
    @property
    def available_slots(self):
        """Return number of available slots"""
        return self.required_workers - self.filled_slots
    
    class Meta:
        db_table = 'jobs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['employer']),
        ]


class Application(models.Model):
    """Job application model"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
        limit_choices_to={'role': 'worker'}
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.worker.full_name} -> {self.job.title} ({self.status})"
    
    class Meta:
        db_table = 'applications'
        ordering = ['-applied_at']
        unique_together = [['job', 'worker']]  # Prevent duplicate applications
        indexes = [
            models.Index(fields=['job', 'status']),
            models.Index(fields=['worker', 'status']),
        ]
