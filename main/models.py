from array import array

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_delete
import os


class User(AbstractUser):
    image = models.ImageField(upload_to='profile' , null=True , blank=True)

    def __str__(self):
        return f'{self.username}'






class Book(models.Model):
    name = models.CharField(max_length=20)
    details = models.TextField(null=True , blank=True)
    price = models.FloatField(max_length=8 , validators=[MinValueValidator(0.0)])
    cover = models.CharField(max_length=30)
    created_at = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    sold = models.BooleanField(default=False)
    image = models.ImageField(upload_to='books' , null=True , blank=True)

    def __str__(self):
        return f'Nomi={self.name} --- Narxi={self.price} -- Ega={self.user} -- Mavjudligi={self.sold}'



class SavedList(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)


    def __str__(self):
        books = self.books.all()
        bookname = '---'.join(book.name for book in books)

        return f'{self.user.username} --- {bookname}'








    # def delete(self , *args , **kwargs):
    #     if self.image and os.path.isfile(self.image.path):
    #         os.remove(self.image.path)
    #     super().delete(*args , **kwargs)


# @receiver(post_delete , sender=Book)
# def delete_file(sender , instance , **kwargs):
#     if instance.image:
#         if os.path.isfile(instance.image.path):
#             os.remove(instance.image.path)











