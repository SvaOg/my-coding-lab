import json
from typing import Any


type Data = list[dict[str, Any]]


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


class DataPipeline:
    def __init__(self, loader: InMemoryLoader, transformer: CleanMissingFields) -> None:
        self.loader = loader
        self.transformer = transformer

    def run(self) -> None:
        # Use the injected loader
        data = self.loader.load()

        # Use the injected transformer
        cleaned = self.transformer.transform(data)

        # Hardcoded export
        self._export_to_json(cleaned)

    def _export_to_json(self, data: Data) -> None:
        with open("output.json", "w") as f:
            json.dump(data, f, indent=2)


def main():
    pipeline = DataPipeline(InMemoryLoader(), CleanMissingFields())
    pipeline.run()
    print("Pipeline completed. Output written to output.json")


if __name__ == "__main__":
    main()
