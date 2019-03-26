from cmd.package.PackageHandler import PackageHandler


class ModulesHandler:
    def __init__(self, package: PackageHandler) -> None:
        self.__package: PackageHandler = package

    def __load_modules(self)->dict:
        if self.__package.config().get(PackageHandler.MODULES_KEY) is None:
            raise KeyError('No modules found')
        for name, module in self.__package.config().get(PackageHandler.MODULES_KEY):
            # TODO build module
            pass



