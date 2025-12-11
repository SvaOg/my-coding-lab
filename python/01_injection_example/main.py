import json
from typing import Any, Protocol, Callable


type Data = list[dict[str, Any]]


class DataLoader(Protocol):
    def load(self) -> Data: ...


class Transformer(Protocol):
    def transform(self, data: Data) -> Data: ...


class Exporter(Protocol):
    def export(self, cleaned_data) -> None: ...


class InMemoryLoader:
    def load(self) -> Data:
        return [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": None},
            {"name": "Charlie", "age": 25},
        ]


class CleanMissingFields:
    def transform(self, data: Data) -> Data:
        return [row for row in data if row["age"] is not None]


class JSONExporter:
    def __init__(self, fpath):
        self.fpath = fpath

    def export(self, cleaned_data: Data) -> None:
        with open(self.fpath, "w") as f:
            json.dump(cleaned_data, f, indent=2)


class Container:
    def __init__(self) -> None:
        self._providers: dict[str, tuple[Callable[[], Any], bool]] = {}
        self._singletons: dict[str, Any] = {}

    def register(
        self, name: str, provider: Callable[[], Any], singleton: bool = False
    ) -> None:
        self._providers[name] = (provider, singleton)

    def resolve(self, name: str) -> Any:
        if name in self._singletons:
            return self._singletons[name]
        if name not in self._providers:
            raise ValueError(f"No provider registered for {name=}.")
        provider, singleton = self._providers[name]
        instance = provider()
        if singleton:
            self._singletons[name] = instance
        return instance


class DataPipeline:
    def __init__(
        self,
        loader: DataLoader,
        transformer: Transformer,
        exporter: Exporter,
    ) -> None:
        self.loader = loader
        self.transformer = transformer
        self.exporter = exporter

    def run(self) -> None:
        # Use the injected loader
        data = self.loader.load()

        # Use the injected transformer
        transformed = self.transformer.transform(data)

        # Hardcoded export
        self.exporter.export(transformed)


def main():
    container = Container()
    container.register("loader", InMemoryLoader, singleton=True)
    container.register("transformer", CleanMissingFields, singleton=True)
    container.register("exporter", lambda: JSONExporter("output.json"), singleton=True)

    container.register(
        "pipeline",
        lambda: DataPipeline(
            loader=container.resolve("loader"),
            transformer=container.resolve("transformer"),
            exporter=container.resolve("exporter"),
        ),
    )

    container.resolve("pipeline").run()

    print("Pipeline completed. Output written to output.json")


if __name__ == "__main__":
    main()
