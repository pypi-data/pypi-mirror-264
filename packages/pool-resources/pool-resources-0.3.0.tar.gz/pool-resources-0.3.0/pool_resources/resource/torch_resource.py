"""TorchResource"""
from __future__ import annotations
from overrides import overrides
import numpy as np
import torch as tr
from torch import nn

from .resource import Resource, T1, T2
from ..logger import logger

def to_device(data, device: tr.device):
    """Moves a generic parameter to the desired torch device."""
    if isinstance(data, (tr.Tensor, nn.Module)):
        return data.to(device)
    if isinstance(data, list):
        return [to_device(x, device) for x in data]
    if isinstance(data, tuple):
        return tuple(to_device(x, device) for x in data)
    if isinstance(data, set):
        return {to_device(x, device) for x in data}
    if isinstance(data, dict):
        return {k: to_device(data[k], device) for k in data}
    if isinstance(data, dict):
        return dict({k: to_device(data[k], device) for k in data})
    if isinstance(data, np.ndarray):
        if data.dtype == object or np.issubdtype(data.dtype, np.unicode_):
            return to_device(data.tolist(), device)
        return tr.from_numpy(data).to(device)  # pylint: disable=no-member
    if isinstance(data, (int, float, bool, str)):
        return data
    logger.debug2(f"Got unknown type: {type(data)}")
    return data

class TorchResource(Resource):
    def __init__(self, device: str | tr.device):
        if isinstance(device, str):
            device = tr.device(device)
        self.device = device

    @overrides
    def enable(self, item: T1 | T2) -> T1 | T2:
        item = to_device(item, self.device)
        return item

    @overrides
    def disable(self, item: T1 | T2) -> T1 | T2:
        item = to_device(item, "cpu")
        return item

    def __str__(self):
        return f"Torch Resource (id: {self.device})"

    def __repr__(self):
        return str(self)
