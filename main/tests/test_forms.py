from django.test import TestCase
from django.core import mail
from main import forms
from django.urls import reverse

class TestPage(TestCase):
    def test_home_page_works(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'BookTime')

    def test_about_us_page_works(self):
        response = self.client.get(reverse("about_us"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_us.html')
        self.assertContains(response, 'BookTime')    

class TestForm(TestCase):
    def test_valid_contact_us_form_sends_email(self):
        form = forms.ContactForm({
            'name': "Rajneesh Kumar",
            'message': "Hi There"
        })
        self.assertTrue(form.is_valid())

        with self.assertLogs('main.forms', level='INFO') as cm:
            form.send_mail()
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Site message')
        self.assertGreaterEqual(len(cm.output), 1)
    
    def test_invalid_contact_us_form(self):
        form = forms.ContactForm({
            'message': "Hi There"
        })
        
        self.assertFalse(form.is_valid())
    