from rest_framework import serializers
from .models import Job

from rest_framework import serializers
from .models import Job

class JobModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Salary cannot be a negative value.")
        return value

class JobSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    company_name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    location = serializers.CharField(max_length=255)
    salary = serializers.IntegerField(required=False, allow_null=True)
    posted_at = serializers.DateTimeField(read_only=True)

    def validate_salary(self, value):
        return JobModelSerializer().validate_salary(value)

    def create(self, validated_data):
        return Job.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.description = validated_data.get('description', instance.description)
        instance.location = validated_data.get('location', instance.location)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.save()
        return instance
