from rest_framework import serializers
from .models import NewTask

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewTask
        fields = '__all__'
