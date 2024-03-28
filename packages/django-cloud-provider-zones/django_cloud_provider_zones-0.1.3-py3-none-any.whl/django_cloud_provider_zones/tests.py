import json

from django.test import Client, TestCase
from django.test.utils import override_settings

from django_cloud_provider_zones import urls


@override_settings(
    ROOT_URLCONF=urls,
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "rest_framework",
        "django_cloud_provider_zones",
    ],
)
class CloudProviderTestCase(TestCase):
    fixtures = [
                "django_cloud_provider_zones-CloudProvider.json",  
                "django_cloud_provider_zones-CloudRegion.json",
"django_cloud_provider_zones-CloudAvailabilityZone.json",  
    ]

    def setUp(self):
        self.client = Client()

    def test_cloud_provider_name(self):
        providers = [
        {'provider': 'aws'},
        {'provider': 'gcp'}
        ]
        r = self.client.get("/cloud-providers/")
        self.assertEqual(r.status_code, 200)
        response_dict = json.loads(r.content.decode("utf-8"))
        for provider in providers:
            self.assertIn(provider, response_dict)

    def test_region_fixture_data(self):
        """simple sanity check"""
        expected_regions = [
            {
                "provider": "gcp",
                "original_region_name": "us-west4",
                "geographic_region": "us",
                "cardinality": "west",
                "number": "4",
            },
            {
                "provider": "aws",
                "original_region_name": "ap-northeast-3",
                "geographic_region": "ap",
                "cardinality": "northeast",
                "number": "3",
            },
        ]
        r = self.client.get("/cloud-regions/")
        self.assertEqual(r.status_code, 200)
        for test_region in expected_regions:
            results_count = 0
            for response in json.loads(r.content.decode("utf-8")):
                if test_region == {k: response[k] for k in test_region.keys()}:
                    results_count += 1
            self.assertEqual(results_count, 1)

    def test_availability_zone_fixture_data(self):
        expected_zones = [
            {
                "az": "a",
                "region": "gcp-us-west4",
            },
        ]
        r = self.client.get("/cloud-availability-zones/")
        self.assertEqual(r.status_code, 200)
        for test_zone in expected_zones:
            results_count = 0
            for response in json.loads(r.content.decode("utf-8")):
                if test_zone == {k: response[k] for k in test_zone.keys()}:
                    results_count += 1
            self.assertEqual(results_count, 1)
