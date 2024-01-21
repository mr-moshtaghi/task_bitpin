import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

from content.models import Content, Rating


class ContentTestCase(APITestCase):
    def setUp(self) -> None:
        user1 = User.objects.create_user(username="sajjad", password="sajjad", )
        user2 = User.objects.create_user(username="ahmad", password="ahmad")
        request_body_for_token_1 = {
            "username": "sajjad",
            "password": "sajjad"
        }
        request_body_for_token_2 = {
            "username": "ahmad",
            "password": "ahmad"
        }
        self.authenticated_client_1 = APIClient()
        self.authenticated_client_2 = APIClient()
        response_for_user_1 = self.authenticated_client_1.post(reverse('token'), request_body_for_token_1)
        response_for_user_2 = self.authenticated_client_1.post(reverse('token'), request_body_for_token_2)

        self.token_1 = json.loads(response_for_user_1.content).get('access')
        self.authenticated_client_1.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_1}')

        self.token_2 = json.loads(response_for_user_2.content).get('access')

        self.authenticated_client_2.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_2}')

        content1 = Content.objects.create(title="content1", text="text for content1")
        content2 = Content.objects.create(title="content2", text="text for content2")

        Rating.objects.create(
            content=content1,
            rating=5,
            user=user1
        )
        Rating.objects.create(
            content=content1,
            rating=3,
            user=user2
        )
        Rating.objects.create(
            content=content2,
            rating=4,
            user=user1
        )

    def test_list_contents(self):
        responses_for_user_1 = self.authenticated_client_1.get(reverse("content:contents")).json()

        self.assertEqual(responses_for_user_1[0]["title"], "content1")
        self.assertEqual(responses_for_user_1[0]["text"], "text for content1")
        self.assertEqual(responses_for_user_1[0]["ratings_count"], 2)
        self.assertEqual(responses_for_user_1[0]["ratings_average"], 4.0)
        self.assertEqual(responses_for_user_1[0]["my_rating"], 5)

        self.assertEqual(responses_for_user_1[1]["title"], "content2")
        self.assertEqual(responses_for_user_1[1]["text"], "text for content2")
        self.assertEqual(responses_for_user_1[1]["ratings_count"], 1)
        self.assertEqual(responses_for_user_1[1]["ratings_average"], 4.0)
        self.assertEqual(responses_for_user_1[1]["my_rating"], 4)

        responses_for_user_2 = self.authenticated_client_2.get(reverse("content:contents")).json()

        self.assertEqual(responses_for_user_2[0]["title"], "content1")
        self.assertEqual(responses_for_user_2[0]["text"], "text for content1")
        self.assertEqual(responses_for_user_2[0]["ratings_count"], 2)
        self.assertEqual(responses_for_user_2[0]["ratings_average"], 4.0)
        self.assertEqual(responses_for_user_2[0]["my_rating"], 3)

        self.assertEqual(responses_for_user_2[1]["title"], "content2")
        self.assertEqual(responses_for_user_2[1]["text"], "text for content2")
        self.assertEqual(responses_for_user_2[1]["ratings_count"], 1)
        self.assertEqual(responses_for_user_2[1]["ratings_average"], 4.0)
        self.assertIsNone(responses_for_user_2[1]["my_rating"])

    def test_rating(self):
        # for user 1
        responses = self.authenticated_client_1.post(
            reverse("content:rating", args=(1,)),  # content1
            {"rating": 2}
        ).json()

        self.assertEqual(responses["title"], "content1")
        self.assertEqual(responses["text"], "text for content1")
        self.assertEqual(responses["ratings_count"], 2)
        self.assertEqual(responses["ratings_average"], 2.5)
        self.assertEqual(responses["my_rating"], 2)

        responses = self.authenticated_client_1.post(
            reverse("content:rating", args=(1,)),  # content1
            {"rating": 5}
        ).json()

        self.assertEqual(responses["title"], "content1")
        self.assertEqual(responses["text"], "text for content1")
        self.assertEqual(responses["ratings_count"], 2)
        self.assertEqual(responses["ratings_average"], 4.0)
        self.assertEqual(responses["my_rating"], 5)

        # for user 2

        responses = self.authenticated_client_2.post(
            reverse("content:rating", args=(1,)),  # content1
            {"rating": 3}
        ).json()

        self.assertEqual(responses["title"], "content1")
        self.assertEqual(responses["text"], "text for content1")
        self.assertEqual(responses["ratings_count"], 2)
        self.assertEqual(responses["ratings_average"], 4.0)
        self.assertEqual(responses["my_rating"], 3)

        responses = self.authenticated_client_2.post(
            reverse("content:rating", args=(2,)),  # content2
            {"rating": 1}
        ).json()

        self.assertEqual(responses["title"], "content2")
        self.assertEqual(responses["text"], "text for content2")
        self.assertEqual(responses["ratings_count"], 2)
        self.assertEqual(responses["ratings_average"], 2.5)
        self.assertEqual(responses["my_rating"], 1)
