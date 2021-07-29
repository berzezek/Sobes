from .models import Poll, Question, UserAnswer, AnswerChoice
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    owner_polls = serializers.PrimaryKeyRelatedField(many=True, queryset=Poll.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'owner_polls']


class AnswerChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerChoice
        fields = ('answer_title',)


class QuestionSerializer(serializers.ModelSerializer):

    type_question = serializers.CharField(source='get_type_question_display')
    answers = AnswerChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'title_question', 'type_question', 'answers']


class PollSerializer(serializers.ModelSerializer):

    # owner_poll = serializers.ReadOnlyField(source='owner_poll.username')
    # question_poll = QuestionSerializer(many=True)
    # start_date_poll = serializers.DateField()

    class Meta:
        model = Poll
        # fields = '__all__'
        fields = ('owner_poll', 'title_poll', 'description_poll', 'start_date_poll', 'end_date_poll')
        ordering = ('title_poll',)


class UserAnswerSerializer(serializers.ModelSerializer):

    user_name = serializers.ReadOnlyField(source='user_name.username')
    # user_poll = PollSerializer()
    # user_question = QuestionSerializer()
    # user_answer_choice = serializers.CharField()
    # user_answer_multi = AnswerChoiceSerializer(many=True, required=False)

    class Meta:
        model = UserAnswer

        fields = ('id', 'user_name', 'user_poll', 'user_question', 'user_answer_text', 'user_answer_choice',
                  'user_answer_multi')