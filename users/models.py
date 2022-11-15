from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


class Area(models.Model):
    """エリア"""
    name = models.CharField(_("name"), max_length=20)
    e_name = models.CharField("英語表記", max_length=20)
    sort_no = models.IntegerField("表示順番")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "エリア"
        verbose_name_plural = "エリア"


class Office(models.Model):
    """事務所(カスタムユーザーで使用)"""
    name = models.CharField(_("name"), max_length=30)
    area = models.ManyToManyField(
        Area, verbose_name="エリア", related_name="area")
    sort_no = models.IntegerField("表示順番")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "事務所"
        verbose_name_plural = "事務所"


class Job(models.Model):
    """職種"""
    name = models.CharField(_("name"), max_length=20)
    e_name = models.CharField("英語表記", max_length=20)
    sort_no = models.IntegerField("表示順番")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "職種"
        verbose_name_plural = "職種"


class PhoneType(models.Model):
    """携帯電話の種類（ユーザー追加情報モデルで使用）"""
    name = models.CharField("携帯電話種別", max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "携帯種別"
        verbose_name_plural = "携帯種別"


class Profile(models.Model):
    """ユーザープロフィールモデル"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_name = models.CharField("性", max_length=50, blank=True)
    first_name = models.CharField("名", max_length=50, blank=True)
    birthday = models.DateField("生年月日", null=True, blank=True)
    phone = models.CharField("携帯番号", max_length=13, blank=True)
    phone_type = models.ForeignKey(PhoneType, verbose_name="携帯種別",
                                   on_delete=models.CASCADE, null=True)
    office = models.ForeignKey(
        Office, verbose_name="事務所", null=True, on_delete=models.CASCADE)
    default_area = models.ForeignKey(
        Area, verbose_name="メインエリア", null=True, on_delete=models.CASCADE)
    default_job = models.ForeignKey(
        Job, verbose_name="メイン職種", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "プロフィール"
        verbose_name_plural = "プロフィール"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Emailを入力して下さい')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff=Trueである必要があります。')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser=Trueである必要があります。')
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_("username"), max_length=30, validators=[
                                username_validator], unique=True)
    email = models.EmailField(_("email_address"), unique=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    """ 新ユーザー作成時に空のprofileも作成する """
    if kwargs['created']:
        user_profile = Profile.objects.get_or_create(user=kwargs['instance'])
