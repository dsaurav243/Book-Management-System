from django.db import models
from django.utils import timezone
from django.conf import settings
from .constants import GenreChoices, RatingChoices

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Book(BaseModel):
    title = models.CharField(max_length=255, db_index=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_books')
    genre = models.CharField(max_length=3, choices=GenreChoices.choices)
    year_published = models.IntegerField()
    summary = models.TextField()

    def __str__(self):
        return self.title

class Review(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reviews')
    review_text = models.TextField()
    rating = models.IntegerField(choices=RatingChoices.choices)

    def save(self, *args, **kwargs):
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review of {self.book.title} by {self.user.username}"