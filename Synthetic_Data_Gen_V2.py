import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import math
from faker import Faker
import warnings
from joblib import load

warnings.filterwarnings("ignore")

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker("en_US")
Faker.seed(42)
today = datetime.today().date()

class ShrinkSenseSystem:

    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.TAX_RATE = 0.30  # Corporate tax rate

        # Load ML models and scalers
        self.markdown_model = load('optimal_markdown_model.pkl')
        self.markdown_scaler = load('markdown_scaler.pkl')
        with open('model_feature_columns.txt', 'r') as f:
            self.markdown_feature_columns = [line.strip() for line in f.readlines()]

        self.upliftment_model = load('upliftment_model.pkl')
        self.upliftment_scaler = load('scaler.pkl')

        # Product Categories and their configurations
        self.categories_config = {
            "Fresh Produce": {
                "sub_categories": ["Fruits", "Vegetables", "Leafy Greens"],
                "uom": "lbs",
                "storage": "Cold Storage",
                "shelf_life_days": (3, 14),
                "price_range": (1, 5),
                "sell_through_target": (15, 30),
            },
            "Dry Goods": {
                "sub_categories": ["Canned Foods", "Pasta", "Cereals"],
                "uom": "oz",
                "storage": "Dry Storage",
                "shelf_life_days": (90, 180),
                "price_range": (2, 10),
                "sell_through_target": (8, 20),
            },
            "General Merchandise": {
                "sub_categories": ["Cleaning", "Paper Products", "Personal Care"],
                "uom": "units",
                "storage": "Ambient",
                "shelf_life_days": (365, 1095),
                "price_range": (5, 25),
                "sell_through_target": (5, 10)
            }
        }
        self.brands = ["Great Value", "Kirkland", "365 Everyday", "Market Pantry", "Signature Select"]
        self.suppliers = ["Sysco", "US Foods", "C&S Wholesale", "McLane", "Kroger Supply"]

        # Store States
        self.states = {
            "CA": "West", "TX": "South", "NY": "North", "FL": "South", "IL": "East",
            "WA": "West", "GA": "South", "NC": "East", "AZ": "West", "PA": "North"
        }

    def generate_complete_system(self, num_inventory_records=1000, num_return_records=100):
        """Generate complete Shrink Sense system with all components"""
        print("Generating Complete Shrink Sense Inventory Management System...")
        print("=" * 70)

        # Generate all system components
        product_data = self.generate_product_master()
        stores_data = self.generate_stores()
        ngo_data = self.generate_ngo_partners(stores_data)
        liquidation_data = self.generate_liquidation_partners(stores_data)
        inventory_data = self.generate_inventory_data(num_inventory_records, stores_data, product_data)
        returns_data = self.generate_returns_data_v2(num_return_records, inventory_data)

        # Integrate ML models
        inventory_data = self.integrate_ml_models(inventory_data)

        # Create Excel file with all sheets
        filename = self.create_excel_system(
            product_data, inventory_data,
            stores_data, ngo_data,
            liquidation_data, returns_data
        )

        return filename

    def generate_product_master(self):
        print(" Generating Product Master Data...")
        product_master = []
        for i in range(1000):
            cat = random.choice(list(self.categories_config.keys()))
            sub_cat = random.choice(self.categories_config[cat]['sub_categories'])
            brand = random.choice(self.brands)
            product = {
                "SKU_ID": f"SKU_{i+1:04d}",
                "Product_Name": fake.word().title() + " " + sub_cat,
                "Brand": brand,
                "Brand Code": brand[:3].upper() + str(random.randint(100,999)),
                "Category": cat,
                "Sub_Category": sub_cat,
                "Pack_Size": f"{random.randint(1,5)}{self.categories_config[cat]['uom']}",
                "Unit_Of_Measure": self.categories_config[cat]['uom'],
                "Storage_Type": self.categories_config[cat]['storage'],
                "Supplier_Name": random.choice(self.suppliers),
            }
            product_master.append(product)
        return pd.DataFrame(product_master)



    def generate_received_date(self, category, shelf_life_days):
        # Controlled distribution for shelf_life_used_pct
        rand = random.random()
    
        if category == "Dry Goods":
            if rand < 0.55:  # ~55% Fresh
                shelf_life_used_pct = random.uniform(10, 55)
            elif rand < 0.75:  # ~20% Expiry Approaching
                shelf_life_used_pct = random.uniform(60, 85)
            elif rand < 0.9:   # ~15% Critical
                shelf_life_used_pct = random.uniform(90, 99)
            else:              # ~10% Expired
                shelf_life_used_pct = random.uniform(101, 130)
    
        elif category == "General Merchandise":
            if rand < 0.6:   # ~60% Fresh
                shelf_life_used_pct = random.uniform(5, 55)
            elif rand < 0.8:  # ~20% Approaching
                shelf_life_used_pct = random.uniform(60, 85)
            elif rand < 0.95:  # ~15% Critical
                shelf_life_used_pct = random.uniform(90, 100)
            else:              # ~5% Expired
                shelf_life_used_pct = random.uniform(101, 120)
    
        else:
            # For Fresh Produce keep earlier high perishability logic
            if rand < 0.4:
                shelf_life_used_pct = random.uniform(10, 55)
            elif rand < 0.7:
                shelf_life_used_pct = random.uniform(60, 85)
            elif rand < 0.9:
                shelf_life_used_pct = random.uniform(90, 100)
            else:
                shelf_life_used_pct = random.uniform(101, 130)
    
        # Calculate received_date from shelf_life_used_pct
        used_days = int((shelf_life_days * shelf_life_used_pct) / 100)
        received_date = datetime.now().date() - timedelta(days=used_days)
        expiry_date = received_date + timedelta(days=shelf_life_days)
        days_to_expiry = (expiry_date - datetime.now().date()).days
    
        return received_date, expiry_date, shelf_life_used_pct, days_to_expiry

    
    def classify_inventory(self, shelf_life_used_pct, category):
        if shelf_life_used_pct < 60:
            return "Fresh", 0
        elif 60 <= shelf_life_used_pct < 90:
            return "Expiry Approaching", 0
        elif 90 <= shelf_life_used_pct <= 100:
            return "Critical - Expiring Soon", 0
        else:
            if category == "Fresh Produce":
                expired_units = random.randint(175, 200)
            elif category == "General Merchandise":
                expired_units = random.randint(150, 175)
            elif category == "Dry Goods":
                expired_units = random.randint(100, 150)
            else:
                expired_units = random.randint(75, 100)
            return "Already Expired", expired_units


    
    def generate_stores(self):
        """Generate comprehensive store data"""
        print(" Generating Store Network Data...")
        store_data = []
        for i in range(30):
            state = random.choice(list(self.states.keys()))
            store = {
                "Store_ID": f"STR_{i+1:03d}",
                "Store_Name": fake.company(),
                "Store_City": fake.city(),
                "Store_State": state,
                "Store_Region": random.randint(1, 8), #self.states[state],
                "Latitude": round(fake.latitude(), 6),
                "Longitude": round(fake.longitude(), 6),
                "Capacity_Limit": random.randint(1000, 5000),
                "Current_Capacity": random.randint(200, 4500),
                "Performance_Score": round(random.uniform(0.8, 1.2), 2)
            }
            store_data.append(store)
        return pd.DataFrame(store_data)

    def generate_ngo_partners(self, stores_data):
        """Generate NGO partnership data for donations"""
        print(" Generating NGO Partnership Network...")
        ngo_types = ["Fresh Produce","Dry Goods","General Merchandise"]
        ngo_data = []

        for i in range(30):
            ngo = {
                "NGO_ID": f"NGO_{i+1:03d}",
                "NGO_Name": fake.company() + " Foundation",
                "NGO_Type": random.choice(ngo_types),
                "NGO_LAT": round(fake.latitude(), 6),
                "NGO_LONG": round(fake.longitude(), 6),
                "Acceptance_Criteria_Met": random.choice([True, False]),
                "Acceptance_Capacity_Fresh_Produce": random.randint(100, 1000),
                "Acceptance_Capacity_Dry_Goods": random.randint(200, 2000),
                "Acceptance_Capacity_GM": random.randint(100, 1000),
                "Past_Donation_Success_Rate": round(random.uniform(60, 100), 2)
            }
            ngo_data.append(ngo)
        return pd.DataFrame(ngo_data)

    def generate_liquidation_partners(self, stores_data):
        """Generate liquidation partner data"""
        print(" Generating Liquidation Partners...")
        liquidator_types = ["Fresh Produce","Dry Goods","General Merchandise"]
        liquidator_data = []

        for i in range(30):
            liquidator = {
                "Liquidator_ID": f"LQD_{i+1:03d}",
                "Liquidator_Name": fake.company() + " Liquidators",
                "Liquidator_Type": random.choice(liquidator_types),
                "Latitude": round(fake.latitude(), 6),
                "Longitude": round(fake.longitude(), 6),
                "Offer Price (% of MRP)": round(random.uniform(20, 70), 2),
                "Pickup SLA (in days)": random.randint(1, 5),
                "Quantity_Handling_Capacity_Fresh_Produce": random.randint(100, 1000),
                "Quantity_Handling_Capacity_Dry_Goods": random.randint(500, 3000),
                "Quantity_Handling_Capacity_GM": random.randint(200, 1500),
                "Past Fulfillment Success Rate (%)": round(random.uniform(50, 100), 2)
            }
            liquidator_data.append(liquidator)
        return pd.DataFrame(liquidator_data)

    def get_price(self, category):
        low, high = self.categories_config[category]['price_range']
        return round(random.uniform(low, high), 2)

    def generate_inventory_data(self, num_records, stores_data, product_data):
        """Generate comprehensive inventory data"""
        print(f" Generating {num_records:,} Inventory Records...")
        inventory_records = []
        for i in range(num_records):
            product = product_data.sample(1).iloc[0]
            store = stores_data.sample(1).iloc[0]
            category = str(product['Category'])
            shelf_life_range = self.categories_config[category]['shelf_life_days']
            shelf_life_days = random.randint(*shelf_life_range)

            received_date, expiry_date, shelf_life_used_pct, days_to_expiry  = self.generate_received_date(category, shelf_life_days)
            
            # expiry_date = received_date + timedelta(days=shelf_life_days)
            inventory_age = (datetime.now().date() - received_date).days
            # days_to_expiry = (expiry_date - datetime.now().date()).days
            days_to_expiry_pct = round(days_to_expiry / shelf_life_days, 2)
            # shelf_life_used_pct = ((shelf_life_days - days_to_expiry)/shelf_life_days)*100
            shelf_life_used_pct = round(shelf_life_used_pct, 2)

            status, expired_units = self.classify_inventory(shelf_life_used_pct, category)

            target_sell_range = self.categories_config[category]['sell_through_target']
            target_sell_rate = random.randint(*target_sell_range)

            days_active = (today - received_date).days
            units_sold = int(target_sell_rate * days_active)

            sell_through_pct = random.uniform(0.35, 0.6)
            total_expected = int(units_sold / sell_through_pct)
            on_hand = max(1, total_expected - units_sold)

            if category == "Fresh Produce":
                damaged_units = random.randint(0, 1)
                dump_units = random.randint(0, 25)
            elif category == "Dry Goods":
                damaged_units = random.randint(0, 35)
                dump_units = random.randint(0, 1)
            elif category == "General Merchandise":
                damaged_units = random.randint(0, 10)
                dump_units = random.randint(0, 1)
            else:
                damaged_units = random.randint(0, 20)
                dump_units = random.randint(0, 15)

                
            # damaged_units = random.randint(0, 20)
            # dump_units = random.randint(0, 15)

            actual_qty = units_sold + on_hand + damaged_units + dump_units + expired_units
            discrepancy = random.randint(0, 20)
            system_qty = actual_qty + discrepancy

            sell_through_rate = round(units_sold / days_active, 2) if days_active > 0 else 0
            sell_through_percent = round(units_sold / actual_qty, 2) if actual_qty > 0 else 0

            projected_sales_remaining = sell_through_rate * days_to_expiry

            sell_price = self.get_price(product["Category"])
            cost_price = round(sell_price * 0.7, 2)
            original_revenue = on_hand*sell_price
            cogs = on_hand*cost_price
            original_gm = ((sell_price-cost_price)/sell_price)*100

            store_channel = ["Wholesale", "E-commerce", "Franchise", "Direct", "Retail"]
            
            inventory_records.append({
                "SKU_ID": product['SKU_ID'],
                "Product_Name": product['Product_Name'],
                "Category": category,
                "Sub_Category": product["Sub_Category"],
                "Store_ID": store['Store_ID'],
                "Store_Channel": random.choice(store_channel),
                "Supplier_Name": fake.company(),
                "Received_Date": received_date,
                "Expiry_Date": expiry_date,
                "System_Quantity_Received": system_qty,
                "Actual_Quantity_Received": actual_qty,
                "Difference_(System - Actual)": system_qty - actual_qty,
                "Inventory_At_Markdown": on_hand, #On-hand_inventory
                "Number_Damaged_Units": damaged_units,
                "Number_Dump_Units": dump_units,
                'Number_Expired_Units': expired_units,
                "Inventory_On_Hand": on_hand,
                "Unit_Sold": units_sold,
                "Days_Active": days_active,
                "Shelf_Life": shelf_life_days,
                "Sell_Through_Rate_Per_Day": sell_through_rate,
                "Sell_Through_Rate": sell_through_percent,
                "Shelf_Life_Remaining": days_to_expiry,
                "Shelf_Life_Used_Pct" : shelf_life_used_pct,
                "Projected_Sales_Remaining": projected_sales_remaining,
                "Inventory_Status": status,
                "Cost_Price_CP": cost_price,
                "Selling_Price_SP": sell_price,
                "Original_Revenue(no return/remediation)": original_revenue,
                "COGS": cogs,
                "Original_Gross_Margin": original_gm,
                "Inventory_Age_Days": inventory_age,
                "Is_Returnable": 0 if product["Category"] == "Fresh Produce" else 1,
                "Is_Perishable": 1 if product["Category"] == "Fresh Produce" else 0,
                "Previous_Markdown_Count": random.randint(0, 5),
                "SKU_Demand_Score": round(random.uniform(0.5, 1.5), 2),
                "Store_Performance_Score": store['Performance_Score'],
                "Region": store["Store_Region"],
                "Competing_SKUs_Count": random.randint(0, 10),
                "Historical markdown %": round(random.uniform(0, 0.5), 2),
                "Days of Supply": round(on_hand / sell_through_rate, 2) if sell_through_rate > 0 else 0
            })
            if (i + 1) % 100 == 0:
                print(f" âœ“ Generated {i+1:,} inventory records...")
        return pd.DataFrame(inventory_records)

    def integrate_ml_models(self, inventory_df):
        print(" Integrating ML Models for Markdown and Upliftment Prediction...")

        # Markdown model prediction
        markdown_df = pd.get_dummies(inventory_df.copy(), columns=["SKU_ID", "Store_ID", "Region"], drop_first=True)
        missing_md_cols = [col for col in self.markdown_feature_columns if col not in markdown_df.columns]
        missing_md_df = pd.DataFrame(0, index=markdown_df.index, columns=missing_md_cols)
        markdown_df = pd.concat([markdown_df, missing_md_df], axis=1)
        markdown_df = markdown_df[self.markdown_feature_columns].copy()

        markdown_numeric_cols = ["Inventory_At_Markdown", "Previous_Markdown_Count", "SKU_Demand_Score",
                                 "Store_Performance_Score", "Sell_Through_Rate", "Competing_SKUs_Count",
                                 "Shelf_Life_Remaining_Pct"]
        markdown_df[markdown_numeric_cols] = self.markdown_scaler.transform(markdown_df[markdown_numeric_cols])
        inventory_df["Predicted_Required_Markdown_Pct"] = self.markdown_model.predict(markdown_df)

        # Upliftment model prediction
        inventory_df["Required_Markdown_Pct"] = inventory_df["Predicted_Required_Markdown_Pct"]
        inventory_df["Sales_Before_Markdown"] = inventory_df["Sell_Through_Rate_Per_Day"] * inventory_df['Shelf_Life_Remaining']
        inventory_df["Sales_After_Markdown"] = inventory_df["Inventory_At_Markdown"]

        uplift_df = pd.get_dummies(inventory_df.copy(), columns=["SKU_ID", "Store_ID", "Region"])
        uplift_df = uplift_df.reindex(columns=self.upliftment_model.feature_names_in_, fill_value=0)

        uplift_numeric_cols = ["Inventory_At_Markdown", "Previous_Markdown_Count", "SKU_Demand_Score",
                               "Store_Performance_Score", "Sell_Through_Rate", "Competing_SKUs_Count",
                               "Shelf_Life_Remaining_Pct", "Required_Markdown_Pct",
                               "Sales_Before_Markdown", "Sales_After_Markdown"]
        uplift_df[uplift_numeric_cols] = self.upliftment_scaler.transform(uplift_df[uplift_numeric_cols])
        inventory_df["Predicted_Upliftment_Factor"] = self.upliftment_model.predict(uplift_df)

        # Drop temporary columns used for prediction "Shelf_Life_Remaining_Pct"
        inventory_df.drop(columns=[
            'Predicted_Required_Markdown_Pct', 'Sales_Before_Markdown',
            'Sales_After_Markdown', "Store_Performance_Score", "Competing_SKUs_Count",
            "Previous_Markdown_Count", "SKU_Demand_Score", "Inventory_At_Markdown"
        ], inplace=True, errors='ignore')

        return inventory_df

    def generate_returns_data(self, num_records, stores_data, inventory_data):
        """Generate customer returns data"""
        print(f"â†©ï¸ Generating {num_records:,} Returns Records...")
        return_reasons = ["Unopened", "Packaging_Damaged", "Expired", "Defective", "Opened_Consumed"]
        categories = ["Dry Goods", "General Merchandise"]
        returns_records = []
        for i in range(num_records):
            store = stores_data.iloc[random.randint(0, len(stores_data) - 1)]
            inventory = inventory_data.iloc[random.randint(0, len(inventory_data) - 1)]
            category = random.choice(categories)
            reason = random.choice(return_reasons)
            quantity = random.randint(1, 10)
            days_left = 0
            if reason == "Expired":
                days_left = 0
            elif reason == "Defective" or reason == "Opened_Consumed":
                days_left = 0
            else:
                if category == "Dry Goods":
                    days_left = random.randint(1, 365)
                elif category == "General Merchandise":
                    days_left = random.randint(1, 730)
            return_date = fake.date_between(start_date="-60d", end_date="-1d")
            returns_records.append({
                "return_id": f"RET_{i+1:04d}",
                "store_id": inventory["Store_ID"],
                "sku_id": inventory["SKU_ID"],
                "category": category, #inventory_data["Category"],
                "product_name": inventory["Product_Name"],
                "return_reason": reason,
                "quantity_returned": quantity,
                "Cost_Price_CP": inventory["Cost_Price_CP"],
                "Selling_Price_SP": inventory["Selling_Price_SP"],
                "shelf_life": inventory["Shelf_Life"],
                "days_left": days_left,
                "return_date": return_date,
                "customer_id": fake.uuid4(),
                "original_purchase_date": fake.date_between(start_date="-1y", end_date="-61d"),
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            })
            if (i + 1) % 10 == 0:
                print(f" âœ“ Generated {i+1:,} returns records...")
        return pd.DataFrame(returns_records)


    def generate_returns_data_v2(self, num_records, inventory_data):
        """Generate customer returns data"""
        print(f"↩️ Generating {num_records:,} Returns Records...")
    
        # Return reasons based on category
        return_reason_map = {
            "Dry Goods": ["Expired", "Packaging Damaged", "Unopened", "Opened/Partially Used", "Spoiled"],
            "General Merchandise": ["Defective", "Packaging Damaged", "Unopened", "Wrong Item", "Ordered by Mistake"]
        }
    
        # Item condition mapping based on reason
        item_condition_map = {
            "Expired": "Expired", 
            "Packaging Damaged": "Damaged Packaging", 
            "Unopened": "New/Sealed", 
            "Opened/Partially Used": "Opened", 
            "Spoiled": "Contaminated", 
            "Defective": "Faulty", 
            "Wrong Item": "Good Condition", 
            "Ordered by Mistake": "Unused"
        }
    
        returns_records = []
    
        for i in range(num_records):
            # store = stores_data.sample(1).iloc[0]
            inventory = inventory_data.sample(1).iloc[0]
    
            category = random.choice(["Dry Goods", "General Merchandise"])
            return_reason = random.choice(return_reason_map[category])
            item_condition = item_condition_map.get(return_reason, "Unknown")
    
            quantity = random.randint(1, 10)
    
            # Determine days_left
            if return_reason in ["Expired", "Spoiled", "Defective", "Opened/Partially Used"]:
                days_left = 0
            else:
                if category == "Dry Goods":
                    days_left = random.randint(1, 365)
                else:  # General Merchandise
                    days_left = random.randint(1, 730)
    
            return_date = fake.date_between(start_date="-60d", end_date="-1d")
    
            returns_records.append({
                "return_id": f"RET_{i+1:04d}",
                "store_id": inventory["Store_ID"],
                "sku_id": inventory["SKU_ID"],
                "category": category,
                "product_name": inventory["Product_Name"],
                "return_reason": return_reason,
                "item_condition": item_condition,
                "quantity_returned": quantity,
                "Cost_Price_CP": inventory["Cost_Price_CP"],
                "Selling_Price_SP": inventory["Selling_Price_SP"],
                "shelf_life": inventory["Shelf_Life"],
                "days_left": days_left,
                "return_date": return_date,
                "customer_id": fake.uuid4(),
                "original_purchase_date": fake.date_between(start_date="-1y", end_date="-61d"),
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            })
    
            if (i + 1) % 10 == 0:
                print(f" ✔ Generated {i+1:,} returns records...")

        return pd.DataFrame(returns_records)

    
    def create_excel_system(self, product_data, inventory_data, stores_data, ngo_data, liquidation_data, returns_data):
        print(" Creating Comprehensive Excel System...")

        filename = f"ShrinkSense_Complete_System_{self.timestamp}.xlsx"

        with pd.ExcelWriter('Output_Files/' + filename, engine="openpyxl") as writer:
            product_data.to_excel(writer, sheet_name="product_master", index=False)
            inventory_data.to_excel(writer, sheet_name="inventory", index=False)
            stores_data.to_excel(writer, sheet_name="stores", index=False)
            ngo_data.to_excel(writer, sheet_name="ngo_partners", index=False)
            liquidation_data.to_excel(writer, sheet_name="liquidation_partners", index=False)
            returns_data.to_excel(writer, sheet_name="returns", index=False)

        return filename

