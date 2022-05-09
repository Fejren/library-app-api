from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    # Serializer for user model

    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}

    def create(self, validated_data):
        # Create new user with encrypted password
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # Update a user (in future will work)
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    # Serializer for user auth token
    email = serializers.CharField()
    # name = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        # Validate and auth the user
        email = attrs.get('email')
        # name = attrs.get('name')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            # name=name,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
