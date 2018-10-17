from django.contrib import admin
from . import models


class SubstanceMoreInfoAdmin(admin.TabularInline):
    model = models.SubstanceMoreInfo


@admin.register(models.Substance)
class SubstanceAdmin(admin.ModelAdmin):
    inlines = [SubstanceMoreInfoAdmin]


class SubCategoryMoreInfoAdmin(admin.TabularInline):
    model = models.SubCategoryMoreInfo


@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryMoreInfoAdmin]


class CategoryMoreInfoAdmin(admin.TabularInline):
    model = models.CategoryMoreInfo


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryMoreInfoAdmin]