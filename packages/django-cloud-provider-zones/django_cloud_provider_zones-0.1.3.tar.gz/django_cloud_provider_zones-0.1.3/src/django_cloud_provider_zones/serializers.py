""" not ready for production, used for testing """
from rest_framework import serializers
from .models import CloudProvider, CloudRegion, CloudAvailabilityZone


class CloudProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudProvider
        fields = ("provider",)


class CloudRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudRegion
        fields = ("provider", "geographic_region", "cardinality", "number", "original_region_name", 
                  "short_name", "short_name_with_provider")


class CloudAvailabilityZoneSerializer(serializers.ModelSerializer):
    region = serializers.StringRelatedField()

    class Meta:
        model = CloudAvailabilityZone
        fields = ("az", "region")
