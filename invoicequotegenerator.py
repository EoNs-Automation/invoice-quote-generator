from datetime import datetime
import os

def create_document():
    print("\n=== New Document ===")
    
    # Document type
    doc_type_input = input("Create Invoice or Quote? (i/q): ").strip().lower()
    if doc_type_input == "quit":
        return False
    doc_type = "INVOICE" if doc_type_input == "i" else "QUOTE"
    folder_name = "invoices" if doc_type == "INVOICE" else "quotes"

    # Basic info
    business_name = input("Your business name: ").strip()
    if business_name.lower() == "quit":
        return False

    client_name = input("Client name: ").strip()
    if client_name.lower() == "quit":
        return False

    doc_number = input(f"{doc_type.title()} number (e.g. 001): ").strip()
    if doc_number.lower() == "quit":
        return False
    if not doc_number:
        doc_number = "001"

    today = datetime.now().strftime("%Y-%m-%d")

    # Items
    items = []
    print("\nAdd items (leave description blank when finished):")

    while True:
        description = input("\nItem description: ").strip()
        if description.lower() == "quit":
            return False
        if not description:
            break

        try:
            quantity = float(input("Quantity: ").strip())
            price = float(input("Price per item: $").strip())
        except ValueError:
            print("Please enter valid numbers.")
            continue

        items.append({
            "description": description,
            "quantity": quantity,
            "price": price,
            "total": quantity * price
        })

    if not items:
        print("No items added.")
        return True

    # Tax
    tax_input = input("\nTax rate (%) or press Enter for 0: ").strip()
    tax_rate = float(tax_input) if tax_input else 0

    # Notes
    notes = input("Additional notes (optional): ").strip()

    # Calculations
    subtotal = sum(item["total"] for item in items)
    tax_amount = subtotal * (tax_rate / 100)
    grand_total = subtotal + tax_amount

    # Build the document
    lines = []
    lines.append("=" * 55)
    lines.append(f"{business_name.upper()}")
    lines.append("=" * 55)
    lines.append(f"{doc_type} #: {doc_number}")
    lines.append(f"Date: {today}")
    lines.append(f"Client: {client_name}")
    lines.append("-" * 55)
    lines.append(f"{'Item':<28} {'Qty':>6} {'Price':>8} {'Total':>9}")
    lines.append("-" * 55)

    for item in items:
        lines.append(
            f"{item['description'][:27]:<28} {item['quantity']:>6.1f} {item['price']:>8.2f} {item['total']:>9.2f}"
        )

    lines.append("-" * 55)
    lines.append(f"{'Subtotal:':<44} ${subtotal:>8.2f}")
    if tax_rate > 0:
        lines.append(f"{'Tax (' + str(tax_rate) + '%):':<44} ${tax_amount:>8.2f}")
    lines.append(f"{'TOTAL:':<44} ${grand_total:>8.2f}")
    lines.append("=" * 55)

    if notes:
        lines.append(f"\nNotes: {notes}")

    document = "\n".join(lines)
    print("\n" + document)

    # Save to file
    save = input("\nSave this to a text file? (y/n): ").strip().lower()
    if save == "y":
        script_folder = os.path.dirname(os.path.abspath(__file__))
        output_folder = os.path.join(script_folder, folder_name)
        os.makedirs(output_folder, exist_ok=True)

        filename = f"{doc_type.lower()}-{doc_number}-{client_name.replace(' ', '_')}.txt"
        filepath = os.path.join(output_folder, filename)

        with open(filepath, "w") as f:
            f.write(document)

        print(f"\nSaved as: {filepath}")

    return True


def main():
    print("=== Invoice / Quote Generator ===")
    print("Type 'quit' at any time to exit.")

    while True:
        keep_going = create_document()
        if not keep_going:
            print("Goodbye!")
            break

        again = input("\nCreate another one? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()