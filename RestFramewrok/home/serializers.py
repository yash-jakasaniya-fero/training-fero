from rest_framework import serializers
from .models import Color, Person
from django.contrib.auth.models import User



class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('username is taken')

        if data['email']:
            if User.objects.filter(mail = data['email']).exists():
                raise serializers.ValidationError('email is taken')

        return data

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
        print(validated_data)



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = ['color_name']

class PeopleSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    color_info = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = '__all__'
        # depth = 1

    def get_color_info(self, instance):
        if instance.color:
            color_obj = Color.objects.get(id=instance.color.id)
            return { "color_name": color_obj.color_name, "color":"#000" }
        return None

    # def get_country(self, obj):
    #     return "India"


    def validate(self, data):
            special_characters = "!@#$%^&*()-+?_=,<>/"
            if any (c in special_characters for c in data['name']):
                raise serializers.ValidationError('Name cannot contain special chars')

            if data['age'] < 18:
                raise serializers.ValidationError('age should be greator than 18')

            return data