"""Modules for utilities."""
import math
import typing as t

if t.TYPE_CHECKING:
    import flywheel

TOP_DOWN_PARENT_HIERARCHY = ["group", "project", "subject", "session", "acquisition"]
BOTTOM_UP_PARENT_HIERARCHY = list(reversed(TOP_DOWN_PARENT_HIERARCHY))


def get_container_from_ref(client: "flywheel.Client", ref: dict):
    """Returns the container from its reference.

    Args:
        client: Authenticated Flywheel SDK client
        ref: A dictionary with type and id keys defined.

    Returns:
        Container: A flywheel container.
    """
    container_type = ref.get("type")
    getter = getattr(client, f"get_{container_type}")
    return getter(ref.get("id"))


def get_parent(client: "flywheel.Client", container):
    """Returns parent container of container input."""
    if container.container_type == "analysis":
        return get_container_from_ref(client, container.parent)
    elif container.container_type == "file":
        return container.parent
    elif container.container_type == "group":
        raise TypeError("Group container does not have a parent.")
    else:
        for cont_type in BOTTOM_UP_PARENT_HIERARCHY:
            if not container.parents.get(cont_type):
                # not defined, parent must be up the hierarchy
                continue
            return get_container_from_ref(
                client, {"type": cont_type, "id": container.parents.get(cont_type)}
            )


def trim(obj: dict):
    """Trim object for printing."""
    return {key: trim_lists(val) for key, val in obj.items()}


def trim_lists(obj: t.Any):
    """Replace a long list with a representation.

    List/Arrays greater than 5 in length will be replaced with the first two
    items followed by `...` then the last two items
    """
    if isinstance(obj, (list, tuple)):
        # Trim list
        if len(obj) > 5:
            return [*obj[:1], f"...{len(obj) - 2} more items...", *obj[-1:]]
        # Recurse into lists
        return [trim_lists(v) for v in obj]
    # Recurse into dictionaries
    if isinstance(obj, dict):
        return {key: trim_lists(val) for key, val in obj.items()}
    return obj


def deep_merge(base, **update):
    """Recursive merging of `update` dict on `base` dict.

    Instead of updating only top-level keys, `deep_merge` recurse down to
    perform a "nested" update.
    """
    for k, v in update.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            deep_merge(base[k], **v)
        else:
            base[k] = v


def convert_nan_in_dict(d: dict) -> dict:  # ruff: noqa: D103
    # Note: convert_nan_in_dict is borrowed from core-api
    return {key: _convert_nan(value) for key, value in d.items()}


def _convert_nan(
    d: t.Optional[t.Union[dict, str, list, float, int]]
) -> t.Optional[t.Union[dict, str, list, float, int]]:
    # Note: _convert_nan is borrowed from core-api
    """Return converted values."""
    if d is None:
        return None
    if isinstance(d, (str, int)):
        return d
    if isinstance(d, float):
        if math.isnan(d) or math.isinf(d):
            return None
        return d
    if isinstance(d, dict):
        return {key: _convert_nan(value) for key, value in d.items()}
    if isinstance(d, list):
        return [_convert_nan(item) for item in d]
    return d
