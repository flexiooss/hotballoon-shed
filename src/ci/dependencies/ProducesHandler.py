from ModuleHandler import ModuleHandler


class ProducesHandler(ModuleHandler):
    produces = []  # params: list
    docker_image = ''  # params: str
    repository = ''  # params: str
    version = ''  # params: str

    def __init__(self, docker_image, repository, version):
        # params: (str, str, str) -> None

        self.docker_image = docker_image
        self.repository = repository
        self.version = version

    def process(self):
        self._add_docker_image()
        return self

    def _add_docker_image(self):
        self.produces.append(
            self.module_item(
                self.SPEC_DOCKER_PREFIX + self.docker_image,
                self.version
            )
        )

    def _add_module(self):
        self.produces.append(
            self.module_item(
                self.SPEC_JS_PREFIX + self.repository,
                self.version
            )
        )
