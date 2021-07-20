from rest_framework.serializers import ModelSerializer
from .models import Poll, Question, UserAnswer


class PollSerializers(ModelSerializer):

    class Meta:
        model = Poll
        fields = '__all__'


class QuestionSerializers(ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class UserAnswerSerializers(ModelSerializer):

    class Meta:
        model = UserAnswer
        fields = '__all__'