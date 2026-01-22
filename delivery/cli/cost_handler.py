from typing import List

from ..models.types import Package
from ..services.cost_service import calculate_delivery_costs
from .input_providers import InputProvider

def handle_cost_mode(provider: InputProvider) -> None:
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
        package_id = parts[0]
        weight = float(parts[1])
        distance = float(parts[2])
        offer_code = parts[3]

        packages.append(
            Package(
                package_no=package_id,
                weight=weight,
                base_price=base_price,
                distance=distance,
                offer_code=offer_code,
            )
        )

    calculate_delivery_costs(packages)

    for package in packages:
        print("Total cost for", package.package_no, "is", package.total_cost, "with discount amount", package.discount_amount)
