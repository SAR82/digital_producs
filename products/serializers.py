from rest_framework import serializers

from .models import Category, Product, File

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'description', 'avatar')

class FileSerializer(serializers.ModelSerializer):
    file_type = serializers.SerializerMethodField()
    class Meta:
        model = File
        fields = ('id', 'title', 'file', 'file_type')

    def get_file_type(self, obj):  # به جای عدد در فیلد تایپ خود اسم فایل رو در تایپ فایل میگذارد
        return obj.get_file_type_display()

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True)
    # files = FileSerializer(many=True)
    # foo = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'avatar', 'categories', 'url')

    # def get_foo(self, obj): این تابع برای اضافه کردن یک فیلد به  تمام پروداکت ها 
    #     return obj.id