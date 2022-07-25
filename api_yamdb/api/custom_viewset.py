from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class CreateListDestroyModelMixinViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    ViewSet создания, удаления и получения списка обьектов.
    """

    pass
