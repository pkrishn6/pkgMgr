"""
GraphQL Server Master
"""

import graphene
import pkgMgr.schema  # GraphQL Child Schema


class Query(pkgMgr.schema.Query, graphene.ObjectType):
    """
    This class will inherit from multiple Queries as we begin to add more apps to our project
    """
    pass


class Mutation(pkgMgr.schema.Mutation, graphene.ObjectType):
    """
    This class will inherit from multiple Mutations as we begin to add more apps to our project
    """
    pass


# GraphQL Parent Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
