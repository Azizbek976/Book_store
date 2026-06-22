# from rest_framework.response import Response
# from .models import Book
# from .serializers import BookSerializer
#
# class BookAPIView(APIView):
#
#     def get(self, request):
#         books = Book.objects.all()
#         serializer = BookSerializer(books, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = BookSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
#
#
#
#
#
#
#
#
#
#
#
# from rest_framework import generics
# from .models import Book
# from .serializers import BookSerializer
#
# class BookListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
# class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
#
#
#
#
#
#
#
#
#
#
#
#
# from rest_framework import viewsets
# from .models import Book
# from .serializers import BookSerializer
#
# class BookViewSet(viewsets.ModelViewSet):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
#
#
#
#
# from rest_framework.routers import DefaultRouter
# from .views import BookViewSet
#
# router = DefaultRouter()
# router.register('books', BookViewSet)
#
# urlpatterns = router.urls