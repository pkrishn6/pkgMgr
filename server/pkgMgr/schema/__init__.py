"""Collect all Queries and Mutations in this module."""

from . import package, common


class Query(package.Query,
           common.Query):
    pass


class Mutation(package.Mutation):
    pass
