from django.test import TestCase
from django.test import Client
from django.contrib.auth import models


class ViewsTestCase(TestCase):
    #def setUp(self):
    #    models.User.objects.create(username="test", password="testpass")

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    #def testLogin(self):
    #        c = Client()
    #        response = c.post(
    #            '/login/', {'username': 'test', 'password': 'testpass'})
    #        self.assertEquals(response.status_code, 200)