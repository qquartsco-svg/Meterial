from __future__ import annotations

from .contracts import StorageStage


def storage_margin_0_1(storage: StorageStage) -> float:
    if storage.capacity_kg <= 0.0:
        return 0.0
    return max(0.0, min(1.0, (storage.capacity_kg - storage.stored_mass_kg) / storage.capacity_kg))


def storage_power_w(storage: StorageStage) -> float:
    return storage.compression_power_w
