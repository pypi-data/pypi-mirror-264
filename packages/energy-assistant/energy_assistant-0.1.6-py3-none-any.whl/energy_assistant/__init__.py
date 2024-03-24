"""The application."""

import uuid
from abc import ABC, abstractmethod


class Optimizer(ABC):
    """Base class for optimizers."""

    @abstractmethod
    def get_optimized_power(self, deviceId: uuid.UUID) -> float:
        """Get the optimized power budget for a give device."""
        pass
