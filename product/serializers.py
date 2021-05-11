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

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     user = request.user
    #     tags = validated_data.pop('tags', [])
    #     post = Product.objects.create(author=user, **validated_data)
    #     for tag in tags:
    #         post.tags.add(tag)
    #     return post

    # def get_fields(self):
    #     action = self.context.get('action')
    #     fields = super().get_fields()
    #     if action == 'create':
    #         fields.pop('slug')
    #         fields.pop('author')
    #     return fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category, context=self.context).data
        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        return representation

# class PostsListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ('title', 'slug', 'image')

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