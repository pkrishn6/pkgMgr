import graphene
import logging
from ..lib.pkg import PkgMgr
from .. import models  # Django ORM
from django.db import transaction
from django.utils import timezone

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
    logger.info("Handling mutation here")
    package = graphene.Field(Package)

    def mutate(self, info, name, author="", description="", deps=None):
        logger.info("Handling mutation")
        with transaction.atomic():
            # Atomic transaction to roll back if add_package throws exception
            package_deps = deps if deps else []
            p = models.Package(name=name, author=author, description=description)
            p.save()

            mgr.addPkg(name, package_deps)

        return CreatePackage(package=Query.resolve_package(self, info, name=p.name))


class DeletePackage(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    logger.info("Handling delete package mutation")
    success = graphene.Boolean(description="success of deletion operation")

    def mutate(self, info, name):
        with transaction.atomic():
            mgr.delPkg(name)

            p = models.Package.objects.select_for_update().get(name=name)
            p.delete()

        return DeletePackage(success=True)


class UpdatePackage(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        author = graphene.String()
        description = graphene.String()
        deps = graphene.List(graphene.String)

    # Return
    package = graphene.Field(Package)

    def mutate(self, info, name, author=None, description=None, deps=None):
        logger.info("Handling mutation")
        with transaction.atomic():
            # Atomic transaction to roll back if add_package throws exception
            p = models.Package.objects.select_for_update().get(name=name)

            if author:
                p.author = author
            if description:
                p.description = description

            p.last_modified_at = timezone.now()

            package_deps = deps if deps else []
            p.save()

            mgr.updatePkg(name, package_deps)

        return UpdatePackage(package=Query.resolve_package(self, info, name=p.name))


class Mutation:
    logger.error("Handling top level mutation")
    create_package = CreatePackage.Field()
    delete_package = DeletePackage.Field()
    update_package = UpdatePackage.Field()
