"""Smoke tests for hub views."""

from django.test import TestCase
from django.urls import reverse

from .models import Community, Person, School


class HubViewTests(TestCase):
    def setUp(self):
        self.person = Person.objects.create(
            name="Test Person",
            role="Tester",
            interests=["Testing"],
            availability="Mentorship",
        )
        self.community = Community.objects.create(
            name="Test Community",
            focus="Testing things",
            location="Yaoundé",
            contact="contact@test",
            links={"website": "https://example.com"},
        )
        self.school = School.objects.create(
            name="Test School",
            city="Buea",
            programs=["Testing"],
            contact="hello@test",
        )

    def test_home_page(self):
        response = self.client.get(reverse("hub:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Djangonista")
        self.assertContains(response, "People")

    def test_people_pagination_and_detail(self):
        for index in range(12):
            Person.objects.create(name=f"Extra Person {index}", role="Contributor")

        list_response = self.client.get(reverse("hub:people"), {"page": 2})
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.context["page_obj"].number, 2)
        self.assertEqual(list_response.context["page_obj"].paginator.num_pages, 2)
        self.assertLessEqual(
            len(list_response.context["page_obj"].object_list),
            list_response.context["page_obj"].paginator.per_page,
        )
        self.assertContains(list_response, self.person.name)

        detail_response = self.client.get(self.person.get_absolute_url())
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, self.person.role)

    def test_community_pagination_and_detail(self):
        for index in range(12):
            Community.objects.create(name=f"Extra Community {index}")

        list_response = self.client.get(reverse("hub:communities"), {"page": 2})
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.context["page_obj"].number, 2)
        self.assertEqual(list_response.context["page_obj"].paginator.num_pages, 2)
        self.assertLessEqual(
            len(list_response.context["page_obj"].object_list),
            list_response.context["page_obj"].paginator.per_page,
        )
        self.assertContains(list_response, self.community.name)

        detail_response = self.client.get(self.community.get_absolute_url())
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, self.community.location)

    def test_school_pagination_and_detail(self):
        for index in range(12):
            School.objects.create(name=f"Extra School {index}")

        list_response = self.client.get(reverse("hub:schools"), {"page": 2})
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.context["page_obj"].number, 2)
        self.assertEqual(list_response.context["page_obj"].paginator.num_pages, 2)
        self.assertLessEqual(
            len(list_response.context["page_obj"].object_list),
            list_response.context["page_obj"].paginator.per_page,
        )
        self.assertContains(list_response, self.school.name)

        detail_response = self.client.get(self.school.get_absolute_url())
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, self.school.city)
