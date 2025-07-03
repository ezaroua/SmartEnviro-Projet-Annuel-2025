from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from .models import Role

User = get_user_model()

# ─────────  A) Sérialiseur JWT  ────────────────
class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role_id"] = user.role_id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["role_id"] = self.user.role_id
        return data

# ─────────  B) Lecture Utilisateur  ────────────────
class UserSerializer(serializers.ModelSerializer):
    role_id = serializers.IntegerField(source='role.id', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role_id', 'role_name', 'phone_number', 'address',
            'preferred_district', 'receive_alerts',
            'is_active', 'date_joined'
        ]
        read_only_fields = ('id', 'date_joined', 'role_id', 'role_name', 'is_active')

# ─────────  C) Inscription  ────────────────
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, label='Confirmation')

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name',
            'phone_number', 'address',
            'preferred_district', 'receive_alerts'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'email': {'required': True},
            'username': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Les mots de passe ne correspondent pas.'})
        password_validation.validate_password(attrs['password'], self.instance)
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')

        # Attribution automatique du rôle "citizen"
        citizen_role = Role.objects.filter(name='citizen').first()
        if not citizen_role:
            raise serializers.ValidationError({'role': "Le rôle 'citizen' est introuvable. Veuillez le créer dans l'admin."})

        user = User(**validated_data, role=citizen_role)
        user.set_password(password)
        user.save()
        return user

# ─────────  D) Profil Utilisateur connecté  ────────────────
class ProfileSerializer(serializers.ModelSerializer):
    role_id = serializers.IntegerField(source='role.id', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name',
            'phone_number', 'address',
            'preferred_district', 'receive_alerts',
            'role_id', 'role_name', 'date_joined'
        ]
        read_only_fields = ('id', 'username', 'role_id', 'role_name', 'date_joined')

# ─────────  E) Changement de mot de passe  ────────────────
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_conf = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Ancien mot de passe incorrect.")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_conf']:
            raise serializers.ValidationError({"new_password": "Les mots de passe ne correspondent pas."})
        password_validation.validate_password(attrs['new_password'], self.context['request'].user)
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
