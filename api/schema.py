import graphene
from graphene_django.types import DjangoObjectType
from graphql_relay import from_global_id
from . import models


class SubstanceMoreInfoType(DjangoObjectType):
    class Meta:
        model = models.SubstanceMoreInfo
        interfaces = (graphene.relay.Node, )


class SubstanceType(DjangoObjectType):
    more_info = graphene.NonNull(graphene.List(graphene.NonNull(SubstanceMoreInfoType)))

    class Meta:
        model = models.Substance
        interfaces = (graphene.relay.Node, )

    def resolve_more_info(self, info):
        return self.more_info.all()


class SubCategoryMoreInfoType(DjangoObjectType):
    class Meta:
        model = models.SubCategoryMoreInfo
        interfaces = (graphene.relay.Node, )


class SubCategoryType(DjangoObjectType):
    substances = graphene.NonNull(graphene.List(graphene.NonNull(SubstanceType)))
    more_info = graphene.NonNull(graphene.List(graphene.NonNull(SubCategoryMoreInfoType)))

    class Meta:
        model = models.SubCategory
        interfaces = (graphene.relay.Node, )

    def resolve_substances(self, info):
        return self.substances.all()

    def resolve_more_info(self, info):
        return self.more_info.all()


class CategoryMoreInfoType(DjangoObjectType):
    class Meta:
        model = models.CategoryMoreInfo
        interfaces = (graphene.relay.Node, )


class CategoryType(DjangoObjectType):
    sub_categories = graphene.NonNull(graphene.List(graphene.NonNull(SubCategoryType)))
    more_info = graphene.NonNull(graphene.List(graphene.NonNull(CategoryMoreInfoType)))

    class Meta:
        model = models.Category
        interfaces = (graphene.relay.Node, )

    def resolve_sub_categories(self, info):
        return self.sub_categories.all()

    def resolve_more_info(self, info):
        return self.more_info.all()


class Query:
    categories = graphene.NonNull(graphene.List(graphene.NonNull(CategoryType)))
    sub_categories = graphene.NonNull(graphene.List(SubCategoryType), category=graphene.ID())
    substances = graphene.NonNull(
        graphene.List(graphene.NonNull(SubstanceType)),
        category=graphene.ID(),
        sub_category=graphene.ID(),
        e_number=graphene.String()
    )

    def resolve_categories(self, info):
        return models.Category.objects.all()

    def resolve_sub_categories(self, info, **kwargs):
        sub_categories = models.SubCategory.objects.all()
        if kwargs.get("category") is not None:
            sub_categories = sub_categories.filter(category=from_global_id(kwargs.get("category"))[1])
        return sub_categories

    def resolve_substances(self, info, **kwargs):
        substances = models.Substance.objects.all()
        if kwargs.get("category") is not None:
            substances = substances.filter(sub_category__category=from_global_id(kwargs.get("category"))[1])
        if kwargs.get("sub_category") is not None:
            substances = substances.filter(sub_category=from_global_id(kwargs.get("sub_category"))[1])
        if kwargs.get("e_number") is not None:
            substances = substances.filter(e_number__icontains=kwargs.get("e_number"))
        return substances
