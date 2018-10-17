import graphene


class Query(src.api.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
