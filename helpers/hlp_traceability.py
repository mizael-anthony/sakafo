from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class TraceabilityHelpers():
    def get_datetime_now():
        """Get current datetime"""
        return datetime.datetime.now(tz=timezone.utc)

    def get_current_user(request):
        """Get current user"""
        return User.objects.get(pk=request.user.id) 