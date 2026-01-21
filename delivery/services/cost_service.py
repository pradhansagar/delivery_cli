from typing import List
from ..models.types import Package
from ..models.offers import find_offer_by_code

def calculate_delivery_costs(packages: List[Package]) -> None:
    for package in packages:
        offer = find_offer_by_code(package.offer_code)
        if offer is not None and offer.is_applicable(package.weight, package.distance):
            package.discount_percent = offer.discount_percent
        else:
            package.discount_percent = 0

        weight_charge = package.weight * 10
        distance_charge = package.distance * 5
        total_cost = package.base_price + weight_charge + distance_charge

        discount_amount = 0.0
        if package.discount_percent > 0:
            discount_amount = total_cost * (package.discount_percent / 100)
            total_cost = total_cost - discount_amount

        package.total_cost = total_cost 
        package.discount_amount = discount_amount
