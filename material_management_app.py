
import json
import datetime
from typing import Dict, List, Optional
import os

class MaterialManager:
    def __init__(self, data_file: str = "materials_data.json"):
        self.data_file = data_file
        self.materials = self.load_data()

    def load_data(self) -> Dict:
        """Load materials data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return self.initialize_default_data()
        else:
            return self.initialize_default_data()

    def save_data(self):
        """Save materials data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.materials, f, indent=2, default=str)

    def initialize_default_data(self) -> Dict:
        """Initialize with default material categories"""
        return {
            "general_materials": {
                "cement": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "bags", "minimum_stock": 10},
                "M sand fine": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "cubic_meters", "minimum_stock": 5},
                "engine oil": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "liters", "minimum_stock": 20},
                "Spider Kits": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "pieces", "minimum_stock": 5},
                "Rope 14mm": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "meters", "minimum_stock": 100},
                "Roller 6 Inch": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "pieces", "minimum_stock": 10},
                "Roller 4 Inch": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "pieces", "minimum_stock": 10},
                "Roller 9 Inch int": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "pieces", "minimum_stock": 5},
                "Roller 9 Inch ext": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "pieces", "minimum_stock": 5},
                "Putty Blade 4 inch": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "pieces", "minimum_stock": 15},
                "Putty Blade 8 inch": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "pieces", "minimum_stock": 10},
                "Sanding Paper Grit220": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "sheets", "minimum_stock": 50},
                "Masking Tape 1 inch": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "rolls", "minimum_stock": 20},
                "Brush 2 inch": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "pieces", "minimum_stock": 10},
                "Brush 4 inch": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "pieces", "minimum_stock": 10},
                "Brush 6 inch": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "pieces", "minimum_stock": 5},
                "Goggles": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "pieces", "minimum_stock": 10},
                "Nose Mask": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "pieces", "minimum_stock": 50},
                "safety gloves": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "pairs", "minimum_stock": 20},
                "Helmet": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "pieces", "minimum_stock": 10}
            },
            "paint_materials": {
                "Zydex White Primer 20L": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "liters", "unit_size": 20, "minimum_stock": 5},
                "Zydex ZycoSil+ 20L": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "liters", "unit_size": 20, "minimum_stock": 3},
                "Zydex ZycoPrime+": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "liters", "unit_size": 20, "minimum_stock": 3},
                "AP SMARTCARE CRACKSEAL": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "kg", "unit_size": 5, "minimum_stock": 10},
                "AP Smooth Putty": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "kg", "unit_size": 40, "minimum_stock": 5},
                "AP Acrylic Putty": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "kg", "unit_size": 20, "minimum_stock": 5},
                "Asian Apex Suprema": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "liters", "unit_size": 20, "minimum_stock": 3},
                "Asian Tractor Emulsion": {"in_stock": 0, "consumed": 0, "transferred": 0, "unit": "liters", "unit_size": 20, "minimum_stock": 5}
            },
            "transactions": [],
            "site_info": {
                "site_name": "L&T Site",
                "last_updated": str(datetime.datetime.now())
            }
        }

    def add_material_receipt(self, category: str, material_name: str, quantity: int, 
                           source: str = "Office", remarks: str = ""):
        """Add received materials to inventory"""
        if category not in self.materials:
            print(f"Category '{category}' not found!")
            return False

        if material_name not in self.materials[category]:
            # Add new material if it doesn't exist
            unit = input(f"Enter unit for {material_name}: ")
            min_stock = int(input(f"Enter minimum stock level for {material_name}: "))
            self.materials[category][material_name] = {
                "in_stock": 0, "consumed": 0, "transferred": 0, 
                "unit": unit, "minimum_stock": min_stock
            }

        self.materials[category][material_name]["in_stock"] += quantity

        # Record transaction
        transaction = {
            "date": str(datetime.datetime.now()),
            "type": "receipt",
            "category": category,
            "material": material_name,
            "quantity": quantity,
            "source": source,
            "remarks": remarks
        }
        self.materials["transactions"].append(transaction)
        self.save_data()
        print(f"✓ Added {quantity} units of {material_name} to inventory")
        return True

    def consume_material(self, category: str, material_name: str, quantity: int, 
                        purpose: str = "", remarks: str = ""):
        """Record material consumption"""
        if category not in self.materials or material_name not in self.materials[category]:
            print(f"Material '{material_name}' not found in category '{category}'!")
            return False

        current_stock = self.materials[category][material_name]["in_stock"]
        if current_stock < quantity:
            print(f"❌ Insufficient stock! Available: {current_stock}, Requested: {quantity}")
            return False

        self.materials[category][material_name]["in_stock"] -= quantity
        self.materials[category][material_name]["consumed"] += quantity

        # Record transaction
        transaction = {
            "date": str(datetime.datetime.now()),
            "type": "consumption",
            "category": category,
            "material": material_name,
            "quantity": quantity,
            "purpose": purpose,
            "remarks": remarks
        }
        self.materials["transactions"].append(transaction)
        self.save_data()
        print(f"✓ Consumed {quantity} units of {material_name}")
        return True

    def transfer_material(self, category: str, material_name: str, quantity: int, 
                         destination: str = "", remarks: str = ""):
        """Transfer materials to another site/office"""
        if category not in self.materials or material_name not in self.materials[category]:
            print(f"Material '{material_name}' not found in category '{category}'!")
            return False

        current_stock = self.materials[category][material_name]["in_stock"]
        if current_stock < quantity:
            print(f"❌ Insufficient stock! Available: {current_stock}, Requested: {quantity}")
            return False

        self.materials[category][material_name]["in_stock"] -= quantity
        self.materials[category][material_name]["transferred"] += quantity

        # Record transaction
        transaction = {
            "date": str(datetime.datetime.now()),
            "type": "transfer",
            "category": category,
            "material": material_name,
            "quantity": quantity,
            "destination": destination,
            "remarks": remarks
        }
        self.materials["transactions"].append(transaction)
        self.save_data()
        print(f"✓ Transferred {quantity} units of {material_name} to {destination}")
        return True

    def check_low_stock(self):
        """Check and display materials with low stock"""
        print("\n" + "="*50)
        print("📊 LOW STOCK ALERT")
        print("="*50)

        low_stock_items = []
        for category in ["general_materials", "paint_materials"]:
            if category in self.materials:
                for material, data in self.materials[category].items():
                    if data["in_stock"] <= data["minimum_stock"]:
                        low_stock_items.append({
                            "category": category,
                            "material": material,
                            "current_stock": data["in_stock"],
                            "minimum_stock": data["minimum_stock"],
                            "unit": data["unit"]
                        })

        if low_stock_items:
            for item in low_stock_items:
                print(f"⚠️  {item['material']}: {item['current_stock']} {item['unit']} (Min: {item['minimum_stock']})")
        else:
            print("✅ All materials are above minimum stock levels")

    def display_inventory(self, category: str = "all"):
        """Display current inventory status"""
        print("\n" + "="*70)
        print(f"📦 INVENTORY STATUS - {self.materials['site_info']['site_name']}")
        print("="*70)

        categories_to_show = [category] if category != "all" else ["general_materials", "paint_materials"]

        for cat in categories_to_show:
            if cat in self.materials:
                print(f"\n🔧 {cat.replace('_', ' ').upper()}")
                print("-" * 70)
                print(f"{'Material Name':<30} {'In Stock':<10} {'Consumed':<10} {'Transferred':<12} {'Unit':<8}")
                print("-" * 70)

                for material, data in self.materials[cat].items():
                    stock_indicator = "⚠️ " if data["in_stock"] <= data["minimum_stock"] else ""
                    print(f"{stock_indicator}{material:<30} {data['in_stock']:<10} {data['consumed']:<10} {data['transferred']:<12} {data['unit']:<8}")

    def view_recent_transactions(self, limit: int = 10):
        """Display recent transactions"""
        print("\n" + "="*80)
        print("📋 RECENT TRANSACTIONS")
        print("="*80)

        recent_transactions = self.materials["transactions"][-limit:]

        for transaction in reversed(recent_transactions):
            date = datetime.datetime.fromisoformat(transaction["date"]).strftime("%Y-%m-%d %H:%M")
            print(f"📅 {date} | {transaction['type'].upper():<12} | {transaction['material']:<25} | {transaction['quantity']} units")
            if transaction.get("remarks"):
                print(f"   💬 {transaction['remarks']}")

    def generate_material_report(self):
        """Generate comprehensive material usage report"""
        print("\n" + "="*80)
        print(f"📊 MATERIAL USAGE REPORT - {self.materials['site_info']['site_name']}")
        print("="*80)

        for category in ["general_materials", "paint_materials"]:
            if category in self.materials:
                print(f"\n🏷️  {category.replace('_', ' ').upper()}")
                print("-" * 80)

                total_items = len(self.materials[category])
                total_stock = sum(item["in_stock"] for item in self.materials[category].values())
                total_consumed = sum(item["consumed"] for item in self.materials[category].values())
                total_transferred = sum(item["transferred"] for item in self.materials[category].values())

                print(f"Total Material Types: {total_items}")
                print(f"Total Stock Value: {total_stock} units")
                print(f"Total Consumed: {total_consumed} units")
                print(f"Total Transferred: {total_transferred} units")

                # Find most consumed materials
                consumed_materials = [(name, data["consumed"]) for name, data in self.materials[category].items() if data["consumed"] > 0]
                if consumed_materials:
                    consumed_materials.sort(key=lambda x: x[1], reverse=True)
                    print(f"\n🔥 Top 3 Most Consumed Materials:")
                    for i, (material, consumed) in enumerate(consumed_materials[:3], 1):
                        unit = self.materials[category][material]["unit"]
                        print(f"   {i}. {material}: {consumed} {unit}")

