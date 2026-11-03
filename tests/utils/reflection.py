from collections.abc import Iterator


def iter_all_subclasses[T](cls: type[T]) -> Iterator[type[T]]:
    for subclass in cls.__subclasses__():
        yield subclass
        yield from iter_all_subclasses(subclass)


def get_subclass_by_name[T](parent_class: type[T], class_name: str) -> type[T]:
    found_subclass: type[T] | None = None
    for subclass in iter_all_subclasses(parent_class):
        if subclass.__name__ == class_name:
            found_subclass = subclass
            break
    if found_subclass is None:
        raise ValueError(f'Unknown subclass "{class_name}" for parent "{parent_class.__name__}"')
    return found_subclass
