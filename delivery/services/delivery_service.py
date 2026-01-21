import math
from typing import List

from ..models.types import Package, Shipment

def truncate(number: float, digits: int) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def shipments(pkgs: List[Package], max_weight: float) -> List[Package]:
    max_count: int = -1
    max_shipment_weight: int = -1
    shipment_combination: List[Package] = []

    def get_best_shipment(index: int, shipment: List[Package], weight: float):
        nonlocal shipment_combination, max_count, max_shipment_weight
        if (index == len(pkgs)):
            shipment_length = len(shipment)
            shipment_weight = sum(pkg.weight for pkg in shipment)
            if (shipment_length > max_count):
                max_count = shipment_length
                max_shipment_weight = shipment_weight
                shipment_combination = list(shipment)
            elif (shipment_length == max_count):
                if (shipment_weight > max_shipment_weight):
                    max_shipment_weight = shipment_weight
                    shipment_combination = list(shipment)
            return

        if (weight + pkgs[index].weight <= max_weight):
            shipment.append(pkgs[index])
            get_best_shipment(index + 1, shipment, weight + pkgs[index].weight)
            shipment.pop()

        get_best_shipment(index + 1, shipment, weight)
        
    get_best_shipment(0, [], 0)
    return shipment_combination

def plan_shipments(packages: List[Package], num_vehicles: int, vehicle_max_weight: float, speed: float) -> List[Shipment]:
    remaining_packages: List[Package] = list(packages)
    vehicle_return_time = [0.0] * num_vehicles
    shipments_list: List[Shipment] = []

    while remaining_packages:
        shipment_pkgs = shipments(remaining_packages, vehicle_max_weight)
        if not shipment_pkgs:
            break

        earliest_return_time: float = min(vehicle_return_time)
        vehicle_index: int = vehicle_return_time.index(earliest_return_time)

        max_distance: float = 0.0
        total_weight: float = 0.0
        
        for package in shipment_pkgs:
            package.delivery_time = truncate(earliest_return_time + (package.distance / speed), 2)

            if package.distance > max_distance:
                max_distance = package.distance
            
            total_weight += package.weight
            remaining_packages.remove(package)
        
        trip_time = max_distance / speed
        vehicle_return_time[vehicle_index] = truncate(earliest_return_time + (2 * trip_time), 2)

        shipments_list.append(
            Shipment(
                packages=shipment_pkgs,
                total_weight=total_weight,
                max_distance=max_distance,
                delivery_time_hours=trip_time
            )
        )
        
    return shipments_list
