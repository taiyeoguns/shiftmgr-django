from django.test import TestCase
from django.http import HttpRequest
from django.test import SimpleTestCase
from django.urls import reverse

from . import views


# Create your tests here.
class ShiftsPageTests(SimpleTestCase):
    def test_shift_page_status_code(self):
        response = self.client.get('/shifts/')
        self.assertEquals(response.status_code, 200)