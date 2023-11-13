from django.urls import reverse
from rest_framework.test import APITestCase,APIRequestFactory
from rest_framework import status 
from accounts.models import User 
from service.models import Announcement
from faker import Faker
# Create your tests here.
class AnnouncementTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_data={"email":"123@naver.com","password":"1234"}
        cls.user_data={"email":"jh2@naver.com","password":"132435ss"}
        cls.faker=Faker()
        cls.request_factory = APIRequestFactory()
        User.objects.create_superuser("123@naver.com",'이진형',"1234")
        for i in range(1111):
            Announcement.objects.create(title=cls.faker.word,content=cls.faker.word)
    def setUp(self):
        self.admin_access=self.client.post(reverse("Login_View"),self.admin_data).data['access']
    def test_get_announcement_list(self):
        response=self.client.get(path=reverse("service"),HTTP_AUTHORIZATION="Bearer {}".format(self.admin_access))
        self.assertEqual(response.status_code,200)

    def test_get_announcement_detail(self):
        response=self.client.get(path=reverse("service"),HTTP_AUTHORIZATION="Bearer {}".format(self.admin_access))
        self.assertEqual(response.status_code,200)
    