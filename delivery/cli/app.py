from .input_providers import InputProvider, ConsoleInputProvider, FileInputProvider
from .cost_handler import handle_cost_mode
from .delivery_handler import handle_delivery_mode

def run_app(provider: InputProvider, initial_mode: str = None) -> None:
    if initial_mode:
        mode = initial_mode
    else:
        mode = provider.get_input("Do you want to calculate cost or delivery? (cost(c)/delivery(d)): ").strip().lower()

    if mode == "cost" or mode == "c":
        handle_cost_mode(provider)
    elif mode == "delivery" or mode == "d":
        handle_delivery_mode(provider)
    else:
        print("Invalid choice. Please run the program again and choose 'cost', 'delivery'.")

def main() -> None:
    print("Welcome to Kiki's delivery service!")

    choice = input("Do you want to calculate cost, delivery, or import from file? (cost/delivery/file): ").strip().lower()

    if choice == "file" or choice == "f":
        file_path = "import/sample_input.txt"
        try:
            provider = FileInputProvider.from_file(file_path)
            run_app(provider)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except Exception as e:
            print(f"Error reading file: {e}")
    else:
        provider = ConsoleInputProvider()
        run_app(provider, initial_mode=choice)
