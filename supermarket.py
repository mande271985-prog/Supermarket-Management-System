import json
import os
from datetime import datetime

PRODUCT_FILE = "products.json"
SALES_FILE = "sales.json"


# Load products from file
def load_products():
    if os.path.exists(PRODUCT_FILE):
        try:
            with open(PRODUCT_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read product file.")
    return {}


# Save products to file
def save_products(products):
    with open(PRODUCT_FILE, "w") as file:
        json.dump(products, file, indent=4)


# Load sales from file
def load_sales():
    if os.path.exists(SALES_FILE):
        try:
            with open(SALES_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read sales file.")
    return []


# Save sales to file
def save_sales(sales):
    with open(SALES_FILE, "w") as file:
        json.dump(sales, file, indent=4)


# Add a new product
def add_product(products):
    product_id = input("Enter Product ID: ").strip()

    if not product_id:
        print("Product ID cannot be empty.")
        return

    if product_id in products:
        print("This Product ID already exists!")
        return

    name = input("Enter Product Name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = float(input("Enter Product Price: "))
        quantity = int(input("Enter Product Quantity: "))

        if price < 0 or quantity < 0:
            print("Price and quantity cannot be negative.")
            return

        products[product_id] = {
            "name": name,
            "price": price,
            "quantity": quantity
        }

        save_products(products)
        print("Product added successfully!")

    except ValueError:
        print("Please enter a valid price and quantity.")


# Display all products
def view_products(products):
    if not products:
        print("No products available.")
        return

    print("\n" + "-" * 65)
    print(f"{'ID':<12}{'Product Name':<20}"
          f"{'Price (Rs.)':<15}{'Quantity':<10}")
    print("-" * 65)

    for product_id, details in products.items():
        print(
            f"{product_id:<12}"
            f"{details['name']:<20}"
            f"{details['price']:<15.2f}"
            f"{details['quantity']:<10}"
        )

    print("-" * 65)


# Search for a product
def search_product(products):
    product_id = input("Enter Product ID: ").strip()

    if product_id in products:
        details = products[product_id]

        print("\nProduct Found!")
        print("Product ID:", product_id)
        print("Product Name:", details["name"])
        print("Price: Rs.", f"{details['price']:.2f}")
        print("Quantity:", details["quantity"])
    else:
        print("Product not found!")


# Update product information
def update_product(products):
    product_id = input("Enter Product ID to update: ").strip()

    if product_id not in products:
        print("Product not found!")
        return

    details = products[product_id]

    print("Press Enter to keep the current value.")

    name = input(f"New Name ({details['name']}): ").strip()
    price_text = input(f"New Price ({details['price']}): ").strip()
    quantity_text = input(
        f"New Quantity ({details['quantity']}): "
    ).strip()

    try:
        new_price = (
            float(price_text) if price_text else details["price"]
        )
        new_quantity = (
            int(quantity_text)
            if quantity_text else details["quantity"]
        )

        if new_price < 0 or new_quantity < 0:
            print("Price and quantity cannot be negative.")
            return

        if name:
            details["name"] = name

        details["price"] = new_price
        details["quantity"] = new_quantity

        save_products(products)
        print("Product updated successfully!")

    except ValueError:
        print("Invalid price or quantity. Please try again.")


# Delete a product
def delete_product(products):
    product_id = input("Enter Product ID to delete: ").strip()

    if product_id not in products:
        print("Product not found!")
        return

    confirm = input("Confirm deletion? (yes/no): ").strip().lower()

    if confirm == "yes":
        del products[product_id]
        save_products(products)
        print("Product deleted successfully!")
    else:
        print("Deletion cancelled.")


# Generate a customer bill
def generate_bill(products):
    if not products:
        print("No products available!")
        return

    cart = {}

    while True:
        product_id = input(
            "Enter Product ID (or type 'done' to finish): "
        ).strip()

        if product_id.lower() == "done":
            break

        if product_id not in products:
            print("Product not found!")
            continue

        try:
            quantity = int(input("Enter quantity to purchase: "))

            if quantity <= 0:
                print("Quantity must be greater than zero.")
                continue

            available = products[product_id]["quantity"]
            selected = cart.get(product_id, 0)

            if quantity + selected > available:
                print("Insufficient stock!")
                continue

            cart[product_id] = selected + quantity
            print("Product added to cart.")

        except ValueError:
            print("Please enter a valid whole number.")

    if not cart:
        print("No products selected.")
        return

    total = 0
    bill_items = []

    print("\n" + "=" * 55)
    print("              SUPERMARKET BILL")
    print("=" * 55)
    print("Date:", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print("-" * 55)
    print(f"{'Product':<20}{'Qty':<7}{'Price':<13}{'Amount':<12}")
    print("-" * 55)

    for product_id, quantity in cart.items():
        details = products[product_id]
        price = details["price"]
        amount = price * quantity
        total += amount

        print(
            f"{details['name']:<20}"
            f"{quantity:<7}"
            f"{price:<13.2f}"
            f"{amount:<12.2f}"
        )

        bill_items.append({
            "product_id": product_id,
            "name": details["name"],
            "quantity": quantity,
            "price": price,
            "amount": amount
        })

    print("-" * 55)
    print(f"TOTAL AMOUNT: Rs. {total:.2f}")
    print("=" * 55)

    # Reduce stock after completing the bill
    for product_id, quantity in cart.items():
        products[product_id]["quantity"] -= quantity

    save_products(products)

    sales = load_sales()
    sales.append({
        "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "items": bill_items,
        "total": total
    })

    save_sales(sales)
    print("Bill generated successfully!")


# View total sales
def view_sales():
    sales = load_sales()

    if not sales:
        print("No sales records available.")
        return

    total_sales = sum(sale["total"] for sale in sales)

    print("\n" + "=" * 45)
    print("               SALES REPORT")
    print("=" * 45)

    for number, sale in enumerate(sales, start=1):
        print(f"\nSale Number: {number}")
        print("Date:", sale["date"])
        print(f"Amount: Rs. {sale['total']:.2f}")

    print("-" * 45)
    print(f"TOTAL SALES: Rs. {total_sales:.2f}")
    print("=" * 45)


# Main menu
def main():
    products = load_products()

    while True:
        print("\n")
        print("=" * 40)
        print("   SUPERMARKET MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. Add New Product")
        print("2. View All Products")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Generate Customer Bill")
        print("7. View Total Sales")
        print("8. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_product(products)
        elif choice == "2":
            view_products(products)
        elif choice == "3":
            search_product(products)
        elif choice == "4":
            update_product(products)
        elif choice == "5":
            delete_product(products)
        elif choice == "6":
            generate_bill(products)
        elif choice == "7":
            view_sales()
        elif choice == "8":
            print("Thank you for using our system!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()