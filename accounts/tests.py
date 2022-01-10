from django.test import TestCase, RequestFactory


# Topページ
class TopPageRenderTest(TestCase):
    def test_should_return_top_page_title(self):
        response = self.client.get("/")
        self.assertContains(response, 'つぶやきで、世界はつながる', status_code=200)
    
    def test_should_use_expected_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'accounts/top.html')


# Aboutページ
class AboutPageRenderTest(TestCase):
    def test_should_return_about_page_title(self):
        response = self.client.get("/about")
        self.assertContains(response, 'TweetAppとは', status_code=200)
    
    def test_should_use_expected_template(self):
        response = self.client.get("/about")
        self.assertTemplateUsed(response, 'accounts/about.html')

