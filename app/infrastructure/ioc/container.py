from typing import Callable, Any


class DependencyContainer:
    """Контейнер зависимостей."""

    def __init__(self) -> None:
        self.__bindings: dict[Callable, Callable] = {}

    def bind(self, interface: Callable, implementation: Callable) -> None:
        """Привязка зависимости."""
        self.__bindings[interface] = implementation

    def bind_multiple(self, bindings: dict) -> None:
        """Привязка нескольких зависимостей."""
        for interface, implementation in bindings.items():
            self.bind(interface, implementation)

    def get(self, interface: Callable) -> Any:
        """Получение зависимости."""
        return self.__bindings[interface]
