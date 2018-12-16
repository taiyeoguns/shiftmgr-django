from django.urls import reverse, resolve


class TestUrls:
    def test_home_view_is_displayed(self):
        path = reverse('home')
        response = resolve(path)
        assert 'home' in str(response.func)
        assert response.view_name == 'home'
