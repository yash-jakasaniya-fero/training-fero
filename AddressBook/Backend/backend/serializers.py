from django.core.validators import EmailValidator
from rest_framework import serializers
from .models import Contact, ContactNumbers



class ContactSerializer(serializers.ModelSerializer):
    contact_numbers = serializers.ListField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'email', 'contact_numbers']

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if Contact.objects.filter(first_name=first_name, last_name=last_name).exists():
            raise serializers.ValidationError("A contact with this first name and last name already exists.")
        return data

    def create(self, validated_data):
        contact_numbers_data = validated_data.pop('contact_numbers', [])
        instance = super().create(validated_data)


        for contact_number_data in contact_numbers_data:
            ContactNumbers.objects.create(contact=instance, **contact_number_data)

        return instance

    def update(self, instance, validated_data):
        contact_numbers_data = validated_data.pop('contact_numbers', [])

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        instance.contact_numbers.all().delete()
        for contact_number_data in contact_numbers_data:
            ContactNumbers.objects.create(contact=instance, **contact_number_data)

        return instance


class ContactNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactNumbers
        fields = ['contact_type','contact_number']


class ContactListSerializer(serializers.ModelSerializer):
    contact_numbers = serializers.SerializerMethodField()
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'email', 'contact_numbers']

    def get_contact_numbers(self, instance):
        contact_numbers = instance.contact_numbers.all()
        return ContactNumberSerializer(contact_numbers, many=True).data


class ContactXLSXSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="contact.first_name", read_only=True)
    last_name = serializers.CharField(source="contact.last_name", read_only=True)
    email = serializers.EmailField(source="contact.email", read_only=True)

    class Meta:
        model = ContactNumbers
        fields = ["first_name" ,"last_name","email","contact_type", "contact_number"]


class ContactXLSXUploadSerializer(serializers.ModelSerializer):
    contact_type = serializers.CharField()
    contact_number = serializers.CharField()
    email = serializers.CharField(validators=[EmailValidator()])

    class Meta:
        model = Contact
        fields = ["id", "first_name", "last_name", "email", "contact_type", "contact_number"]

    def validate_contact_type(self, value):
        valid_choices = {choice[0] for choice in ContactNumbers.TYPE_CHOICES}
        if value not in valid_choices:
            raise serializers.ValidationError(f"Invalid contact_type. Allowed values: {valid_choices}")
        return value

    def validate_contact_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Invalid Contact Number")
        return value

    def create(self, validated_data):
        contact_number_data = {
            "contact_type": validated_data.pop("contact_type"),
            "contact_number": validated_data.pop("contact_number"),
        }

        contact_instance, created = Contact.objects.get_or_create(**validated_data)

        contact_number_instance, created = ContactNumbers.objects.get_or_create(
            contact=contact_instance,
            contact_type=contact_number_data["contact_type"],
            defaults={"contact_number": contact_number_data["contact_number"]}
        )

        if not created:
            contact_number_instance.contact_number = contact_number_data["contact_number"]
            contact_number_instance.save()

        # try:
        #     contact_number_instance = ContactNumbers.objects.get(
        #         contact=contact_instance, contact_type=contact_number_data["contact_type"]
        #     )
        #     contact_number_instance.contact_number = contact_number_data["contact_number"]
        #     contact_number_instance.save()
        # except ContactNumbers.DoesNotExist:
        #     ContactNumbers.objects.create(contact=contact_instance, **contact_number_data)
        #
        # return contact_instance