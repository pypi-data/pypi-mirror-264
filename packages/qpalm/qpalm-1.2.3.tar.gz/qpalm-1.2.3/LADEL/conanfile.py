import os

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.build import can_run


class LADELRecipe(ConanFile):
    name = "ladel"
    version = "0.0.1"

    # Optional metadata
    license = "LGPLv3"
    author = "Pieter P <pieter.p.dev@outlook.com>"
    url = "https://github.com/kul-optec/LADEL"
    description = "Quasidefinite LDL factorization package with (symmetric) row/column adds and deletes"
    topics = ("LDL", "LDLT", "linear-algebra")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = (
        "CMakeLists.txt",
        "LADEL/*",
        "thirdparty/*",
        "test/*",
        "LICENSE",
        "README.md",
    )

    generators = ("CMakeDeps",)

    def requirements(self):
        self.test_requires("gtest/1.11.0")

    def config_options(self):
        if self.settings.get_safe("os") == "Windows":
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        if can_run(self):
            tc.variables["LADEL_FORCE_TEST_DISCOVERY"] = True
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.test()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "none")
        self.cpp_info.builddirs.append(os.path.join("lib", "cmake", "LADEL"))
