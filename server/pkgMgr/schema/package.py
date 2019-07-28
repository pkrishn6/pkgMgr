import graphene
import logging
from ..lib.pkg import PkgMgr
from .. import models  # Django ORM
from django.db import transaction

logger = logging.getLogger(__name__)
mgr = PkgMgr()


class Package(graphene.ObjectType):
    id = graphene.UUID(description="Unique id of a project")
    name = graphene.String(description="Name of the package")
    author = graphene.String(description="Author of the package")
    created_at = graphene.DateTime(description="DateTime when the package was created")
    last_modified_at = graphene.DateTime(description="DateTime when the package was last modified")
    description = graphene.String(description="Package description")
    dependencies = graphene.List(graphene.String, description="All dependencies of package")
    install_order = graphene.List(graphene.String, description="Package installation order")

    def resolve_name(self, info, **kwargs):
        return self.name

    def resolve_author(self, info, **kwargs):
        return self.author

    def resolve_description(self, info, **kwargs):
        return self.description

    def resolve_dependencies(self, info, **kwargs):
        pkg_name = self.name
        return mgr.getPkgDeps(pkg_name)

    def resolve_install_order(self, info, **kwargs):
        pkg_name = self.name
        logger.info("package name is", pkg_name)
        return mgr.installOrder(pkg_name)


class Query:
    package = graphene.Field(Package, name=graphene.String(required=True),
                             description="Look up a package by name.")

    @staticmethod
    def resolve_package(root, info, **kwargs):
        name = kwargs.get('name')
        logger.info("Handling resolve_package")
        return models.Package.objects.get(name=name)

    @staticmethod
    def resolve_packages(root, info):
        return models.Package.objects.all()


class CreatePackage(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        author = graphene.String()
        description = graphene.String()
        deps = graphene.List(graphene.String)

    # Return
    logger.error("Handling mutation here")
    package = graphene.Field(Package)

    def mutate(self, info, name, author="", description="", deps=None):
        logger.error("Handling mutation")
        with transaction.atomic():
            # Atomic transaction to roll back if add_package throws exception
            package_deps = deps if deps else []
            p = models.Package(name=name, author=author, description=description)
            p.save()

            mgr.addPkg(name, package_deps)

        return CreatePackage(package=Query.resolve_package(self, info, name=p.name))


class Mutation:
    logger.error("Handling top level mutation")
    create_package = CreatePackage.Field()
