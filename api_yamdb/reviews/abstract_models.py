from django.db import models


class AbstractContentModel(models.Model):
    """
    Абстрактная модель для модели Genre и Category.
    """

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        help_text='Неофициальное имя, часть URL адреса',
    )

    class Meta:
        abstract = True


class AbstractReviewCommentModel(models.Model):
    """
    Абстрактная модель для модели Review и Comment.
    """

    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        help_text='Выберите автора.',
    )

    class Meta:
        abstract = True
