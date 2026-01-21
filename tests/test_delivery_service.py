from typing import List
import unittest

from delivery.services.delivery_service import plan_shipments
from delivery.models.types import Package

class DeliveryCalculatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.num_vehicles = 2
        self.packages: List[Package] = [
            Package(package_no="PKG1", weight=50, base_price=100.0, distance=30),
            Package(package_no="PKG2", weight=75, base_price=100.0, distance=125),
            Package(package_no="PKG3", weight=175, base_price=100.0, distance=100),
            Package(package_no="PKG4", weight=110, base_price=100.0, distance=60),
            Package(package_no="PKG5", weight=155, base_price=100.0, distance=95),
        ]

    def test_plan_shipments_respects_vehicle_weight_limit(self) -> None:
        print("\n--- Test: Plan Shipments Respects Vehicle Weight Limit ---")
        print(f"Inputs: {len(self.packages)} packages, Max Weight=200")
        
        shipments = plan_shipments(self.packages, self.num_vehicles, vehicle_max_weight=200, speed=70)
        
        print(f"Result: {len(shipments)} shipments created")
        for i, shipment in enumerate(shipments):
            total_weight = sum(p.weight for p in shipment.packages)
            print(f"  Shipment {i+1}: Weight={total_weight}, Packages={[p.package_no for p in shipment.packages]}")
            
            try:
                self.assertLessEqual(total_weight, 200)
            except AssertionError as e:
                print(f"Status: FAILED - Shipment {i+1} exceeds weight limit! ({total_weight} > 200)")
                raise
        print("Status: SUCCESS")

    def test_plan_shipments_uses_all_packages(self) -> None:
        print("\n--- Test: Plan Shipments Uses All Packages ---")
        print(f"Inputs: {len(self.packages)} packages")
        
        shipments = plan_shipments(self.packages, self.num_vehicles, vehicle_max_weight=200, speed=70)
        
        shipped_numbers = sorted(p.package_no for s in shipments for p in s.packages)
        expected_numbers = sorted(p.package_no for p in self.packages)
        
        print(f"Result: Shipped Packages={shipped_numbers}")
        print(f"Expected: All Packages={expected_numbers}")
        
        try:
            self.assertEqual(shipped_numbers, expected_numbers)
            print("Status: SUCCESS")
        except AssertionError as e:
            print(f"Status: FAILED - {e}")
            raise

    def test_plan_shipments_correctly_calculates_delivery_time(self) -> None:
        print("\n--- Test: Plan Shipments Correctly Calculates Delivery Time ---")
        print(f"Inputs: {len(self.packages)} packages, 2 Vehicles, Speed=70")
        
        shipments = plan_shipments(self.packages, num_vehicles=self.num_vehicles, vehicle_max_weight=200, speed=70)

        results = {p.package_no: p.delivery_time for s in shipments for p in s.packages}
        
        expected_results = {
            "PKG1": 3.99,
            "PKG2": 1.78,
            "PKG3": 1.42,
            "PKG4": 0.85,
            "PKG5": 4.20
        }
        
        print("Verifying Delivery Times:")
        all_passed = True
        for pkg_id, expected_time in expected_results.items():
            actual_time = results.get(pkg_id)
            print(f"  {pkg_id}: Actual={actual_time}, Expected={expected_time}")
            if actual_time != expected_time:
                all_passed = False
                print(f"    -> FAILED: Expected {expected_time}, got {actual_time}")
        
        try:
            self.assertEqual(results["PKG1"], 3.99)
            self.assertEqual(results["PKG2"], 1.78)
            self.assertEqual(results["PKG3"], 1.42)
            self.assertEqual(results["PKG4"], 0.85)
            self.assertEqual(results["PKG5"], 4.20)
            print("Status: SUCCESS")
        except AssertionError as e:
            print(f"Status: FAILED - {e}")
            raise

if __name__ == "__main__":
    unittest.main()
