from dataclasses import dataclass
from typing import List

@dataclass
class Package:
    package_no: str
    weight: float
    base_price: float
    distance: float
    offer_code: str = ""
    discount_percent: float = 0.0
    total_cost: float = 0.0
    discount_amount: float = 0.0
    delivery_time: float = 0.0

@dataclass
class Shipment:
    packages: List[Package]
    total_weight: float
    max_distance: float
    delivery_time_hours: float

