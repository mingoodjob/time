from pyexpat import model
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an username')
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            # username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class UserModel(AbstractBaseUser):
    # username = models.CharField("사용자 계정", max_length=20, unique=True)
    email = models.EmailField("이메일", unique=True)
    password = models.CharField("비밀번호", max_length=128)
    fullname = models.CharField("이름", max_length=20)
    user_type = models.CharField("사용자 타입", max_length=20, default="user")
    join_date = models.DateTimeField("가입일", auto_now_add=True)
    def __str__(self):
        return self.email


		# is_active가 False일 경우 계정이 비활성화됨
    is_active = models.BooleanField(default=True) 

    # is_staff에서 해당 값 사용
    is_admin = models.BooleanField(default=False)
    
    # id로 사용 할 필드 지정.
    # 로그인 시 USERNAME_FIELD에 설정 된 필드와 password가 사용된다.
    USERNAME_FIELD = 'email'

    # user를 생성할 때 입력받은 필드 지정
    REQUIRED_FIELDS = []
    
    objects = UserManager() # custom user 생성 시 필요
    
    def __str__(self):
        return self.email

    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_perm(self, perm, obj=None):
        return True
    
    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_module_perms(self, app_label): 
        return True
    
    # admin 권한 설정
    @property
    def is_staff(self): 
        return self.is_admin


class UserType(models.Model):
    useremail = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    candidate = models.CharField("지원자", max_length=20)
    recruiter = models.CharField("채용자", max_length=20)


    def __str__(self):
        return self.candidate


class UserLog(models.Model):
    useremail = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    apply_date = models.DateTimeField("지원일")   
    login_date = models.DateTimeField("로그인일")
    logout_date = models.DateTimeField("로그아웃일")

# class UserProfile(models.Model):
#     user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
#     nickname = models.CharField("닉네임", max_length=20, blank=True)
#     phone = models.CharField("전화번호", max_length=20, blank=True)
#     address = models.CharField("주소", max_length=100, blank=True)
#     hobby = models.CharField("취미", max_length=100, blank=True)

#     def __str__(self):
#         return self.nickname
