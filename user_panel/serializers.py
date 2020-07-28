from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('phone_number', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8
            }
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update the user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """Serialize for the detail user object"""

    class Meta(UserSerializer.Meta):
        fields = (
                'name',
                'email',
                'picture',
                'gender',
                'favorite_question',
        )


class UserPhoneRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('phone_number', 'generated_token')

    
class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""

    model = get_user_model()

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
