import json
from typing import Dict, List, Optional, Type, TypeVar

from latch.types.metadata import _IsDataclass

T = TypeVar("T", bound=_IsDataclass)


def get_boolean_value(channel_value: str) -> bool:
    og_error: Optional[Exception] = None

    try:
        payload = json.loads(channel_value)

        if type(payload) is list:
            return payload[0]["boolean"]
        elif type(payload) is dict:
            return payload["value"]["boolean"]
    except Exception as e:
        og_error = e

    error = ValueError(
        f"Unable to extract boolean value for conditional: {channel_value}"
    )
    if og_error is not None:
        raise error from og_error

    raise error


def get_mapper_inputs(
    cls: Type[T],
    wf_inputs: Dict[str, object],
    channel_inputs: Dict[str, str],
) -> List[T]:
    value_channels = {}
    queue_channels = {}

    min_len = float("inf")
    for param_name, channel in channel_inputs.items():
        values = json.loads(channel)

        if type(values) == list:
            queue_channels[param_name] = values
            min_len = min(min_len, len(values))
        else:
            value_channels[param_name] = channel

    if min_len == float("inf"):
        min_len = 1

    res: List[T] = []
    for i in range(min_len):
        kwargs = {**wf_inputs, **value_channels}

        for k, v in queue_channels.items():
            kwargs[k] = json.dumps([v[i]])

        res.append(cls(**kwargs))

    return res
