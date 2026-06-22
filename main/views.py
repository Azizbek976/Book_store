from drf_yasg import openapi
from drf_yasg.openapi import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.permissions import SAFE_METHODS

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializer import *
from .pagination import *






class RegisterCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]



class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user






class BookListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Book.objects.all()

    filter_backends = [DjangoFilterBackend , SearchFilter , OrderingFilter]
    filterset_fields = ['name' , 'price' , 'cover' , 'user']
    search_fields = ['title' , ]
    ordering_fields = ['title' , 'price' , 'created_at']
    pagination_class = BookPagination


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name = 'sold' ,
                in_ = openapi.IN_QUERY ,
                type = openapi.TYPE_BOOLEAN ,
                description='Sotilganlar boyicha filterlash' ,
            )
        ]
    )






    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookSerializer
        else:
            return BookPostSerializer




    # def get_permissions(self):
    #     if self.request.method in SAFE_METHODS:
    #         return [AllowAny]
    #     else:
    #         return [IsAuthenticated]


    def perform_create(self, serializer):
        print(self.request.user)

        serializer.save(user=self.request.user)








class BookRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()



    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)




    # def get_permissions(self):
    #     if self.request.method in SAFE_METHODS:
    #         return [AllowAny()]
    #     else:
    #         return [IsAuthenticated()]



    def perform_update(self, serializer):
        book = serializer.instance
        if book.user != self.request.user:
        # if serializer.validated_data['user'] != self.request.user.id:
            return Response(
                {
                'success' : False ,
                'message' : 'Siz ushbu kitob egasi emassiz!'
            }
            )
        serializer.save()






















