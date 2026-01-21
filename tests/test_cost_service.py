import unittest
from delivery.services.cost_service import calculate_delivery_costs
from delivery.models.types import Package

class CostCalculatorTests(unittest.TestCase):
    def test_calculate_delivery_costs_with_discount(self) -> None:
        print("\n--- Test: Calculate Delivery Costs With Discount ---")
        pkg = Package(package_no="PKG1", weight=80.0, base_price=100.0, distance=100.0, offer_code="OFR001")
        print(f"Input: {pkg}")
        
        calculate_delivery_costs([pkg])
        
        print(f"Result: Total Cost={pkg.total_cost}, Discount={pkg.discount_percent}%")
        expected_cost = 1260.0
        expected_discount = 10.0
        print(f"Expected: Total Cost={expected_cost}, Discount={expected_discount}%")

        try:
            self.assertAlmostEqual(pkg.total_cost, expected_cost)
            self.assertEqual(pkg.discount_percent, expected_discount)
            print("Status: SUCCESS")
        except AssertionError as e:
            print(f"Status: FAILED - {e}")
            raise

    def test_calculate_delivery_costs_without_discount(self) -> None:
        print("\n--- Test: Calculate Delivery Costs Without Discount ---")
        # Invalid offer criteria
        pkg = Package(package_no="PKG2", weight=5.0, base_price=50.0, distance=5.0, offer_code="OFR001")
        print(f"Input: {pkg}")
        
        calculate_delivery_costs([pkg])
        
        print(f"Result: Total Cost={pkg.total_cost}, Discount={pkg.discount_percent}%")
        expected_cost = 125.0
        expected_discount = 0.0
        print(f"Expected: Total Cost={expected_cost}, Discount={expected_discount}%")

        try:
            self.assertAlmostEqual(pkg.total_cost, expected_cost)
            self.assertEqual(pkg.discount_percent, expected_discount)
            print("Status: SUCCESS")
        except AssertionError as e:
            print(f"Status: FAILED - {e}")
            raise

    def test_calculate_delivery_costs_with_na_offer(self) -> None:
        print("\n--- Test: Calculate Delivery Costs With NA Offer ---")
        pkg = Package(package_no="PKG3", weight=10.0, base_price=100.0, distance=100.0, offer_code="NA")
        print(f"Input: {pkg}")
        
        calculate_delivery_costs([pkg])
        # Base: 100, Weight: 10*10=100, Dist: 100*5=500. Total = 700. Discount 0.
        
        print(f"Result: Total Cost={pkg.total_cost}, Discount={pkg.discount_percent}%")
        expected_cost = 700.0
        expected_discount = 0.0
        print(f"Expected: Total Cost={expected_cost}, Discount={expected_discount}%")

        try:
            self.assertEqual(pkg.total_cost, expected_cost)
            self.assertEqual(pkg.discount_percent, expected_discount)
            print("Status: SUCCESS")
        except AssertionError as e:
            print(f"Status: FAILED - {e}")
            raise

if __name__ == "__main__":
    unittest.main()