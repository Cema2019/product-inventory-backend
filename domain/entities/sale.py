from dataclasses import dataclass


@dataclass
class Sale:
    id: int | None = None
    name: str = ""
    price: float = 0.0
    delivery: float = 0.0

    @property
    def total(self) -> float:
        return self.price + self.delivery
