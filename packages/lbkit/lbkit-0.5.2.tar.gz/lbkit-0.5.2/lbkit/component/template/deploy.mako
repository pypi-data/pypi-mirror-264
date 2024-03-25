from conan import ConanFile


class DeployConan(ConanFile):
    name = "deploy"
    settings = "os", "arch", "compiler", "build_type"
    description = "部署组件"
    url = "https://litebmc.com"
    homepage = ""
    generators = "CMakeDeps"
    package_type = "application"
    version = "0.0.1"
    license = "MulanPSL v2"

    def requirements(self):
    % for package in packages:
        self.requires("${package}")
    % endfor
        pass

