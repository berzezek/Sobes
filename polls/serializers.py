from .models import *
from django.contrib.auth.models import User
from rest_framework.serializers import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class PollSerializer(ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerChoiceSerializer(ModelSerializer):
    question = PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())

    class Meta:
        model = AnswerChoice
        fields = ('answer_title', 'question')


class UserAnswerSerializer(ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'


# class Poll2Serializer(Serializer):
#     pk = IntegerField(read_only=True)
#     owner_poll = UserSerializer()
#     # title_poll = CharField(max_length=255, style={'placeholder': 'Наименование опроса', 'autofocus': True})
#     # description_poll = CharField(max_length=255)
#     start_date_poll = DateField(required=False)
#     end_date_poll = DateField(required=False)
#
#     class Meta:
#         model = Poll
#         fields = '__all__'
