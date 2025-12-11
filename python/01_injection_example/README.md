# Dependency Injection in Python

Topic: Design Patterns, Architecture, Inversion of Control

Source: Stop Hardcoding Everything: Use Dependency Injection

Date: 2025-12-08

Tags: #learning #python #dependency-injection #testing

## 🚀 Quick Start (uv)

How to run the refactored pipeline.

```
# 1. Install dependencies (if any)
uv sync

# 2. Run the main pipeline script
uv run src/main.py

# 3. Run tests (now easier with mocks!)
uv run pytest
```

## 🧠 Key Concepts Learned

- **Inversion of Control:** Instead of a class creating its own dependencies (e.g., `self.loader = CSVLoader()`), instances are passed in (injected) via the constructor.
    
- **Protocols (Structural Subtyping):** Using `typing.Protocol` to define the _shape_ of a dependency (e.g., "anything that has a `.load()` method") rather than inheriting from Abstract Base Classes.
    
- **Containers:** A pattern to centralize the logic of instantiating and wiring objects, though manual wiring in `main()` is often sufficient.
    

## 🏗️ Design Decisions & Architecture

- **Why I used Manual Wiring instead of a DI Framework:**
    
    - _Context:_ Arjan demonstrates building a custom `Container` class but concludes it's often overkill.
        
    - _Decision:_ For 99% of apps, manually instantiating objects in `main()` and passing them is clearer and less "magical" than using complex frameworks like `inject`.
        
- **Abstraction Layer:**
    
    - Decoupled `DataPipeline` from concrete classes (like `JSONExporter`).
        
    - It now relies on abstract interfaces (`Loader`, `Transformer`, `Exporter`), making it easy to swap CSV for Database implementations later.
        

## 📝 Notes & Observations

### The "Aha!" Moments

- **Testing is the biggest winner:** By injecting the `Loader`, I can easily inject a `MockLoader` that returns hardcoded list data during tests, avoiding file I/O entirely.
    
- **Protocols don't enforce inheritance:** A class doesn't need to inherit from `Loader` to be treated as one; it just needs a `load()` method.
    

### Gotchas & Errors

- **Complexity Trap:** It's tempting to build a generic `Container` that handles Singletons and Providers (like in the video), but this often makes the code harder to follow than just `pipeline = Pipeline(loader=CSVLoader())`.
    
- **Runtime Ignorance:** Python type hints (Protocols) are ignored at runtime. If you pass an object missing the `load()` method, it will crash _when called_, not when instantiated (unless you use static analysis tools like `mypy`).
    

## 💻 Code Highlights

_Using Protocols to define what the pipeline expects, without binding it to a specific class._

```
from typing import Protocol, Any

# The pipeline doesn't care if it's a CSV or Database loader
# It only cares that it has a load() method.
class Loader(Protocol):
    def load(self) -> Any:
        ...

class DataPipeline:
    # We inject the dependency here
    def __init__(self, loader: Loader):
        self.loader = loader

    def run(self):
        # We use the injected behavior
        data = self.loader.load()
```

## 🔮 Future Improvements / Ideas

- [ ] Refactor existing ETL scripts to use this pattern.
    
- [ ] Try using `FastAPI`'s built-in dependency injection system (`Depends`).
    
- [ ] Add unit tests using `unittest.mock` to verify the pipeline logic in isolation.