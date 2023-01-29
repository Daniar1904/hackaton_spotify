from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)
    password2 = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'last_name', 'first_name', 'username', 'avatar')

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs['password'] != password2:
            raise serializers.ValidationError('Passwords did not match!')
        if not attrs['password'].isalnum():
            raise serializers.ValidationError('Password field must contain'
                                              'alpha and numeric symbols')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {'bad_token': _('Token is invalid or expired!')}

    def validate(self, attrs):
        print(attrs, '!!!!!!!!!!!!!!!')
        self.token = attrs['refresh']
        return attrs

    def save(self):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#
#     @staticmethod
#     def validate_email(email):
#         if not User.objects.filter(email=email).exists():
#             raise serializers.ValidationError('нет такого зарегистрированного пользователя')
#         return email
#
#     def create(self, validated_data):
#         user = User.objects.get(email=validated_data['email'])
#         user.create_activation_code()
#         user.save()
#         tasks.send_user_forgot_password_code.delay(email=user.email, activation_code=user.activation_code)
#         return user
#
#
# class ForgotPasswordConfirmSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     code = serializers.CharField(required=True, write_only=True)
#     password = serializers.CharField(required=True, write_only=True, min_length=6, max_length=128)
#     password_repeat = serializers.CharField(required=True, write_only=True, min_length=6, max_length=128)
#
#     def validate(self, attrs):
#         p1 = attrs['password']
#         p2 = attrs['password_repeat']
#         if p1 != p2:
#             return serializers.ValidationError('Пароли не совпадают')
#         return attrs
#
#     @staticmethod
#     def validate_email(email):
#         if not User.objects.filter(email=email).exists():
#             raise serializers.ValidationError('нет такого зарегистрированного пользователя')
#         return email
#
#     @staticmethod
#     def validate_code(code):
#         if not User.objects.filter(activation_code=code).exists():
#             raise serializers.ValidationError('неправильный код подтверждения')
#         return code
#
#     def create(self, validated_data):
#         user = User.objects.get(email=validated_data['email'])
#         user.set_password(validated_data['password'])
#         user.activation_code = ''
#         user.save()
#         return user
#
#     class ChangePasswordSerializer(serializers.Serializer):
#         old_password = serializers.CharField(required=True, min_length=6, write_only=True)
#         new_password = serializers.CharField(required=True, min_length=6, write_only=True)
#         new_password_repeat = serializers.CharField(required=True, min_length=6, write_only=True)
#
#         def validate_old_password(self, old_password):
#             user = self.context.get('request').user
#             if not user.check_password(old_password):
#                 raise serializers.ValidationError('Старый пароль введен неверно')
#             return old_password
#
#         def validate(self, attrs):
#             p1 = attrs['new_password']
#             p2 = attrs['new_password_repeat']
#             if p1 != p2:
#                 raise serializers.ValidationError('Пароли не совпадают')
#             return attrs
#
#         def create(self, validated_data):
#             user = self.context.get('request').user
#             user.set_password(validated_data['new_password'])
#             user.save()
#             return user