def main_menu():
    """Main application menu"""
    manager = MaterialManager()

    while True:
        print("\n" + "="*60)
        print("🏗️  MATERIAL MANAGEMENT SYSTEM - L&T SITE")
        print("="*60)
        print("1. 📦 View Inventory")
        print("2. ➕ Add Material Receipt")
        print("3. ➖ Record Material Consumption")
        print("4. 🔄 Transfer Material")
        print("5. ⚠️  Check Low Stock")
        print("6. 📋 View Recent Transactions")
        print("7. 📊 Generate Material Report")
        print("8. 🆕 Add New Material")
        print("9. 💾 Backup Data")
        print("0. 🚪 Exit")
        print("="*60)

        choice = input("👆 Select an option (0-9): ").strip()

        if choice == "1":
            print("\n📦 INVENTORY OPTIONS:")
            print("1. General Materials")
            print("2. Paint Materials") 
            print("3. All Materials")
            inv_choice = input("Select category (1-3): ").strip()

            if inv_choice == "1":
                manager.display_inventory("general_materials")
            elif inv_choice == "2":
                manager.display_inventory("paint_materials")
            else:
                manager.display_inventory("all")

        elif choice == "2":
            print("\n➕ ADD MATERIAL RECEIPT")
            print("Categories: 1. General Materials  2. Paint Materials")
            cat_choice = input("Select category (1-2): ").strip()
            category = "general_materials" if cat_choice == "1" else "paint_materials"

            material_name = input("Material name: ").strip()
            try:
                quantity = int(input("Quantity received: "))
                source = input("Source (Office/Dealer/Site): ").strip() or "Office"
                remarks = input("Remarks (optional): ").strip()
                manager.add_material_receipt(category, material_name, quantity, source, remarks)
            except ValueError:
                print("❌ Please enter a valid quantity!")

        elif choice == "3":
            print("\n➖ RECORD MATERIAL CONSUMPTION")
            print("Categories: 1. General Materials  2. Paint Materials")
            cat_choice = input("Select category (1-2): ").strip()
            category = "general_materials" if cat_choice == "1" else "paint_materials"

            material_name = input("Material name: ").strip()
            try:
                quantity = int(input("Quantity consumed: "))
                purpose = input("Purpose/Work area: ").strip()
                remarks = input("Remarks (optional): ").strip()
                manager.consume_material(category, material_name, quantity, purpose, remarks)
            except ValueError:
                print("❌ Please enter a valid quantity!")

        elif choice == "4":
            print("\n🔄 TRANSFER MATERIAL")
            print("Categories: 1. General Materials  2. Paint Materials")
            cat_choice = input("Select category (1-2): ").strip()
            category = "general_materials" if cat_choice == "1" else "paint_materials"

            material_name = input("Material name: ").strip()
            try:
                quantity = int(input("Quantity to transfer: "))
                destination = input("Destination (Office/Site name): ").strip()
                remarks = input("Remarks (optional): ").strip()
                manager.transfer_material(category, material_name, quantity, destination, remarks)
            except ValueError:
                print("❌ Please enter a valid quantity!")

        elif choice == "5":
            manager.check_low_stock()

        elif choice == "6":
            try:
                limit = int(input("Number of recent transactions to show (default 10): ") or "10")
                manager.view_recent_transactions(limit)
            except ValueError:
                manager.view_recent_transactions()

        elif choice == "7":
            manager.generate_material_report()

        elif choice == "8":
            print("\n🆕 ADD NEW MATERIAL")
            print("Categories: 1. General Materials  2. Paint Materials")
            cat_choice = input("Select category (1-2): ").strip()
            category = "general_materials" if cat_choice == "1" else "paint_materials"

            material_name = input("New material name: ").strip()
            unit = input("Unit (pieces/liters/kg/etc.): ").strip()
            try:
                min_stock = int(input("Minimum stock level: "))
                manager.materials[category][material_name] = {
                    "in_stock": 0, "consumed": 0, "transferred": 0,
                    "unit": unit, "minimum_stock": min_stock
                }
                manager.save_data()
                print(f"✅ Added new material: {material_name}")
            except ValueError:
                print("❌ Please enter a valid minimum stock level!")

        elif choice == "9":
            backup_file = f"materials_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            try:
                with open(backup_file, 'w') as f:
                    json.dump(manager.materials, f, indent=2, default=str)
                print(f"✅ Data backed up to {backup_file}")
            except Exception as e:
                print(f"❌ Backup failed: {e}")

        elif choice == "0":
            print("\n👋 Thank you for using Material Management System!")
            print("💾 All data has been saved automatically.")
            break

        else:
            print("❌ Invalid choice! Please select 0-9.")

        input("\n🔄 Press Enter to continue...")

if __name__ == "__main__":
    main_menu()
