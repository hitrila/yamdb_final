from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from .swagger_urls import urlpatterns as swagger_urls
from .views import (
    TitleModelViewSet,
    CategoryViewSet,
    GenreViewSet,
    ReviewModelViewSet,
    CommentModelViewSet,
    SignUpViewSet,
    TokenViewSet,
    UsersModelViewSet,
)

router = DefaultRouter()

app_name = 'api'
router.register(
    'users',
    UsersModelViewSet,
    basename='users',
)
router.register(
    'titles',
    TitleModelViewSet,
)

router.register(
    'categories',
    CategoryViewSet,
)

router.register(
    'genres',
    GenreViewSet,
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewModelViewSet,
    basename='reviews',
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentModelViewSet,
    basename='comments',
)

router.register(
    'auth',
    SignUpViewSet,
    basename='auth',
)
router.register(
    'auth',
    TokenViewSet,
    basename='token',
)

urlpatterns = [
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc',
    ),
    path(
        'v1/',
        include(router.urls),
    ),
]

urlpatterns += swagger_urls
