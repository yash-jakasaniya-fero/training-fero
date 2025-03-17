from django.db import models


class Contact(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ContactNumbers(models.Model):
    TYPE_CHOICES = [
        ('Home', 'Home'),
        ('Work', 'Work'),
        ('Other', 'Other'),
    ]
    contact = models.ForeignKey(Contact, related_name="contact_numbers", on_delete=models.CASCADE)
    contact_type = models.CharField(choices=TYPE_CHOICES, max_length=10)
    contact_number = models.CharField(max_length=15,)

    def __str__(self):
        return f"{self.contact_type}: {self.contact_number}"