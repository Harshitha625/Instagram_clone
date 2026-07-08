from . models import Notifications

def notification_count(request):
    if request.user.is_authenticated:
        count = Notifications.objects.filter(
            receiver = request.user,
            is_read = False
        ).count()
    else:
        count = 0;

    return {
        "notification_count" : count
    }