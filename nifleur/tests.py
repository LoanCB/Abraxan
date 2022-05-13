from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestMessageCase(TestCase):
    """ Custom class method to add a new unit test assertMessagesContains to testing response messages """
    def assertMessagesContains(self, response, messages):
        """
        Unit test for messages returned by the view

        :param response:
        :param messages: List contains all messages
        :type messages: list of str
        """
        response_messages = list(response.context['messages'])
        self.assertEqual(len(response_messages), len(messages))
        for i in range(len(messages)):
            self.assertEqual(str(response_messages[i]), messages[i])


class ViewsTest(TestMessageCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser('super_user', 'superuser@test.com', 'admin_password')
        cls.user = User.objects.create_user('user', 'user@test.com', 'user_password')

    # def setUp(self):
    #     self.client.force_login(self.superuser)

    def test_home_page(self):
        self.client.force_login(self.superuser)

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nifleur/home.html')

    def test_logout(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('logout_user'), follow=True)
        self.assertTemplateUsed(response, 'nifleur/login.html')
        self.assertMessagesContains(response, ['Vous avez bien été déconnecté'])

    def test_get_login_page(self):
        response = self.client.get(reverse('login_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nifleur/login.html')

    def test_post_login_page_wrong_user(self):
        response = self.client.post(
            reverse('login_user'),
            {'username': 'wrong_username', 'password': self.user.password},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nifleur/login.html')
        self.assertMessagesContains(response, ['Utilisateur ou mot de passe incorrect'])

    def test_post_login_page(self):
        response = self.client.post(
            reverse('login_user'),
            {'username': 'user', 'password': 'user_password'},
            follow=True
        )
        self.assertTrue(response.context['user'].is_authenticated)
