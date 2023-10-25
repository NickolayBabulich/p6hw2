import random
from django.views.generic import CreateView, UpdateView
from django.core.mail import send_mail
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from config import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
import logging

logger = logging.getLogger('users')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    # success_url = reverse_lazy('users:user_verify')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Деактивируем пользователя

        # Сохраняем пользователя
        user.save()

        # Генерируем токен для верификации почты

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Создаем URL для верификации

        current_site = get_current_site(self.request)
        verification_url = reverse('users:verify_email', kwargs={'uidb64': uid, 'token': token})
        verification_url = f'http://{current_site.domain}{verification_url}'

        # Формируем тему и текст письма

        subject = 'Интернет-магазин: подтверждение почты'
        message = render_to_string('users/email_verification.html', {
            'user': user,
            'verification_url': verification_url,
        })
        plain_message = strip_tags(message)

        # Отправляем письмо для верификации
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=message,
        )

        user.save()
        return render(self.request, 'users/registration_email_sent.html')


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        logger.debug(f'Verifying email for user: {user.username}')

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)  # Вход пользователя после активации
            messages.success(request, 'Почта подтверждена, вы вошли в систему.')
            return redirect('users:profile')  # Перенаправить на страницу профиля
        else:
            messages.error(request, 'Ссылка для подтверждения почты недействительна.')
            return redirect('users:login')  # Перенаправить на страницу входа
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return redirect('users:login')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Смена пароля',
        message=f'Ваш новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()

    return redirect(reverse('catalog:list'))
