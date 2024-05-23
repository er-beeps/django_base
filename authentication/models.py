from django.db import models,connection
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_login_failed

class User(AbstractUser):
    # add additional fields here
    token=models.CharField(max_length=50,null=True,blank=True)
    is_password_changed = models.BooleanField(default=False)
    current_group_id = models.IntegerField(blank=True,null=True)
    last_activity = models.DateTimeField(
        _('last activity'), default=timezone.now, editable=False)

    
    def __str__(self):
        return self.username

    def update_last_activity(self):
        self.last_activity = timezone.now()
        self.save(update_fields=["last_activity"])
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    return (
        x_forwarded_for.split(",")[0]
        if x_forwarded_for
        else request.META.get("REMOTE_ADDR")
    )



CREATE, READ, UPDATE, DELETE = "Create", "Read", "Update", "Delete"
LOGIN, LOGOUT, LOGIN_FAILED = "Login", "Logout", "Login Failed"
ACTION_TYPES = [
    (CREATE, CREATE),
    (READ, READ),
    (UPDATE, UPDATE),
    (DELETE, DELETE),
    (LOGIN, LOGIN),
    (LOGOUT, LOGOUT),
    (LOGIN_FAILED, LOGIN_FAILED),
]

SUCCESS, FAILED = "Success", "Failed"
ACTION_STATUS = [(SUCCESS, SUCCESS), (FAILED, FAILED)]


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    message = f"{user.username} is logged in with ip:{get_client_ip(request)}"
    ActivityLogs.objects.create(actor=user, action_type=LOGIN, extra_data=message)


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    message = f"Login Attempt Failed for username: {credentials.get('username')} with ip: {get_client_ip(request)}"
    ActivityLogs.objects.create(action_type=LOGIN_FAILED, extra_data=message)
    
class ActivityLogs(models.Model):
    actor = models.ForeignKey(User,models.SET_NULL,null=True,blank=True)
    request_url = models.CharField(_('url'), max_length=256,null=True,blank=True)
    request_method = models.CharField(_('http method'), max_length=10, db_index=True,null=True,blank=True)
    response_code = models.CharField(_('response code'), max_length=3, db_index=True,null=True,blank=True)
    action_type = models.CharField(choices=ACTION_TYPES, max_length=15)
    datetime = models.DateTimeField(_('datetime'), default=timezone.now, db_index=True)
    status = models.CharField(choices=ACTION_STATUS, max_length=7, default=SUCCESS)
    extra_data = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(_('user IP'), null=True, blank=True, db_index=True)
    model = models.CharField(max_length=50,blank=True, null=True)
    class Meta:
        db_table = 'activity_logs'

    def __str__(self) -> str:
        return f"{self.action_type} by {self.actor} on {self.datetime}"