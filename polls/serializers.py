from .models import Poll, Question, UserAnswer, AnswerChoice
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    owner_polls = serializers.PrimaryKeyRelatedField(many=True, queryset=Poll.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'owner_polls']


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'title_question', 'type_question', 'poll_question', 'answers']


class PollSerializer(serializers.ModelSerializer):

    owner_poll = serializers.ReadOnlyField(source='owner_poll.username')
    question_poll = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        # fields = '__all__'
        fields = ('owner_poll', 'title_poll', 'description_poll', 'start_date_poll', 'end_date_poll', 'question_poll')
        ordering = ('title_poll',)


class AnswerChoiceSerializer(serializers.ModelSerializer):

    answers = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = AnswerChoice
        fields = ('answer_title', 'answer', 'answers')


class UserAnswerSerializer(serializers.ModelSerializer):

    type_question = QuestionSerializer(read_only=True)

    class Meta:
        model = UserAnswer
        fields = ('type_question',)