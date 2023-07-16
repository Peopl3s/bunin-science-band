from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from events.models import Event
from comments.models import Comment
from ..forms import LoginForm, UserRegistrationForm

User = get_user_model()


class LoginFormTests(TestCase):
    """Проверка формы входа."""

    def setUp(self):
        User.objects.create_user(username="auth", 
                                 email='test@test.ru',
                                 password='test_password')

    def test_LoginForm_name_error(self):
        """Проверка ввода неправильного username."""

        form_data = {
            'username': 'error',
            'password': 'test_password'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid(), 'Данные невалидные')
        
    def test_LoginForm_pass_error(self):
        """Проверка ввода неправильного password."""
        
        form_data = {
            'username': 'auth',
            'password': 'error'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid(), 'Данные невалидные')
        
    def test_LoginForm_email_error(self):
        """Проверка ввода неправильного password."""
        
        form_data = {
            'username': 'auth',
            'password': 'test_password',
            'email': 'error'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid(), 'Данные невалидные')

    def test_LoginForm_true(self):
        """Проверка ввода корректных данных."""
        
        form_data = {
            'username': 'auth',
            'password': 'test_password',
            'email':'test@test.ru'
        }
        
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid(), 'Данные невалидные')
    
    
    
class UserRegistrationFormTests(TestCase):
    """Проверка формы регистрации."""

    def setUp(self):
        User.objects.create_user(username="auth", 
                                 email='test@test.ru',
                                 password='test_password')   
         
    def test_password_weak(self):
        """Проверка ввода cлабого пароля."""
        
        form_data = {
            'username': 'auth',
            'password': '123',
            'password2': '123',
            'email':'test2@test.ru'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.errors['password'])
        
    def test_email_already_exists(self):
        """Проверка ввода уже существующей почты."""
        
        form_data = {
            'username': 'auth',
            'password': '123dfnfdjHJ!',
            'password2': '123dfnfdjHJ!',
            'email':'test@test.ru'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.errors['email'])
    
    def test_repeat_password_wrong(self):
        """Проверка несовпадающих паролей."""
        
        form_data = {
            'username': 'auth',
            'password': '123dfnfdjHJ!',
            'password2': '123dfnfdjHJ1',
            'email':'test@test.ru'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.errors['password2'])
    
    def test_username_null(self):
        """Проверка ввода пустого username."""
        
        form_data = {
            'username': '',
            'password': 'test_password',
            'email':'test2@test.ru'
        }
        
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid(), 'Данные невалидные')
    
    def test_password_null(self):
        """Проверка ввода пустого password."""
        
        form_data = {
            'username': 'auth',
            'password': '',
            'password2': 'fgfg',
            'email':'test2@test.ru'
        }
        
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid(), 'Данные невалидные')


   