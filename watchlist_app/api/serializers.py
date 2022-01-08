from rest_framework import serializers
from watchlist_app.models import Watchlist, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ['watchlist']


class WatchlistSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform  = serializers.CharField(source='platform.name')
    class Meta:
        model = Watchlist
        fields = '__all__'


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchlistSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_validate])
#     remarks = serializers.CharField()
#     active = serializers.BooleanField()

#     def name_validate(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError('Name too short!')

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)


#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.remarks = validated_data.get('remarks', instance.remarks)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance


#     def validate(self, data):

#         if data['name'] == data['remarks']:
#             raise serializers.ValidationError('Dude!, am i a joke to you ??')
#         else:
#             return data


    # def validate_name(self, value):

    #     if len(value) < 2:
    #         raise serializers.ValidationError('Name too short!')
    #     else:
    #         return value
    