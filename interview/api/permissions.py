from rest_framework.permissions import BasePermission
from datetime import date
from ..models import Category


class IsStartDateBegin(BasePermission):
    message = 'Вы не можете изменять опрос после начала'

    def has_object_permission(self, request, view, obj):
        print(Category.objects.filter(title=obj).filter(start_date__lte=date.today()))
        if Category.objects.filter(title=obj).filter(start_date__lte=date.today()):
            return False
        else:
            return True
