# Import monster

You need to create package called `import_monster`
This package has to provide method called `methods_importer`

Signature:
```python
def methods_importer(method_name: str, modules: List[Union[str, ModuleType]]) -> List[Callable]:
    ...
```

## What this method should do?

Method has to check if any of `modules` contains `callable` object with name `method_name` and return list of such objects

Additional requirements:

- pre-commit
- isort
- black
- flake8
