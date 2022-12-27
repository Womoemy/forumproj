from django.test import TestCase
from django.urls import reverse, resolve
# from django.contrib.auth.models import User
from ..views import home
from ..models import Forum

class HomeTests(TestCase):
    def setUp(self):
        self.forum = Forum.objects.create(name='Django', description='Django board.')
        url = reverse('home')
        self.response = self.client.get(url)
    
    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)
        
    def test_home_view_contains_link_to_topics_page(self):
        forum_topics_url = reverse('forum_topics', kwargs={'pk': self.forum.pk})
        self.assertContains(self.response, 'href="{0}"'.format(forum_topics_url))
        