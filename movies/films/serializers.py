from rest_framework import serializers

from movies.films.models import Movie, Comment


class TopSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        pass

    def to_representation(self, obj):
        return {'id': obj[1].id,
                'rank': obj[0],
                'total_comments': obj[1].total_comments}


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'rated', 'released', 'runtime',
                  'genre', 'director', 'plot', 'language', 'country', 'imdbID')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'movie')