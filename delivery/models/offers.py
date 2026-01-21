from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Offer:
    code: str
    discount_percent: int
    min_distance: float
    max_distance: float
    min_weight: float
    max_weight: float

    def is_applicable(self, weight: float, distance: float) -> bool:
        return self.min_distance <= distance <= self.max_distance and self.min_weight <= weight <= self.max_weight


OFFERS: List[Offer] = [
    Offer(
        code="OFR001",
        discount_percent=10,
        min_distance=0,
        max_distance=199,
        min_weight=70,
        max_weight=200,
    ),
    Offer(
        code="OFR002",
        discount_percent=7,
        min_distance=50,
        max_distance=150,
        min_weight=100,
        max_weight=250,
    ),
    Offer(
        code="OFR003",
        discount_percent=5,
        min_distance=50,
        max_distance=250,
        min_weight=10,
        max_weight=150,
    ),
]


def find_offer_by_code(code: str) -> Optional[Offer]:
    for offer in OFFERS:
        if offer.code.upper() == code.strip().upper():
            return offer
    return None

