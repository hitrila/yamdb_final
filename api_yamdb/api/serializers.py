import datetime

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from rest_framework import serializers

from reviews.models import Title, Category, Genre, Review, Comment, User
from .email import ConfirmationCodeEmailMessage
from .validators import username_validator


class SignUpSerializer(serializers.Serializer):
    """
    Сериализатор аутентификации пользователя.
    """

    username = serializers.CharField(
        max_length=150,
        required=True,
        label='Имя пользователя',
        validators=[
            UnicodeUsernameValidator(),
            username_validator,
        ],
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        label='Эл.почта',
    )

    def create(self, validated_data):
        """
        Метод создания модели пользователя.
        :param validated_data: Валидный данные.
        :return: Модель User.
        """

        try:
            user, _ = User.objects.get_or_create(**validated_data)
        except IntegrityError as error:
            # Получение поля, из-за которого произошла ошибка ограничения на
            # уникальность.
            error = error.args[0].split()
            field_error = error[-1].split('.')[-1]
            data = {
                field_error: (
                    'Имя пользователя или эл.почта занята другим '
                    'пользователем.'
                )
            }
            raise serializers.ValidationError(detail=data)
        confirmation_code = default_token_generator.make_token(user=user)
        email_sender = ConfirmationCodeEmailMessage()
        email_sender.send_confirmation_code_email(
            username=user.username,
            email=user.email,
            confirmation_code=confirmation_code,
        )
        return user


class TokenCreateSerializer(serializers.Serializer):
    """
    Сериализатор создания токенов.
    """

    username = serializers.CharField(
        max_length=150,
        required=True,
        label='Имя пользователя',
        validators=[
            UnicodeUsernameValidator(),
            username_validator,
        ],
    )
    confirmation_code = serializers.CharField(
        required=True,
        label='Код подтверждения',
    )


class TokenResponseSerializer(serializers.Serializer):
    """
    Сериализатор созданного токена.
    """

    token = serializers.CharField(label='Токен')


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категорий.
    """

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанров.
    """

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор произведений на GET запрос.
    """

    genre = GenreSerializer(many=True, label='Жанры')
    category = CategorySerializer(label='Категория')
    rating = serializers.IntegerField(
        read_only=True,
        label='Рейтинг',
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )


class TitlePostPatchSerializer(serializers.ModelSerializer):
    """
    Сериализатор произведений на POST запрос.
    """

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
        label='Жанры',
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), label='Категория'
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )

    def validate_year(self, value: int):
        if value > datetime.date.today().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор отзывов
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        label='Автор',
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )

    def validate(self, attrs):
        author = self.context['request'].user
        title_id = (
            self.context['request']
            .parser_context.get('kwargs')
            .get('title_id')
        )
        method = self.context['request'].method
        if (
            method == 'POST'
            and Review.objects.filter(
                author=author, title__id=title_id
            ).exists()
        ):
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв к этому произведению!'
            )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор комментариев
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        label='Автор',
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя.
    """

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'role',
            'bio',
            'email',
        )
