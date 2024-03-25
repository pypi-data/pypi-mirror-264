from abc import ABC


ANNOTATIONS = "__annotations__"


class DIContainer:
    def __init__(self):
        self.registration_lookup = {}

    def assert_implementation(self, interface: ABC, concrete_class):
        """Assert that the concrete class implements the interface
        being registered."""
        if interface not in concrete_class.__bases__:
            raise TypeError(f"Concrete class: {concrete_class}"
                            f" has to implement interface: {interface}.")

    def assert_abstract_class(self, interface: ABC):
        """Assert that the interface being registered is an abstract class."""
        if ABC not in interface.__bases__:
            raise TypeError(f"Interface: {interface}"
                            f" has to be an abstract class.")

    def register_interface(self, interface: ABC, concrete_class):
        """Register interface with a corresponding concrete class to use."""
        self.assert_abstract_class(interface)
        self.assert_implementation(interface, concrete_class)
        self.registration_lookup[interface] = concrete_class

    def build(self, interface: ABC):
        """Build a given interface using its corresponding class registered
        in the lookup."""
        if interface not in self.registration_lookup:
            raise TypeError(f"Interface: {interface} is not registered.")

        concrete_class = self.registration_lookup[interface]
        if hasattr(concrete_class.__init__, ANNOTATIONS):
            dependancies = getattr(concrete_class.__init__, ANNOTATIONS)
            if 'return' in dependancies:
                dependancies.pop('return')
            concrete_dependancies = {param: self.build(
                interface) for param, interface in dependancies.items()}
            if (concrete_dependancies):
                return concrete_class(**concrete_dependancies)

        return concrete_class()
