from rest_framework import serializers

from .models import Category, Product, Review

###
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']

    def validate_title(self, title):
        if self.Meta.model.objects.filter(title=title).exists():
            raise serializers.ValidationError('Название категории не должно повторяться')
        return title


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category, context=self.context).data
        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        representation['likes'] = instance.likes.count()
        return representation

###
class ProductsListSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='slug')

    class Meta:
        model = Product
        fields = ['title', 'slug', 'image', 'price', 'details']


###
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        review = Review.objects.create(user=user, **validated_data)
        return review