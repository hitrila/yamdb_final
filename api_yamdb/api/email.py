from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class ConfirmationCodeEmailMessage:
    """
    Класс формирования и отправки писем с кодом подтверждения.
    """

    def send_confirmation_code_email(
        self,
        username: str,
        email: str,
        confirmation_code: str,
    ) -> None:
        """
        Метод подготовки и отправки сообщения с кодом подтверждения.
        :param username: Имя пользователя.
        :param email: Эл.почта пользователя.
        :param confirmation_code: Сгенерированный код подтверждения.
        :return: None
        """

        context = {
            'username': username,
            'text': 'Вы запросили код подтверждения на "API-yamdb".',
            'confirmation_code': confirmation_code,
        }

        html_message = render_to_string(
            template_name='send_confirmation_code.html',
            context=context,
        )

        message = EmailMessage(
            subject='API-yamdb: Код подтверждения.',
            body=html_message,
            to=[email],
        )
        message.content_subtype = 'html'
        message.send()
