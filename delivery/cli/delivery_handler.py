from typing import List

from ..models.types import Package
from ..services.cost_service import calculate_delivery_costs
from ..services.delivery_service import plan_shipments
from .input_providers import InputProvider

def handle_delivery_mode(provider: InputProvider) -> None:
    header = provider.get_input("Enter base_delivery_cost and no_of_packages (e.g. '100 3'): ").strip()
    parts = header.split()
    while len(parts) != 2:
        header = provider.get_input("Please re-enter two values: base_delivery_cost no_of_packages: ").strip()
        parts = header.split()
    base_price = float(parts[0])
    num_packages = int(parts[1])

    packages: List[Package] = []

    for _ in range(num_packages):
        line = provider.get_input("Enter pkg_id weight_kg distance_km offer_code: ").strip()
        parts = line.split()
        while len(parts) != 4:
            line = provider.get_input("Please re-enter: pkg_id weight_kg distance_km offer_code: ").strip()
            parts = line.split()
        package_no = parts[0]
        weight = float(parts[1])
        distance = float(parts[2])
        offer_code = parts[3]

        packages.append(
            Package(
                package_no=package_no,
                weight=weight,
                base_price=base_price,
                distance=distance,
                offer_code=offer_code,
            )
        )

    calculate_delivery_costs(packages)

    vehicle_line = provider.get_input("Enter no_of_vehicles max_speed max_carriable_weight: ").strip()
    parts = vehicle_line.split()
    while len(parts) != 3:
        vehicle_line = provider.get_input("Please re-enter: no_of_vehicles max_speed max_carriable_weight: ").strip()
        parts = vehicle_line.split()
    
    number_of_vehicles = int(parts[0])
    max_speed = float(parts[1])
    max_carriable_weight = float(parts[2])

    plan_shipments(packages, number_of_vehicles, max_carriable_weight, max_speed)

    packages.sort(key=lambda p: p.package_no)
    for package in packages:
        print(f"Package {package.package_no} will be delivered in {package.delivery_time} hours, the total cost is {package.total_cost} and discount amount is {package.discount_amount}")
