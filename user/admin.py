from django.contrib import admin
from user.models import UserModel, UserType, UserLog

admin.site.register(UserModel)
admin.site.register(UserType)
admin.site.register(UserLog)
