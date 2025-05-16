import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email).lower()

        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_pro_user(self, email, name, password=None):
        """Tworzy użytkownika Pro"""
        user = self.create_user(email, name, password)
        user.role = UserAccount.Role.USER_PRO
        user.is_pro = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """Tworzy administratora"""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.role = UserAccount.Role.ADMIN
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER_BASE = "USER_BASE", "Base User"
        USER_PRO = "USER_PRO", "Pro User"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.USER_BASE)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Flaga dla użytkowników Pro
    is_pro = models.BooleanField(default=False)

    # Dane dotyczące ciała
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def upgrade_to_pro(self):
        """Prosta metoda zmiany użytkownika na Pro"""
        self.role = self.Role.USER_PRO
        self.is_pro = True
        self.save()

    def downgrade_to_base(self):
        """Zmiana użytkownika Pro na zwykłego"""
        self.role = self.Role.USER_BASE
        self.is_pro = False
        self.save()


class WeightEntry(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="weight_entries")
    date = models.DateField(auto_now_add=True)  # Data automatycznie ustawiana na dzień dodania
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ["-date"]  # Ostatnia waga na górze

    def __str__(self):
        return f"{self.user.email} - {self.weight} kg on {self.date}"

    