import datetime

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .abstract_models import (
    AbstractContentModel,
    AbstractReviewCommentModel,
)

FIRST_CHARACTERS = 15

ADMIN = 'admin'
USER = 'user'
MODERATOR = 'moderator'
ROLE_CHOICES = [
    (ADMIN, 'Админ'),
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
]


class User(AbstractUser):
    first_name = models.CharField(
        verbose_name='Имя', max_length=150, blank=True
    )
    email = models.EmailField(
        verbose_name='Эл.почта',
        unique=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    @property
    def is_moderator(self) -> bool:
        """
        Проверка, является ли пользователь модеротором.
        :return:
        """

        return self.role == MODERATOR

    @property
    def is_admin(self) -> bool:
        """
        Проверка, является ли пользователь админом.
        :return:
        """

        return self.role == ADMIN


class Category(AbstractContentModel):
    """
    Модель категории.
    """

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Genre(AbstractContentModel):
    """
    Модель жанров.
    """

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """
    Модель произведений.
    """

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    year = models.IntegerField(
        verbose_name='Год издания',
        validators=[MinValueValidator(1900)],
        default=datetime.date.today().year,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        help_text='Выберите категорию.',
        on_delete=models.SET_NULL,
        null=True,
    )
    genre = models.ManyToManyField(Genre, verbose_name='Жанры')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'

    def __str__(self) -> str:
        return f'Название: {self.name}. Год издания: {self.year}'

    def clean(self) -> None:
        """
        Проверка на валидный год выпуска произведения.
        :return: None
        """

        if self.year > datetime.date.today().year:
            raise ValidationError('Год выпуска не может быть больше текущего')


class Review(AbstractReviewCommentModel):
    """
    Модель отзывов.
    """

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        help_text='Выберите произведение.',
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка',
        error_messages={'invalid': ' Оценка должна быть от 1 до 10'},
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'author',
                    'title',
                ],
                name='author_title_unique',
            )
        ]

    def __str__(self) -> str:
        return self.text[:FIRST_CHARACTERS]


class Comment(AbstractReviewCommentModel):
    """
    Модель комментариев.
    """

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        help_text='Выберите отзыв.',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self) -> str:
        return self.text[:FIRST_CHARACTERS]