# Main execution function
def main():
    print("SHRINK SENSE INVENTORY MANAGEMENT SYSTEM")
    print("=" * 60)
    print("Complete Inventory Optimization & Recovery Recommendation Engine")
    print("=" * 60)

    try:
        print("\nðŸ“Š Dataset Size Options:")
        print("1. Small Dataset (500 inventory, 50 returns) - Quick demo")
        print("2. Medium Dataset (1,500 inventory, 150 returns) - Standard analysis")
        print("3. Large Dataset (3,000 inventory, 300 returns) - Comprehensive analysis")
        print("4. Custom size")

        choice = input("\nSelect option (1-4): ").strip()

        num_inventory_records = 0
        num_return_records = 0

        if choice == "1":
            num_inventory_records = 500
            num_return_records = 50
        elif choice == "2":
            num_inventory_records = 1500
            num_return_records = 150
        elif choice == "3":
            num_inventory_records = 3000
            num_return_records = 300
        elif choice == "4":
            try:
                num_inventory_records = int(input("Enter number of inventory records: "))
                num_return_records = int(input("Enter number of returns records: "))
                if num_inventory_records <= 0 or num_return_records <= 0:
                    raise ValueError("Numbers must be positive")
            except ValueError:
                print("Invalid input. Using default size of 1,500 inventory and 150 returns records.")
                num_inventory_records = 1500
                num_return_records = 150
        else:
            print("Invalid choice. Using default size of 1,500 inventory and 150 returns records.")
            num_inventory_records = 1500
            num_return_records = 150

        print(f"\nðŸ”„ Initializing Shrink Sense System with {num_inventory_records:,} inventory records and {num_return_records:,} returns records...")
        system = ShrinkSenseSystem()

        filename = system.generate_complete_system(num_inventory_records, num_return_records)

        print(f"ðŸ“ File Created: {filename}")

    except KeyboardInterrupt:
        print("\n\n Operation cancelled by user.")
    except Exception as e:
        print(f"\n Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print("Please check your inputs and try again.")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()

    
