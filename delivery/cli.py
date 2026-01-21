import sys
from typing import List

from .models.types import Package
from .services.cost_service import calculate_delivery_costs
from .services.delivery_service import plan_shipments


class InputProvider:
    def get_input(self, prompt: str = "") -> str:
        raise NotImplementedError


class ConsoleInputProvider(InputProvider):
    def get_input(self, prompt: str = "") -> str:
        return input(prompt)


class FileInputProvider(InputProvider):
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.index = 0

    def get_input(self, prompt: str = "") -> str:
        if self.index < len(self.lines):
            line = self.lines[self.index]
            self.index += 1
            return line
        sys.exit("Error: End of input file reached unexpectedly.")


class PreloadedConsoleInputProvider(ConsoleInputProvider):
    def __init__(self, preloaded: List[str]):
        self.preloaded = preloaded
        self.index = 0

    def get_input(self, prompt: str = "") -> str:
        if self.index < len(self.preloaded):
            val = self.preloaded[self.index]
            self.index += 1
            return val
        return super().get_input(prompt)


def run_app(provider: InputProvider) -> None:
    mode = provider.get_input("Do you want to calculate cost or delivery? (cost(c)/delivery(d)): ").strip().lower()

    packages: List[Package] = []

    if mode == "cost" or mode == "c":
        header = provider.get_input("Enter base_delivery_cost and no_of_packages (e.g. '100 3'): ").strip()
        parts = header.split()
        while len(parts) != 2:
            header = provider.get_input("Please re-enter two values: base_delivery_cost no_of_packages: ").strip()
            parts = header.split()
        base_price = float(parts[0])
        num_packages = int(parts[1])

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

    elif mode == "delivery" or mode == "d":
        header = provider.get_input("Enter base_delivery_cost and no_of_packages (e.g. '100 3'): ").strip()
        parts = header.split()
        while len(parts) != 2:
            header = provider.get_input("Please re-enter two values: base_delivery_cost no_of_packages: ").strip()
            parts = header.split()
        base_price = float(parts[0])
        num_packages = int(parts[1])

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
            print(f"{package.package_no} {package.discount_percent} {package.total_cost} {package.delivery_time}")

    else:
        print("Invalid choice. Please run the program again and choose 'cost', 'delivery'.")


def main() -> None:
    print("Welcome to Kiki's delivery service!")

    choice = input("Do you want to calculate cost, delivery, or import from file? (cost/delivery/file): ").strip().lower()

    if choice == "file" or choice == "f":
        file_path = "import/sample_input.txt"
        try:
            with open(file_path, 'r') as f:
                lines = [
                    line.strip() 
                    for line in f.readlines() 
                    if line.strip() and not line.strip().startswith("#") and not line.strip().startswith("//")
                ]
            provider = FileInputProvider(lines)
            run_app(provider)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except Exception as e:
            print(f"Error reading file: {e}")
    else:
        provider = PreloadedConsoleInputProvider([choice])
        run_app(provider)


if __name__ == "__main__":
    main()
