class ModuleHandler:
    SPEC_JS_PREFIX = 'js::'
    SPEC_DOCKER_PREFIX = 'docker::'
    DEFAULT_VERSION = 'master'

    def module_item(self, spec, version):
        # type: (str, str) -> dict

        return {
            'spec': spec,
            'version': version
        }

    @staticmethod
    def merge_dicts(x, y):
        # type: (dict, dict) -> dict
        if isinstance(x, dict) and len(x) and isinstance(y, dict) and len(y):
            z = x.copy()
            z.update(y)
            return z
        elif isinstance(x, dict) and len(x) and (not isinstance(y, dict) or not len(y)):
            return x
        elif isinstance(y, dict) and len(y) and (not isinstance(x, dict) or not len(x)):
            return y
        else:
            return {}
