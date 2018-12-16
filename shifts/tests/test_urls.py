from django.urls import reverse, resolve


# Create your tests here.
class TestUrls:
    def test_shift_page_url(self):
        path = reverse('shifts:index')
        assert resolve(path).view_name == 'shifts:index'
