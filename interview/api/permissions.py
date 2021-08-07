from rest_framework.permissions import BasePermission
from datetime import date
# from .models import Category


class IsStartDateBegin(BasePermission):
    message = 'Вы не можете изменять опрос после начала'

    def has_object_permission(self, request, view, obj):
        # start_date = Category.objects.get(start_date__lte=date.today())
        my_safe_method = ['GET']
        if request.method in my_safe_method:
            return obj.start_date > date.today()
