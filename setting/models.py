from django.db import models
from django.contrib.auth.models import User # type: ignore
from accounts.models import User

# Create your models here.
class SettingCategory(models.Model):
    setting_name=models.CharField(max_length=200)
    description=models.TextField()

    def __str__(self):
        return self.setting_name

class Setting(models.Model):
    category_id = models.ForeignKey(SettingCategory, on_delete=models.CASCADE, related_name='settings')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    data_type = models.CharField(max_length=20, choices=[
        ('string', 'String'),
        ('integer', 'Integer'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
    ])
    default_value = models.TextField()

    def __str__(self):
        return self.name



class SystemSetting(models.Model):
    setting = models.ForeignKey('Setting', on_delete=models.CASCADE, related_name='system_settings')
    value = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    updated_by_user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_override = models.BooleanField(default=True)

    class Meta:
        unique_together = ['setting']

    def __str__(self):
        return f"{self.setting.key}: {self.value}"

    def save(self, *args, **kwargs):
        # Custom logic to validate value based on setting.data_type
        # For example:
        if self.setting.data_type == 'integer':
            self.value = int(self.value)
        elif self.setting.data_type == 'boolean':
            self.value = str(bool(self.value)).lower()
        super().save(*args, **kwargs)


class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    theme = models.CharField(max_length=20, default='light')
    notifications_enabled = models.BooleanField(default=True)
    language = models.CharField(max_length=10, default='en')
    daily_email_digest=models.BooleanField(default=False)
    privacy_level =models.IntegerField(default=0,db_comment="0 for private and 1 for public")

    def __str__(self):
        return f"{self.user.username}'s settings"