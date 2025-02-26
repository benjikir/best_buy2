import store
import products


def start(store_obj):
    """Starts the Best Buy store user interface."""
    while True:
        print("\nWelcome to Best Buy Store!\n")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nAvailable Products:")
            for idx, product in enumerate(store_obj.get_all_products(), start=1):
                print(f"{idx}. {product.name} - ${product.price} - {product.quantity} in stock")

        elif choice == "2":
            print(f"Total quantity in store: {store_obj.get_total_quantity()}")

        elif choice == "3":
            shopping_list = []
            all_products = store_obj.get_all_products()

            while True:
                print("\nAvailable Products:")
                for idx, product in enumerate(all_products, start=1):
                    print(f"{idx}. {product.name} - ${product.price} - {product.quantity} in stock")

                product_choice = input("Enter product number or name (or 'done' to finish): ")
                if product_choice.lower() == "done":
                    break

                product = None

                if product_choice.isdigit():
                    product_index = int(product_choice) - 1
                    if 0 <= product_index < len(all_products):
                        product = all_products[product_index]
                else:
                    product = next((p for p in all_products if p.name.lower() == product_choice.lower()), None)

                if not product:
                    print("Invalid product selection. Please try again.")
                    continue

                try:
                    quantity = int(input("Enter quantity: "))
                    if quantity <= 0:
                        print("Quantity must be greater than zero.")
                        continue
                    if product.quantity < quantity:
                        print(f"Not enough stock available. Only {product.quantity} left.")
                        continue
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    continue

                shopping_list.append((product, quantity))

            if shopping_list:
                total_price = store_obj.order(shopping_list)
                print(f"Total price of your order: ${total_price}")
            else:
                print("No valid items in your order.")

        elif choice == "4":
            print("Thank you for shopping with us!")
            break

        else:
            print("Invalid choice. Please try again.")


# Setup initial stock of inventory
product_inventory = [
    products.Product("MacBook Air M2", price=1450, quantity=100),
    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    products.Product("Google Pixel 7", price=500, quantity=250)
]

best_buy = store.Store(product_inventory)
start(best_buy)