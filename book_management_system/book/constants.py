from django.db import models

class GenreChoices(models.TextChoices):
    FICTION = ('FIC', 'Fiction')
    NON_FICTION = ('NF', 'Non-Fiction')
    MYSTERY = ('MYS', 'Mystery')
    FANTASY = ('FAN', 'Fantasy')
    BIOGRAPHY = ('BIO', 'Biography')
    SCIENCE_FICTION = ('SF', 'Science Fiction')
    THRILLER = ('THR', 'Thriller')
    ROMANCE = ('ROM', 'Romance')

class RatingChoices(models.IntegerChoices):
    ONE = (1, '1 Star')
    TWO = (2, '2 Stars')
    THREE = (3, '3 Stars')
    FOUR = (4, '4 Stars')
    FIVE = (5, '5 Stars')
