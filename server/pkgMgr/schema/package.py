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

    def resolve_name(self, info, **kwargs):
        return self.name

    def resolve_author(self, info, **kwargs):
        return self.author

    def resolve_description(self, info, **kwargs):
        return self.description

    def resolve_dependencies(self, info, **kwargs):
        pkg_name = kwargs.get('name')
        return mgr.getPkgDeps(pkg_name)


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

    @staticmethod
    def resolve_install_order(root, info, **kwargs):
        pkg_name = kwargs.get('name')
        return mgr.installOrder(pkg_name)


class CreatePackageInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    author = graphene.String(required=False)
    description = graphene.String(required=False)


class CreatePackage(graphene.Mutation):

    class Arguments:
        input = CreatePackageInput(required=True)

    # Return
    logger.error("Handling mutation here")
    package = graphene.Field(Package)

    def mutate(self, info, name):
        logger.error("Handling mutation")
        with transaction.atomic():
            # Atomic transaction to roll back if add_package throws exception
            package_name = input.name
            package_author = input.name if input.name else ""
            package_description = input.description if input.description else ""
            package_deps = []
            p = models.Package(name=package_name, author=package_author, description=package_description)
            p.save()

            mgr.addPkg(package_name, package_deps)

        return CreatePackage(ok=True)


class Mutation:
    logger.error("Handling top level mutation")
    create_package = CreatePackage.Field(description="Creates a new package.")
