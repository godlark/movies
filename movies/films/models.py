from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    rated = models.CharField(max_length=20)
    released = models.DateField(null=True)
    runtime = models.CharField(max_length=20)
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=50)
    plot = models.TextField()
    language = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    imdbID = models.CharField(max_length=20, unique=True)


class Comment(models.Model):
    body = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name='comments')