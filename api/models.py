from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    more_info = models.URLField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')
    name = models.CharField(max_length=255)
    more_info = models.URLField()

    class Meta:
        verbose_name_plural = "Sub categories"

    def __str__(self):
        return self.name


class Substance(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='substances')
    name = models.CharField(max_length=255)
    e_number = models.PositiveIntegerField()
    more_info = models.URLField()

    def __str__(self):
        return self.name
