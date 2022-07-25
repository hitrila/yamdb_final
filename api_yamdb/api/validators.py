from rest_framework import serializers

INVALID_USERNAME_SET = {
    'me',
}


def username_validator(value: str) -> None:
    """
    Валидатор имя пользователя.
    :param value: Имя пользователя.
    :return: None
    """

    if value in INVALID_USERNAME_SET:
        raise serializers.ValidationError(
            f'Использовать имя {value} в качестве username запрещено.'
        )
