from pathlib import Path

from typing import List


class Config:
    BUILD_KEY: str = 'build'
    BUILDER_KEY: str = 'builder'
    BUILD_ENTRIES_KEY: str = 'entries'
    BUILD_HTML_TEMPLATE_KEY: str = 'html_template'
    BUILD_OUTPUT_KEY: str = 'output'
    MODULES_KEY: str = 'modules'
    TEST_KEY: str = 'test'
    TESTER_KEY: str = 'tester'
    TEST_PATH_KEY: str = 'path'
    GENERATE_SOURCES_KEY: str = 'generate-sources'
    VALUE_OBJECT_KEY: str = 'value-objects'
    VALUE_OBJECT_EXTENSION_KEY: str = 'extension'
    VALUE_OBJECT_VERSION_KEY: str = 'version'
    VALUE_OBJECT_PATH_KEY: str = 'path'

    def __init__(self, data: dict, cwd: Path) -> None:
        self.__data: dict = data
        self.__cwd: Path = cwd

    def has_generate_sources(self) -> bool:
        return self.__data.get(self.GENERATE_SOURCES_KEY) is not None

    def generate_sources(self) -> dict:
        return self.__data.get(self.GENERATE_SOURCES_KEY)

    def has_value_object(self) -> bool:
        return self.has_generate_sources() and self.generate_sources().get(self.VALUE_OBJECT_KEY) is not None

    def value_object(self) -> dict:
        return self.generate_sources().get(self.VALUE_OBJECT_KEY)

    def has_value_object_version(self) -> bool:
        return self.has_generate_sources() and self.has_value_object() and self.value_object().get(
            self.VALUE_OBJECT_VERSION_KEY) is not None

    def value_object_version(self) -> str:
        return self.value_object().get(self.VALUE_OBJECT_VERSION_KEY)

    def has_value_object_extension(self) -> bool:
        return self.has_generate_sources() and self.has_value_object() and self.value_object().get(
            self.VALUE_OBJECT_EXTENSION_KEY) is not None

    def value_object_extension(self) -> str:
        return self.value_object().get(self.VALUE_OBJECT_EXTENSION_KEY)

    def has_value_object_path(self) -> bool:
        return self.has_generate_sources() and self.has_value_object() and self.value_object().get(
            self.VALUE_OBJECT_PATH_KEY) is not None

    def value_object_path(self) -> Path:
        if not self.has_value_object_path():
            raise ValueError('No directory for value-object-generator defined')

        p: Path = Path(self.__cwd / self.value_object().get(self.VALUE_OBJECT_PATH_KEY))
        p.resolve()

        if not p.is_dir():
            raise FileNotFoundError('Not found directory for value-object-generator')
        return p

    def has_build(self) -> bool:
        return self.__data.get(self.BUILD_KEY) is not None

    def build(self) -> dict:
        return self.__data.get(self.BUILD_KEY)

    def has_build_entries(self) -> bool:
        return self.has_build() and self.build().get(self.BUILD_ENTRIES_KEY) is not None

    def build_entries(self) -> List[Path]:
        if not self.has_build_entries():
            raise ValueError('No build entries defined')
        entries: List[Path] = []
        v: str
        for v in self.build().get(self.BUILD_ENTRIES_KEY):

            p: Path = Path(self.__cwd / v)
            p.resolve()
            if not p.is_file():
                raise FileNotFoundError('Not found entry path : ' + p.as_posix())
            entries.append(p)

        return entries

    def has_build_output(self) -> bool:
        return self.has_build() and self.build().get(self.BUILD_OUTPUT_KEY) is not None

    def build_output(self) -> Path:
        if not self.has_build_output():
            raise ValueError('No output build path defined')

        p: Path = Path(self.__cwd / self.build().get(self.BUILD_OUTPUT_KEY))
        p.resolve()

        return p

    def has_build_html_template(self) -> bool:
        return self.has_build() and self.build().get(self.BUILD_HTML_TEMPLATE_KEY) is not None

    def build_html_template(self) -> Path:
        if not self.has_build_html_template():
            raise ValueError('No html template path defined')

        p: Path = Path(self.__cwd / self.build().get(self.BUILD_HTML_TEMPLATE_KEY))
        p.resolve()

        if not p.is_file():
            raise FileNotFoundError('Not found html template : ' + p.as_posix())
        return p

    def has_builder(self) -> bool:
        return self.has_build() and self.build().get(self.BUILDER_KEY) is not None

    def builder(self) -> str:
        return self.build().get(self.BUILDER_KEY)

    def has_test(self) -> bool:
        return self.__data.get(self.TEST_KEY) is not None

    def has_tester(self) -> bool:
        return self.has_test() and self.test().get(self.TESTER_KEY) is not None

    def test(self) -> dict:
        return self.__data.get(self.TEST_KEY)

    def tester(self) -> str:
        return self.test().get(self.TESTER_KEY)

    def has_test_dir(self) -> bool:
        return self.test().get(self.TEST_PATH_KEY) is not None

    def test_dir(self) -> Path:
        if not self.has_test_dir():
            raise ValueError('No test dir defined')

        p: Path = Path(self.__cwd / self.test().get(self.TEST_PATH_KEY))
        p.resolve()

        if not p.is_dir():
            raise FileNotFoundError('Not found test path')
        return p

    def has_modules(self) -> bool:
        return self.__data.get(self.MODULES_KEY) is not None

    def modules(self) -> dict:
        return self.__data.get(self.MODULES_KEY)
