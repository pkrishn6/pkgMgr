import graphene
from ..lib.pkg import PkgMgr
import logging

logger = logging.getLogger(__name__)


class Query:

    version = graphene.String(description="Return the current PkgMgr Version")

    @staticmethod
    def resolve_version(root, info, **kwargs):
        logger.info("Handling query for version")
        return PkgMgr.getVersion()
