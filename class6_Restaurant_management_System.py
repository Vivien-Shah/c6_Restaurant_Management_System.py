import tkinter as tk
from tkinter import ttk, messagebox


class RestaurantOrderManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Order Management")
        self.root.geometry("800x600")

        self.menu_items = {
            "FRIES MEAL": 2,
            "LUNCH MEAL": 2,
            "BURGER MEAL": 3,
            "PIZZA MEAL": 4,
            "CHEESE BURGER": 2.5,
            "DRINKS": 1
        }

        self.exchange_rate = 82

        # Dictionaries
        self.menu_labels = {}
        self.menu_quantities = {}

        # Main Frame
        frame = ttk.Frame(root, padding=20)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Title
        ttk.Label(
            frame,
            text="Restaurant Order Management",
            font=("Arial", 20, "bold")
        ).grid(row=0, columnspan=3, pady=10)

        # Menu Items
        for i, (item, price) in enumerate(self.menu_items.items(), start=1):
            label = ttk.Label(
                frame,
                text=f"{item} ($ {price})",
                font=("Arial", 12)
            )
            label.grid(row=i, column=0, padx=10, pady=5)

            self.menu_labels[item] = label

            quantity_entry = ttk.Entry(frame, width=5)
            quantity_entry.grid(row=i, column=1, padx=10, pady=5)

            self.menu_quantities[item] = quantity_entry

        # Currency Selection
        self.currency_var = tk.StringVar(value="INR")

        ttk.Label(
            frame,
            text="Currency:",
            font=("Arial", 12)
        ).grid(row=len(self.menu_items) + 1, column=0, padx=10, pady=5)

        currency_dropdown = ttk.Combobox(
            frame,
            textvariable=self.currency_var,
            values=["USD", "INR"],
            state="readonly",
            width=10
        )

        currency_dropdown.grid(
            row=len(self.menu_items) + 1,
            column=1,
            padx=10,
            pady=5
        )

        currency_dropdown.current(0)

        # Update prices when currency changes
        self.currency_var.trace_add("write", self.update_menu_prices)

        # Order Button
        order_button = ttk.Button(
            frame,
            text="Place Order",
            command=self.place_order
        )

        order_button.grid(
            row=len(self.menu_items) + 2,
            columnspan=3,
            pady=10
        )

    # Update Menu Prices
    def update_menu_prices(self, *args):
        currency = self.currency_var.get()

        symbol = "₹" if currency == "INR" else "$"
        rate = self.exchange_rate if currency == "INR" else 1

        for item, label in self.menu_labels.items():
            price = self.menu_items[item] * rate
            label.config(text=f"{item} ({symbol}{price})")

    # Place Order
    def place_order(self):
        total_cost = 0
        order_summary = "Order Summary:\n\n"

        currency = self.currency_var.get()

        symbol = "₹" if currency == "INR" else "$"
        rate = self.exchange_rate if currency == "INR" else 1

        for item, entry in self.menu_quantities.items():
            quantity = entry.get()

            if quantity.isdigit():
                quantity = int(quantity)

                if quantity > 0:
                    price = self.menu_items[item] * rate
                    cost = quantity * price

                    total_cost += cost

                    order_summary += (
                        f"{item}: {quantity} x "
                        f"{symbol}{price} = {symbol}{cost}\n"
                    )

        if total_cost > 0:
            order_summary += f"\nTotal Cost: {symbol}{total_cost}"
            messagebox.showinfo("Order Placed", order_summary)

        else:
            messagebox.showerror(
                "Error",
                "Please order at least one item."
            )


# Run Application
root = tk.Tk()
app = RestaurantOrderManagement(root)
root.mainloop()