from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class Package:
    def __init__(self, name):
        self.name = name


class PkgMgr:
    def __init__(self):
        self.g = defaultdict(list)
        self.mapping = {}

    @classmethod
    def getVersion(cls):
        return "1.0.0"

    def getPkgInfo(self, pkgName):
        if pkgName not in self.mappings:
            return None

        pkg = self.mapping[pkgName]

        return pkg.name

    def getPkgDeps(self, pkgName):
        if pkgName not in self.mapping:
            return None
        pkgObj = self.mapping[pkgName]

        result = []
        for dep in self.g[pkgObj]:
            result.append(dep.name)
            logger.info("Package deps are:", result)
        return result

    def addPkg(self, pkgName, deps):
        for dep in deps:
            if dep not in self.mapping:
                raise Exception("Dep package not found", dep)

        pkgObj = Package(pkgName)
        self.mapping[pkgName] = pkgObj

        for dep in deps:
            depObj = self.mapping[dep]
            self.g[pkgObj].append(depObj)

    def installOrder(self, pkgName):
        if pkgName not in self.mapping:
            raise Exception("Package not found", pkgName)

        install_order = []
        GRAY, BLACK = 1, 2
        colors = defaultdict(int)

        def dfs(pkg):
            colors[pkg] = GRAY
            for dep in self.g[pkg]:
                if colors[dep] == GRAY:
                    return False
                elif colors[dep] == BLACK:
                    continue
                elif not dfs(dep):
                    return False
            colors[pkg] = BLACK
            install_order.append(pkg.name)
            return True

        pkgObj = self.mapping[pkgName]
        if dfs(pkgObj):
            return True, install_order

        return False, []


if __name__ == "__main__":
    pkgMgr = PkgMgr()
    pkgMgr.addPkg("pkgF", [])
    pkgMgr.addPkg("pkgE", ["pkgF"])
    pkgMgr.addPkg("pkgD", ["pkgE"])
    pkgMgr.addPkg("pkgC", [])
    pkgMgr.addPkg("pkgB", [])
    pkgMgr.addPkg("pkgA", ["pkgB", "pkgC", "pkgD"])

    possible, install_order = pkgMgr.installOrder("pkgA")
    print(possible, install_order)
