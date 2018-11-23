from datetime import datetime

import requests
from django.db.models import Count

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response

from movies.films.models import Movie, Comment
from movies.films.serializers import MovieSerializer, CommentSerializer, \
    TopSerializer

from django.conf import settings


class TopViewSet(viewsets.ViewSet):

    @classmethod
    def _rankize(cls, iterable, get_val):
        current_rank = 1
        next_rank = 2

        iterable = iter(iterable)
        first_el = next(iterable)
        yield (current_rank, first_el)
        old_val = get_val(first_el)

        for el in iterable:
            new_val = get_val(el)
            if old_val > new_val:
                old_val = new_val
                yield (next_rank, el)
                current_rank = next_rank
            else:
                yield (current_rank, el)
            next_rank += 1

    def list(self, request):
        queryset = Movie.objects.all().annotate(
            total_comments=Count('comments')
        ).order_by('-total_comments')
        serializer = TopSerializer(self._rankize(queryset,
                                                 lambda el: el.total_comments),
                                   many=True)
        return Response(serializer.data)


class MovieViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Movie.objects.all()
        serializer = MovieSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        title = request.data.get('title', None)
        if title is None:
            raise ValidationError('Movie `title` is a required parameter.')

        params = {'apikey': settings.API_KEY, 't': title}
        r = requests.get('http://www.omdbapi.com/', params=params)
        r.raise_for_status()
        body = r.json()

        if 'Error' in body:
            raise NotFound(detail='Movie with title={} not found'.format(title))

        try:
            released_date = datetime.strptime(body['Released'],
                                              "%d %b %Y").date()
        except ValueError:
            released_date = None

        movie = Movie(title=body['Title'],
                      year=body['Year'],
                      rated=body['Rated'],
                      released=released_date,
                      runtime=body['Runtime'],
                      genre=body['Genre'],
                      director=body['Director'],
                      plot=body['Plot'],
                      language=body['Language'],
                      country=body['Country'],
                      imdbID=body['imdbID'])
        movie.save()
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=201)

    def retrieve(self, request, pk=None):
        queryset = Movie.objects.all()
        movie = get_object_or_404(queryset, pk=pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


class CommentViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Comment.objects.all()
        movie = request.query_params.get('movie', None)
        if movie is not None:
            queryset = queryset.filter(movie_id=movie)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        movie_id = request.data.get('movie', None)
        if movie_id is None:
            raise ValidationError('Movie shouldn\' be empty'.format(movie_id))

        movie = Movie.objects.filter(pk=movie_id).first()
        if movie is None:
            raise ValidationError('There is no such movie with id={}'.format(
                movie))

        body = request.data.get('body', None)
        if body is None:
            raise ValidationError('Content of the comment shouldn\' be empty')

        comment = Comment(movie=movie, body=body)
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=201)

    def retrieve(self, request, pk=None):
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)