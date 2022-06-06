from rest_framework import serializers

from .. import models


class ReviewSeriaizer(serializers.ModelSerializer):
    """Serializer for Review model."""

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    course = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Review
        fields = (
            "id",
            "rating",
            "review",
            "user",
            "course",
        )