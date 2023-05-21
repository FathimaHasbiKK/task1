# Catalog of products and their prices
products = {
    "Product A": 20,
    "Product B": 40,
    "Product C": 50
}

# Discount rules
discount_rules = {
    "flat_10_discount": {"threshold": 200, "discount": 10},
    "bulk_5_discount": {"threshold": 10, "discount": 0.05},
    "bulk_10_discount": {"threshold": 20, "discount": 0.10},
    "tiered_50_discount": {"quantity_threshold": 30, "single_product_threshold": 15, "discount": 0.50}
}

# Fees
gift_wrap_fee = 1
shipping_fee_per_package = 5
units_per_package = 10

# Function to calculate the total amount for a product based on its quantity and gift wrap status
def calculate_product_total(name, quantity, is_gift_wrapped):
    unit_price = products[name]
    total_amount = unit_price * quantity
    if is_gift_wrapped:
        total_amount += gift_wrap_fee * quantity
    return total_amount

# Function to calculate the discount amount based on the applicable discount rule and cart total
def calculate_discount(cart_total):
    applicable_discounts = []
    for rule, details in discount_rules.items():
        if rule == "flat_10_discount" and cart_total > details["threshold"]:
            applicable_discounts.append((rule, details["discount"]))
        elif rule == "bulk_10_discount" and total_quantity > details["threshold"]:
            applicable_discounts.append((rule, cart_total * details["discount"]))
        elif (
            rule == "tiered_50_discount"
            and total_quantity > details["quantity_threshold"]
            and any(quantity > details["single_product_threshold"] for quantity in quantities.values())
        ):
            total_discount = sum(
                (quantity - details["single_product_threshold"]) * products[name] * details["discount"]
                for name, quantity in quantities.items()
                if quantity > details["single_product_threshold"]
            )
            applicable_discounts.append((rule, total_discount))
    if applicable_discounts:
        return max(applicable_discounts, key=lambda x: x[1])
    else:
        return None

# Get the quantity and gift wrap status for each product
quantities = {}
is_gift_wrapped = {}
for name in products:
    quantity = int(input(f"Enter the quantity for {name}: "))
    quantities[name] = quantity
    gift_wrapped = input(f"Is {name} wrapped as a gift? (yes/no): ").lower()
    is_gift_wrapped[name] = gift_wrapped == "yes"

# Calculate the subtotal and apply the discount
subtotal = sum(calculate_product_total(name, quantity, is_gift_wrapped[name]) for name, quantity in quantities.items())
total_quantity = sum(quantities.values())
discount_name, discount_amount = calculate_discount(subtotal)
if discount_name:
    subtotal -= discount_amount

# Calculate the shipping fee
shipping_fee = (total_quantity - 1) // units_per_package * shipping_fee_per_package

# Calculate the total amount
total = subtotal + shipping_fee

# Display the details
print("------ Order Details ------")
for name in products:
    total_amount = calculate_product_total(name, quantities[name], is_gift_wrapped[name])
    print(f"{name}: Quantity - {quantities[name]}, Total - ${total_amount}")
print(f"\nSubtotal: ${subtotal}")
if discount_name:
    print(f"Discount Applied: {discount_name}, Amount: ${discount_amount}")
print(f"Shipping Fee: ${shipping_fee}")
print(f"Total: ${total}")
