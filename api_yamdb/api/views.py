from typing import List, Union

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import (
    Title,
    Category,
    Genre,
    Review,
    Comment,
)
from reviews.filters import TitleFilter
from .custom_viewset import CreateListDestroyModelMixinViewSet
from .permissions import (
    IsAdminOrReadOnly,
    IsSuperuser,
    IsAdmin,
    IsAuthor,
    IsModerator,
)
from .serializers import (
    TitleGetSerializer,
    CategorySerializer,
    GenreSerializer,
    TitlePostPatchSerializer,
    ReviewSerializer,
    CommentSerializer,
    TokenCreateSerializer,
    TokenResponseSerializer,
    SignUpSerializer,
    UserSerializer,
)

User = get_user_model()


@method_decorator(
    name='signup',
    decorator=swagger_auto_schema(
        request_body=SignUpSerializer(),
        responses={status.HTTP_200_OK: SignUpSerializer()},
    ),
)
class SignUpViewSet(viewsets.GenericViewSet):
    """
    GenericViewSet аутентификации пользователя.
    """

    serializer_class = SignUpSerializer
    swagger_tags = ('auth',)

    @action(
        detail=False,
        permission_classes=(permissions.AllowAny,),
        methods=['post'],
        url_path='signup',
    )
    def signup(self, request: Request) -> Response:
        """
        Метод регистрации и отправки письма с кодом подтверждения.
        :param request: Экземпляр класса Request DRF.
        :return: Response DRF.
        """

        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.validated_data,
            status=status.HTTP_200_OK,
        )


@method_decorator(
    name='token',
    decorator=swagger_auto_schema(
        request_body=TokenCreateSerializer(),
        responses={status.HTTP_200_OK: TokenResponseSerializer()},
    ),
)
class TokenViewSet(viewsets.GenericViewSet):
    """
    GenericViewSet получения токена.
    """

    serializer_class = TokenCreateSerializer

    @action(
        detail=False,
        permission_classes=(permissions.AllowAny,),
        methods=['post'],
        url_path='token',
    )
    def token(self, request: Request) -> Response:
        """
        Метод получения токена.
        :param request: Экземпляр класса Request DRF.
        :return: Response DRF.
        """

        serializer = TokenCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )
        user_confirmation_code = default_token_generator.check_token(
            user=user, token=serializer.validated_data.get('confirmation_code')
        )
        if not user_confirmation_code:
            data = {'confirmation_code': 'Неверный код подтверждения'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        response = {'token': str(AccessToken.for_user(user))}
        return Response(response, status=status.HTTP_200_OK)


class UsersModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet для работы с пользователями
    """

    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-date_joined')
    lookup_field = 'username'
    permission_classes = (
        permissions.IsAuthenticated,
        IsSuperuser | IsAdmin,
    )

    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        methods=['get', 'patch'],
        url_path='me',
    )
    def get_or_update_self_user(self, request: Request) -> Response:
        """
        Метод взаимодействия пользователя со своим профилем.
        :param request: Экземпляр класса Request DRF.
        :return: Response DRF.
        """

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                instance=request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)

            # Если пользователь пытается изменить свою роль, вернуть роль из
            # request.user
            if serializer.validated_data.get('role'):
                serializer.validated_data['role'] = request.user.role
            serializer.save()
            return Response(serializer.data)

        serializer = self.get_serializer(request.user, many=False)
        return Response(serializer.data)


@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        responses={status.HTTP_201_CREATED: TitleGetSerializer()}
    ),
)
class TitleModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet произведений.
    """

    queryset = (
        Title.objects.prefetch_related('reviews')
        .annotate(rating=Avg('reviews__score'))
        .order_by('year')
    )
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filterset_class = TitleFilter
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly & IsAdminOrReadOnly
        | IsSuperuser,
    )

    def get_serializer_class(
        self,
    ) -> Union[TitleGetSerializer, TitlePostPatchSerializer]:
        """
        Метод получения сериализатора по параметрам из self.action.
        :return: Один из сериазаторов.
        """

        if self.action in {'list', 'retrieve'}:
            serializer = TitleGetSerializer
        else:
            serializer = TitlePostPatchSerializer
        return serializer

    def create(self, request, *args, **kwargs) -> Response:
        """
        Переопределенный метод create.
        Помимо сохранения модели, заменяет сериализатор POST на GET.
        :param request: Экземпляр класса Request DRF.
        :return: Response DRF.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_serializer = TitleGetSerializer(instance=serializer.instance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class CategoryViewSet(CreateListDestroyModelMixinViewSet):
    """
    GenericViewSet категорий.
    """

    permission_classes = (IsAdminOrReadOnly | IsSuperuser,)
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyModelMixinViewSet):
    """
    GenericViewSet жанров.
    """

    queryset = Genre.objects.all().order_by('name')
    permission_classes = (IsAdminOrReadOnly | IsSuperuser,)
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet отзывов.
    """

    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly & IsAuthor
        | IsModerator
        | IsAdminOrReadOnly
        | IsSuperuser,
    )
    swagger_tags = ('reviews',)

    def get_queryset(self) -> List[Review]:
        """
        Переопределенный метод get_queryset,
        получаем нужные отзывы по title_id.
        :return: Модели отзывов.
        """

        # Необходимо для создания схемы openapi, документация ниже.
        # https://drf-yasg.readthedocs.io/en/stable/openapi.html#a-note-on-limitations
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()

        return Review.objects.filter(title__id=self.get_title_id()).order_by(
            '-pub_date',
        )

    def perform_create(
        self,
        serializer: ReviewSerializer,
    ) -> None:
        """
        Переопределенный метод perform_create,
        проверяющий наличие отзывов текущего
        пользователя к данному произведению.
        Так же подготавливает модель к сохранению, подставляя
        необходимые значения.
        :param serializer: Сериализатор ReviewSerializer.
        :return: None
        """

        title = get_object_or_404(
            Title,
            pk=self.get_title_id(),
        )
        serializer.save(
            title=title,
            author=self.request.user,
        )

    def get_title_id(self) -> int:
        """
        Получение id произведения.
        :return: id произведения в формате int.
        """

        return self.kwargs.get('title_id')


class CommentModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet комментариев.
    """

    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly & IsAuthor
        | IsModerator
        | IsAdminOrReadOnly
        | IsSuperuser,
    )
    swagger_tags = ('comments',)

    def get_queryset(self) -> List[Comment]:
        """
        Переопределенный метод get_queryset,
        получаем нужные комментарии по review_id и title_id.
        :return: Модели комментариев.
        """

        # Необходимо для создания схемы openapi, документация ниже.
        # https://drf-yasg.readthedocs.io/en/stable/openapi.html#a-note-on-limitations
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()

        review = get_object_or_404(
            Review,
            pk=self.get_review_id(),
            title__pk=self.get_title_id(),
        )
        return Comment.objects.filter(review=review,).order_by(
            '-pub_date',
        )

    def perform_create(
        self,
        serializer: CommentSerializer,
    ) -> None:
        """
        Переопределенный метод perform_create,
        подготавливает модель к сохранению, подставляя
        необходимые значения.
        :param serializer: Сериализатор CommentSerializer.
        :return: None
        """

        review = get_object_or_404(
            Review,
            pk=self.get_review_id(),
            title__pk=self.get_title_id(),
        )
        serializer.save(
            review=review,
            author=self.request.user,
        )

    def get_title_id(self) -> int:
        """
        Получение id произведения.
        :return: id произведения в формате int.
        """

        return self.kwargs.get('title_id')

    def get_review_id(self):
        """
        Получение id отзыва.
        :return: id отзыва в формате int.
        """

        return self.kwargs.get('review_id')
