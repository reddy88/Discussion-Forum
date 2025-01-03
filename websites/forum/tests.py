# from django.core.urlresolvers import reverse
from django.urls import reverse, resolve  
from django.test import TestCase
from .models import Board
from .views import home, board_topics

class HomeTests(TestCase):
    def setUp(self):
        # Create a Board instance and set it as an attribute for the test
        self.board = Board.objects.create(name='Python', description='Python board.')
        self.url = reverse('home')
        self.response = self.client.get(self.url)

    def test_home_view_status_code(self):
        url = reverse('home')  
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)
    
    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, f'href="{board_topics_url}"')
        
class BoardTopicsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Python', description='Python board.')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        url = f'/boards/{self.board.pk}/'
        view = resolve(url)
        self.assertEquals(view.func, board_topics)