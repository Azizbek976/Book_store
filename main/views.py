from pydoc import resolve

from django.contrib.auth import user_logged_in
from django.template.context_processors import request
from drf_yasg import openapi
from drf_yasg.openapi import Response
from drf_yasg.utils import swagger_auto_schema
from pyexpat.errors import messages
from rest_framework.decorators import authentication_classes
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.permissions import SAFE_METHODS

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.views import APIView
from rest_framework.response import Response
from select import select

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
            ) ,
            openapi.Parameter(
                name = 'price' ,
                in_ = openapi.IN_QUERY ,
                type = openapi.TYPE_STRING ,
                description='Narxlar boyicha filterlash' ,
            )
        ]
    )




    def get(self , request , *args , **kwargs):
        return self.list(request , *args , **kwargs)





    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookSerializer
        else:
            return BookPostSerializer




    # def get_permissions(self):
    #     if self.request.method in SAFE_METHODS:
    #         return [AllowAny()]
    #     else:
    #         return [IsAuthenticated()]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class BookRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Book.objects.all()
    serializer_class = BookSerializer






    # def get_permissions(self):
    #     if self.request.method in SAFE_METHODS:
    #         return [AllowAny()]
    #     else:
    #         return [IsAuthenticated()]



    def perform_update(self, serializer):
        if serializer.instance != self.request.user:
            raise PermissionDenied(detail='Siz ushbu kitob egasi emassiz')
        serializer.save()




    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied(detail='Kechirasiz siz bu kitob egasi emassiz!')
        instance.delete()





class MyBookList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend , OrderingFilter , SearchFilter]
    filterset_fields = ['sold' , 'cover']
    ordering_filter = ['price' , 'created_at']
    search_fields = ['name' , ]
    pagination_class = BookPagination



    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name = 'sold' ,
                in_ = openapi.IN_QUERY ,
                type = openapi.TYPE_BOOLEAN ,
                description='Sotilganlar boyicha filterlash' ,
            ) ,
            openapi.Parameter(
                name = 'price' ,
                in_ = openapi.IN_QUERY ,
                type = openapi.TYPE_INTEGER ,
                description='Narxlar boyicha filterlash' ,
            ) ,
            openapi.Parameter(
                name = 'cover' ,
                in_ = openapi.IN_QUERY ,
                type = openapi.TYPE_STRING ,
                description='Muqova boyicha filterlash' ,
            )
        ]
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)



class BookMarkSoldView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self , request , pk):
        book = get_object_or_404(Book , pk=pk , user=request.user)
        serializer = BookMarkSoldSerializer(book , data=request.data)

        if serializer.is_valid():
            serializer.save(sold=True)
            response = {
                'success' : True ,
                'message' : 'Kitob sotildi' ,
                'data' : BookSerializer(book).data
            }
            return Response(response , status=status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)




    #
    # def perform_create(self, serializer):
    #     serializer.save()
    #     Wishlist.objects.create(user=serializer.instance)



class SavedListAPIVIew(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def get_queryset(self):
        savedlist = SavedList.objects.get(user=self.request.user)
        return savedlist.books.order_by('name')


class SevedListAddBookAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self , request , pk):

        user = self.request.user
        book = get_object_or_404(Book , pk=pk)
        savedlist = SavedList.objects.get(user=user)
        savedlist.books.add(book)
        savedlist.save()
        response = {
            'success' : True ,
            'message' : 'Kitob saqlanganlarga qoshildi'
        }
        return  Response(response , status=status.HTTP_201_CREATED)






class SevedListRemoveBookAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self , request , pk):
        user = self.request.user
        book = get_object_or_404(Book , pk=pk)
        savedlist = SavedList.objects.get(user=user)
        savedlist.books.remove(book)
        savedlist.save()

        response = {
            'success' : True ,
            'message' : 'Kitob saqlanganlardan muvafaqqiyatli olib tashlandi'
        }

        return Response(response , status=status.HTTP_204_NO_CONTENT)



































