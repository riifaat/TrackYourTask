from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError


class BaseTest(TestCase):
    def setUp(self):
        self.signupuser_url=reverse('signupuser')
        self.loginuser_url=reverse('loginuser')
        self.user={
            'username':'username',
            'password1':'password',
            'password2':'password',
            'password':'password'
        }
        self.user_unmatching_password={

            'username':'username',
            'password1':'teslatt',
            'password2':'teslatt',
            'password':'password'
        }
         
        return super().setUp()

class SignUpUserTest(BaseTest):
   def test_user_can_view_page_correctly(self):
       response=self.client.get(self.signupuser_url)
       self.assertEqual(response.status_code,200)
       self.assertTemplateUsed(response,'task/signupuser.html')


   def test_user_can_register(self):
       response = self.client.post(self.signupuser_url, self.user, format='text/html')
       self.assertEqual(response.status_code, 302)



def test_user_cant_register_with_taken_username(self):
        self.client.post(self.signupuser_url,self.user,format='text/html')
        response=self.client.post(self.signupuser_url,self.user,format='text/html')
        self.assertEqual(response.status_code,400) 



def test_user_cant_register_with_unmatched_passwords(self):
        response=self.client.post(self.signupuser_url,self.user_unmatching_password,format='text/html')
        self.assertEqual(response.status_code,400)   

        
            


class LoginTest(BaseTest):
    def test_user_can_access_login_page(self):
        response=self.client.get(self.loginuser_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'task/loginuser.html')



    def test_user_can_login_successfully(self):
        self.client.post(self.signupuser_url,self.user,format='text/html')
        user=User.objects.filter(username=self.user['username']).first()
        user.is_active=True
        user.save()
        response= self.client.post(self.loginuser_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302) 



    def test_user_cant_login_without_username(self):
        response= self.client.post(self.loginuser_url,{'password':'passwped','username':''},format='text/html')
        self.assertEqual(response.status_code,200)


    
    def test_user_cant_login_without_password(self):
        response= self.client.post(self.loginuser_url,{'username':'username','password':''},format='text/html')
        self.assertEqual(response.status_code,200)