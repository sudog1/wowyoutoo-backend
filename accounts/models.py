from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser


class UserManager(BaseUserManager):

    """ 사용자 모델을 생성하고 관리하는 클래스입니다. """

    def create_user(self, email, password, nickname):
        """ 일반 사용자를 생성하는 메서드입니다. """
        if not email:
            raise ValueError('유효하지 않은 이메일 형식입니다.')

        user = self.model(
            email=self.normalize_email(email),
            password=password,
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, nickname):
        """ 관리자를 생성하는 메서드입니다. """
        if not email:
            raise ValueError('유효하지 않은 이메일 형식입니다.')

        user = self.create_user(
            email,
            password=password,
            nickname=nickname,
        )

        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = None
    nickname = models.CharField("닉네임", max_length=30)
    password = models.CharField("비밀번호", max_length=255)
    email = models.EmailField(unique=True)
    profile_img = models.ImageField(
        upload_to="media/userProfile",
        default="media/userProfile/default.png",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField("관리자 여부", default=False)
    updated_at = models.DateField("수정일", auto_now=True)
    verified = models.BooleanField(default=False)
    agree_terms = models.BooleanField("서비스 이용약관 동의", default=False, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "nickname"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


# class English_Level(models.Model):
#     LEVEL_CHOICES = [
#         ('BASIC', 'Basic'),
#         ('INTERMEDIATE', 'Intermediate'),
#         ('ADVANCE', 'Advance'),
#     ]
#     level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
