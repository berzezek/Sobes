from rest_framework import serializers
from main.interview.models import Category, Question, Choice, Answer


class CategoryModelSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='interview-api:category_detail',
    )
    delete_url = serializers.HyperlinkedIdentityField(
        view_name='interview-api:category_delete',
    )
    post_detail_url = serializers.HyperlinkedIdentityField(
        view_name='interview-api:category_delete',
    )

    class Meta:
        model = Category
        # fields = '__all__'
        exclude = ('owner',)


class QuestionModelSerializer(serializers.ModelSerializer):

    # category = serializers.PrimaryKeyRelatedField(many=True, label='Категория', queryset=Category.objects.all(),
    #                                               style={'base_template': 'select.html'})

    class Meta:
        model = Question
        fields = '__all__'
        # exclude = ('choice',)


class ChoiceModelSerializer(serializers.ModelSerializer):

    # question = QuestionModelSerializer(read_only=True)

    class Meta:
        model = Choice
        fields = '__all__'


class AnswerModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'
