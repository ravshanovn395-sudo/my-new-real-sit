from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import ChatMessage


class ChatPageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='chat_user', password='test-password')
        self.chat_url = reverse('chat_page')

    def test_chat_requires_login(self):
        response = self.client.get(self.chat_url)

        self.assertRedirects(response, f'{reverse("login_page")}?next=%2Fchat%2F')

    def test_authenticated_user_can_view_messages_and_usernames(self):
        other_user = User.objects.create_user(username='other_user', password='test-password')
        ChatMessage.objects.create(user=other_user, text='Salom!')
        self.client.force_login(self.user)

        response = self.client.get(self.chat_url)

        self.assertContains(response, '@other_user')
        self.assertContains(response, 'Salom!')

    def test_authenticated_user_can_send_message(self):
        self.client.force_login(self.user)

        response = self.client.post(self.chat_url, {'text': '  Hammaga salom!  '})

        self.assertRedirects(response, self.chat_url)
        message = ChatMessage.objects.get()
        self.assertEqual(message.user, self.user)
        self.assertEqual(message.text, 'Hammaga salom!')

    def test_blank_message_is_not_saved(self):
        self.client.force_login(self.user)

        response = self.client.post(self.chat_url, {'text': '   '})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(ChatMessage.objects.exists())
