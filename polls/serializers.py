from .models import Poll, Question, UserAnswer
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']


class PollSerializer(serializers.ModelSerializer):

    owner_poll = UserSerializer()

    class Meta:
        model = Poll
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    poll_question = PollSerializer()
    type_question = serializers.CharField(source='get_type_question_display')

    class Meta:
        model = Question
        fields = '__all__'


class UserAnswerSerializer(serializers.ModelSerializer):

    user_name = UserSerializer()
    user_poll = PollSerializer()
    user_question = QuestionSerializer()
    user_answer_choice = QuestionSerializer()
    user_answer_multi = QuestionSerializer()

    class Meta:
        model = UserAnswer
        fields = '__all__'
