"""Comprehensive tests for hub views and models."""

from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError

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


class ModelTests(TestCase):
    """Test model functionality and validation."""
    
    def test_person_creation(self):
        """Test creating a person with all fields."""
        person = Person.objects.create(
            name="Test Person",
            role="Developer",
            interests=["Python", "Django"],
            availability="Mentorship, Speaking",
            bio="A test person",
            avatar_url="https://example.com/avatar.jpg",
            github_url="https://github.com/test",
            twitter_url="https://twitter.com/test",
            linkedin_url="https://linkedin.com/in/test",
            website_url="https://test.com"
        )
        
        self.assertEqual(person.name, "Test Person")
        self.assertEqual(person.slug, "test-person")
        self.assertEqual(person.interests, ["Python", "Django"])
        self.assertTrue(person.created_at)
        self.assertTrue(person.updated_at)
    
    def test_person_slug_generation(self):
        """Test automatic slug generation and uniqueness."""
        person1 = Person.objects.create(name="John Doe")
        person2 = Person.objects.create(name="John Doe")
        
        self.assertEqual(person1.slug, "john-doe")
        self.assertEqual(person2.slug, "john-doe-2")
    
    def test_person_validation(self):
        """Test person model validation."""
        person = Person(
            name="Test Person",
            avatar_url="invalid-url",
            interests="not-a-list"
        )
        
        with self.assertRaises(ValidationError):
            person.full_clean()
    
    def test_person_social_links(self):
        """Test social links method."""
        person = Person.objects.create(
            name="Test Person",
            github_url="https://github.com/test",
            twitter_url="https://twitter.com/test"
        )
        
        links = person.get_social_links()
        self.assertEqual(len(links), 2)
        self.assertIn(('GitHub', 'https://github.com/test', 'github'), links)
        self.assertIn(('Twitter', 'https://twitter.com/test', 'twitter'), links)
    
    def test_community_creation(self):
        """Test creating a community with all fields."""
        community = Community.objects.create(
            name="Test Community",
            focus="Testing things",
            location="Test City",
            contact="test@example.com",
            links={"website": "https://test.com", "twitter": "https://twitter.com/test"},
            logo_url="https://example.com/logo.jpg",
            description="A test community",
            founded_year=2020,
            member_count=100
        )
        
        self.assertEqual(community.name, "Test Community")
        self.assertEqual(community.slug, "test-community")
        self.assertEqual(community.founded_year, 2020)
        self.assertEqual(community.member_count, 100)
    
    def test_community_validation(self):
        """Test community model validation."""
        community = Community(
            name="Test Community",
            founded_year=1800,  # Too old
            member_count=-5  # Negative
        )
        
        with self.assertRaises(ValidationError):
            community.full_clean()
    
    def test_community_links_display(self):
        """Test community links display method."""
        community = Community.objects.create(
            name="Test Community",
            links={"website": "https://test.com", "twitter": "https://twitter.com/test"}
        )
        
        links = community.get_links_display()
        self.assertEqual(len(links), 2)
        self.assertIn(('Website', 'https://test.com', 'website'), links)
        self.assertIn(('Twitter', 'https://twitter.com/test', 'twitter'), links)
    
    def test_school_creation(self):
        """Test creating a school with all fields."""
        school = School.objects.create(
            name="Test School",
            city="Test City",
            programs=["Computer Science", "Engineering"],
            contact="school@example.com"
        )
        
        self.assertEqual(school.name, "Test School")
        self.assertEqual(school.slug, "test-school")
        self.assertEqual(school.programs, ["Computer Science", "Engineering"])
    
    def test_school_programs_display(self):
        """Test school programs display method."""
        school = School.objects.create(
            name="Test School",
            programs=["CS", "Engineering"]
        )
        
        self.assertEqual(school.get_programs_display(), "CS, Engineering")
        
        school_no_programs = School.objects.create(name="Empty School")
        self.assertEqual(school_no_programs.get_programs_display(), "No programs listed")


class SearchAPITests(TestCase):
    """Test search API functionality."""
    
    def setUp(self):
        self.person = Person.objects.create(
            name="John Developer",
            role="Full-Stack Developer",
            bio="Python and Django expert"
        )
        self.community = Community.objects.create(
            name="Python Community",
            focus="Python development",
            location="Test City"
        )
        self.school = School.objects.create(
            name="Tech University",
            city="Test City",
            programs=["Computer Science"]
        )
    
    def test_search_api_empty_query(self):
        """Test search API with empty query."""
        response = self.client.get(reverse('hub:search-api'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['people'], [])
        self.assertEqual(data['communities'], [])
        self.assertEqual(data['schools'], [])
    
    def test_search_api_short_query(self):
        """Test search API with short query."""
        response = self.client.get(reverse('hub:search-api'), {'q': 'a'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['people'], [])
    
    def test_search_api_people(self):
        """Test search API for people."""
        response = self.client.get(reverse('hub:search-api'), {'q': 'john'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['people']), 1)
        self.assertEqual(data['people'][0]['name'], 'John Developer')
    
    def test_search_api_communities(self):
        """Test search API for communities."""
        response = self.client.get(reverse('hub:search-api'), {'q': 'python'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['communities']), 1)
        self.assertEqual(data['communities'][0]['name'], 'Python Community')
    
    def test_search_api_schools(self):
        """Test search API for schools."""
        response = self.client.get(reverse('hub:search-api'), {'q': 'tech'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['schools']), 1)
        self.assertEqual(data['schools'][0]['name'], 'Tech University')


class FilterTests(TestCase):
    """Test filtering functionality."""
    
    def setUp(self):
        Person.objects.create(
            name="Python Developer",
            role="Backend Developer",
            interests=["Python", "Django"],
            availability="Mentorship"
        )
        Person.objects.create(
            name="Frontend Developer",
            role="Frontend Developer",
            interests=["React", "JavaScript"],
            availability="Speaking"
        )
        Person.objects.create(
            name="Full Stack Developer",
            role="Full-Stack Developer",
            interests=["Python", "React"],
            availability="Mentorship, Speaking"
        )
    
    def test_people_search_filter(self):
        """Test people search filtering."""
        response = self.client.get(reverse('hub:people'), {'search': 'python'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['people']), 2)  # Python Developer and Full Stack
    
    def test_people_role_filter(self):
        """Test people role filtering."""
        response = self.client.get(reverse('hub:people'), {'role': 'Backend'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['people']), 1)
        self.assertEqual(response.context['people'][0].name, 'Python Developer')
    
    def test_people_interest_filter(self):
        """Test people interest filtering."""
        response = self.client.get(reverse('hub:people'), {'interest': 'React'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['people']), 2)  # Frontend and Full Stack
    
    def test_people_availability_filter(self):
        """Test people availability filtering."""
        response = self.client.get(reverse('hub:people'), {'availability': 'Speaking'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['people']), 2)  # Frontend and Full Stack
