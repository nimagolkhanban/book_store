from rest_framework import serializers


def validate_email(value):
    if 'admin' in value:
        raise serializers.ValidationError('admin cant be inside your email address')


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, validators=[validate_email])
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_username(self, username):
        if username == "admin":
            raise serializers.ValidationError("username cant be admin")
        return username

    def validate(self, obj):
        if obj["password"] != obj["password2"]:
            raise serializers.ValidationError("passwords don't match")
        return obj
