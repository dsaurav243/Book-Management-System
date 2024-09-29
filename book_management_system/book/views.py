from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# from common.llama_model import generate_summary

class BookAPIView(APIView):
    """API endpoint for managing books."""

    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Add a new book",
        request_body=BookSerializer,
        responses={201: BookSerializer}
    )
    def post(self, request):
        """Create a new book."""
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError(serializer.errors)

    # For GET request, you use query_serializer or manual_parameters
    @swagger_auto_schema(
        operation_description="Retrieve all books",
        responses={200: BookSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('author', openapi.IN_QUERY, description="Author name", type=openapi.TYPE_STRING),
            openapi.Parameter('genre', openapi.IN_QUERY, description="Genre of the book", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request):
        """Retrieve all books."""
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class SingleBookAPIView(APIView):
    """API endpoint for managing a specific book."""

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """Retrieve a specific book by its ID."""
        try:
            book = get_object_or_404(Book, id=id)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Exception as e:
            raise NotFound(f"Book with id {id} does not exist.") from e

    def put(self, request, id):
        """Update a book's information by its ID."""
        book = get_object_or_404(Book, id=id)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        raise ValidationError(serializer.errors)

    def delete(self, request, id):
        """Delete a book by its ID."""
        try:
            book = get_object_or_404(Book, id=id)
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            raise NotFound(f"Book with id {id} could not be deleted.") from e

class ReviewAPIView(APIView):
    """API endpoint for managing reviews of a book."""

    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        """Add a review for a book."""
        book = get_object_or_404(Book, id=id)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(book=book, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError(serializer.errors)

    def get(self, request, id):
        """Retrieve all reviews for a book."""
        book = get_object_or_404(Book, id=id)
        reviews = book.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class BookSummaryAPIView(APIView):
    """API endpoint to get a summary and aggregated rating for a book."""

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """Get a summary and aggregated rating for a book."""
        try:
            book = get_object_or_404(Book, id=id)
            reviews = book.reviews.all()
            total_rating = sum(review.rating for review in reviews)
            avg_rating = total_rating / reviews.count() if reviews.exists() else 0

            summary = {
                "title": book.title,
                "summary": book.summary,
                "average_rating": avg_rating,
                "total_reviews": reviews.count(),
            }
            return Response(summary)
        except Exception as e:
            raise NotFound(f"Summary for book with id {id} could not be retrieved.") from e

class RecommendationAPIView(APIView):
    """API endpoint to get book recommendations based on user preferences."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get book recommendations based on user preferences."""
        # Sample implementation (customize based on actual logic)
        recommended_books = Book.objects.filter(genre__in=['FIC', 'NF'])  # Example filter
        serializer = BookSerializer(recommended_books, many=True)
        return Response(serializer.data)

# class GenerateSummaryAPIView(APIView):
#     """API endpoint to generate a summary for a given book content."""

#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         """Generate a summary for a given book content."""
#         content = request.data.get('content')
#         if not content:
#             raise ValidationError("Content is required to generate a summary.")
        
#         # Placeholder for summary generation logic
#         generated_summary = f"Generated summary for the content: {content[:50]}..."  # Just a placeholder

#         return Response({"summary": generated_summary}, status=status.HTTP_200_OK)

# class GenerateBookSummaryAPIView(APIView):
#     """API to generate a summary for a book's content."""

#     def post(self, request):
#         """Generate a summary for the provided book content."""
#         content = request.data.get('content')
#         if not content:
#             return Response({"error": "Book content is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             summary = generate_summary(content)
#             return Response({"summary": summary}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class GenerateReviewSummaryAPIView(APIView):
#     """API to generate a summary for a review's content."""

#     def post(self, request):
#         """Generate a summary for the provided review content."""
#         review_content = request.data.get('review_content')
#         if not review_content:
#             return Response({"error": "Review content is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             summary = generate_summary(review_content)
#             return Response({"summary": summary}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)