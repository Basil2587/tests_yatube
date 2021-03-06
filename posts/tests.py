from django.test import TestCase, Client
from .models import Post, User
from users.forms import User


class SimpleTestCase(TestCase):
    def setUp(self):
        self.client = Client()
                # создаём пользователя
        self.user = User.objects.create_user(
                        username="testname", email="myname@test.com", password="12345678"
                )
        self.client.force_login(self.user)

    def test_profile(self):
        response = self.client.get("/testname/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_authorization_post(self):
        test_post = 'Создали новый пост для ника testname'
        self.client.post("/new/", {"text":test_post})
        response = self.client.get('/')
        self.assertContains(response, test_post)

    def test_not_authorization(self):
        self.client.logout()
        response = self.client.get('/new/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/auth/login/?next=/new/')

    def test_create_post(self):
        test_post = 'Создали новый пост для ника testname'
        self.client.post("/new/", {"text":test_post})
        response = self.client.get('/')
        self.assertContains(response, test_post)
        response = self.client.get("/testname/")
        self.assertContains(response, test_post)
        post = Post.objects.get(author=self.user)
        response = self.client.get(f'/testname/{post.id}/')
        self.assertContains(response, test_post)

    def test_edit_post(self):
        test_post = 'Здесь находится пост testname'
        self.client.post("/new/", {"text":test_post}, follow=True)
        post = Post.objects.get(author=self.user)
        test_2 = 'Здесь находится пост testname, новоя редакция.' 
        self.client.post(f'/testname/{post.id}/edit', {"text":test_2}, follow=True)
        response = self.client.get("/testname/")
        self.assertContains(response, test_2)  
        response = self.client.get(f'/testname/{post.id}/')
        self.assertContains(response, test_2) 
        response = self.client.get("/")
        self.assertContains(response, test_2)
        
    def tearDown(self):
        print('Excellent')
