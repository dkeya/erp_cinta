import streamlit as st
import pandas as pd
import random
from datetime import datetime
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Utility Functions
def generate_barcode():
    return f"CBW-{random.randint(100000, 999999)}"

def display_dataframe(df, title):
    st.subheader(title)
    st.dataframe(df)

def save_to_csv(df, filename):
    df.to_csv(filename, index=False)

def load_from_csv(filename):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return pd.DataFrame()

def scan_barcode(image):
    """Scan barcode using OpenCV."""
    # Convert PIL image to OpenCV format
    image_cv = np.array(image)
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)
    
    # Decode barcode
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(image_cv)
    return data if data else None

# Function to get product of the week
def get_product_of_the_week():
    # Load sales data
    sales_file = "data/sales.csv"
    df = load_from_csv(sales_file)
    
    if df.empty:
        return None, None
    
    # Find the best-selling product
    best_product = df["Product Name"].value_counts().idxmax()
    
    # Load inventory data to get the product image
    inventory_file = "data/inventory.csv"
    inventory_df = load_from_csv(inventory_file)
    
    if inventory_df.empty:
        return best_product, None
    
    # Get the product image (assuming the image filename is stored in the inventory data)
    product_row = inventory_df[inventory_df["Product Name"] == best_product]
    if not product_row.empty:
        product_image = product_row.iloc[0]["Image"]  # Assuming "Image" column contains the filename
        return best_product, product_image
    else:
        return best_product, None

# Function to get seller of the week
def get_seller_of_the_week():
    # Load sales data
    sales_file = "data/sales.csv"
    df = load_from_csv(sales_file)
    
    if df.empty:
        return None, None
    
    # Find the best-performing seller
    best_seller = df["Customer Name"].value_counts().idxmax()
    
    # Load seller data to get the seller's photo (assuming a "sellers.csv" file exists)
    sellers_file = "data/sellers.csv"
    sellers_df = load_from_csv(sellers_file)
    
    if sellers_df.empty:
        return best_seller, None
    
    # Get the seller's photo (assuming "Photo" column contains the filename)
    seller_row = sellers_df[sellers_df["Customer Name"] == best_seller]
    if not seller_row.empty:
        seller_photo = seller_row.iloc[0]["Photo"]
        return best_seller, seller_photo
    else:
        return best_seller, None

# Main Function
def main():
    st.set_page_config(page_title="🌐Verse ERP", layout="wide")
    
    # Sidebar Navigation
    st.sidebar.title("🌐Verse ERP")
    
    menu = {
        "Home": home,
        "Production Management": production_management,
        "Inventory Management": inventory_management,
        "Point of Sale (POS)": pos_module,
        "Sales & Marketing": sales_marketing,
        "Personnel Management": personnel_management,
        "Financial Management": financial_management,
        "Analytics & Reporting": analytics_reporting,
    }
    
    choice = st.sidebar.radio("Select Module", list(menu.keys()), key="main_menu")
    
    # Initialize submenu variable
    submenu = None
    
    # Display submenus for the selected module
    if choice in ["Production Management", "Inventory Management", "Point of Sale (POS)", "Sales & Marketing", "Personnel Management", "Financial Management", "Analytics & Reporting"]:
        if choice == "Production Management":
            submenu = st.sidebar.radio(
                "Select Submenu",
                ["Production Tracking", "Workflow Management", "Product Formulations"],
                key="production_submenu"
            )
        elif choice == "Inventory Management":
            submenu = st.sidebar.radio(
                "Select Submenu",
                ["Stock Levels", "Reorder Alerts", "Barcode Management"],
                key="inventory_submenu"
            )
        elif choice == "Point of Sale (POS)":
            submenu = st.sidebar.radio(
                "Select Submenu",
                ["Process Sale", "View Sales History"],
                key="pos_submenu"
            )
        elif choice == "Sales & Marketing":
            submenu = st.sidebar.radio(
                "Select Submenu",
                ["Sales Performance", "Customer Insights", "Campaign Management"],
                key="sales_submenu"
            )
        elif choice == "Personnel Management":
            submenu = st.sidebar.radio(
                "Select Submenu",
                ["Employee Records", "Payroll Processing", "Attendance Tracking"],
                key="personnel_submenu"
            )
        elif choice == "Financial Management":
            submenu = st.sidebar.radio(
                "Select Submenu",
                ["Revenue Tracking", "Expense Tracking", "Financial Reports"],
                key="financial_submenu"
            )
        elif choice == "Analytics & Reporting":
            submenu = st.sidebar.radio(
                "Select Submenu",
                ["Sales Analytics", "Inventory Analytics", "Financial Analytics"],
                key="analytics_submenu"
            )
    
    # Add a separator (dotted lines)
    st.sidebar.markdown("---")
    
    # Product of the Week Section
    st.sidebar.subheader("Product of the Week 🏆")
    product_name, product_image = get_product_of_the_week()
    
    if product_name:
        st.sidebar.write(f"**{product_name}** is this week's top product!")
        if product_image:
            # Display the product image with a playful animation (zoom-in effect)
            st.sidebar.image(
                product_image,
                caption=product_name,
                use_column_width=True,
                output_format="auto",
                width=200,
            )
        else:
            st.sidebar.write("No image available for this product.")
    else:
        st.sidebar.write("No sales data available to determine the product of the week.")
    
    # Add another separator
    st.sidebar.markdown("---")
    
    # Seller of the Week Section
    st.sidebar.subheader("Seller of the Week 🌟")
    seller_name, seller_photo = get_seller_of_the_week()
    
    if seller_name:
        st.sidebar.write(f"**{seller_name}** is this week's top seller!")
        if seller_photo:
            # Display the seller's photo with a moving effect (fade-in)
            st.sidebar.image(
                seller_photo,
                caption=f"Congratulations, {seller_name}! 🎉",
                use_column_width=True,
                output_format="auto",
                width=200,
            )
        else:
            st.sidebar.write("No photo available for this seller.")
    else:
        st.sidebar.write("No sales data available to determine the seller of the week.")
    
    # Call the selected function
    if submenu:
        menu[choice](submenu)  # Pass the submenu selection to the module function
    else:
        menu[choice]()  # Call the module function without submenu

# Home Page
def home():
    st.image("logo.png", width=150)
    st.title("Welcome to the Verse!")
    st.write("Your all-in-one solution for managing production, inventory, sales, and more.")
    
    # Display key metrics
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", "Kes 1M")
    with col2:
        st.metric("Inventory Levels", "1,200 Items")
    with col3:
        st.metric("Production Batches", "15 Batches")
    
    # Quick links
    st.subheader("Quick Links")
    st.write("Navigate to specific modules using the sidebar or the links below:")
    st.write("- [Production Management](#production-management)")
    st.write("- [Inventory Management](#inventory-management)")
    st.write("- [Point of Sale (POS)](#point-of-sale-pos)")
    st.write("- [Sales & Marketing](#sales-marketing)")
    st.write("- [Analytics & Reporting](#analytics-reporting)")

# Production Management Module
def production_management(submenu=None):
    st.title("Production Management")
    
    if submenu == "Production Tracking":
        st.subheader("Production Tracking")
        # Load or initialize production data
        production_file = "data/production.csv"
        df = load_from_csv(production_file)
        
        if df.empty:
            df = pd.DataFrame({
                "Batch ID": [],
                "Product Name": [],
                "Raw Materials Used": [],
                "Quantity Produced": [],
                "Production Date": [],
                "Status": []
            })
        
        # Display production data
        display_dataframe(df, "Production Batches")
        
        # Add new production batch
        st.subheader("Add New Production Batch")
        with st.form("production_form"):
            product_name = st.text_input("Product Name", placeholder="Enter product name")
            raw_materials = st.text_area("Raw Materials Used", placeholder="List raw materials")
            quantity = st.number_input("Quantity Produced", min_value=1)
            production_date = st.date_input("Production Date")
            status = st.selectbox("Status", ["Scheduled", "In Progress", "Completed"])
            submit = st.form_submit_button("Add Batch")
            
            if submit:
                if not product_name or not raw_materials:
                    st.error("Please fill in all fields.")
                else:
                    new_batch = {
                        "Batch ID": f"B{len(df) + 1:03d}",
                        "Product Name": product_name,
                        "Raw Materials Used": raw_materials,
                        "Quantity Produced": quantity,
                        "Production Date": production_date.strftime("%Y-%m-%d"),
                        "Status": status
                    }
                    df = df.append(new_batch, ignore_index=True)
                    save_to_csv(df, production_file)
                    st.success(f"Production batch for {product_name} added successfully!")
    
    elif submenu == "Workflow Management":
        st.subheader("Workflow Management")
        st.write("Manage and track production workflows.")
        # Add workflow management functionality here
    
    elif submenu == "Product Formulations":
        st.subheader("Product Formulations")
        st.write("Store and manage product formulations.")
        # Add product formulations functionality here

# Inventory Management Module
def inventory_management(submenu=None):
    st.title("Inventory Management")
    
    if submenu == "Stock Levels":
        st.subheader("Stock Levels")
        # Load or initialize inventory data
        inventory_file = "data/inventory.csv"
        df = load_from_csv(inventory_file)
        
        if df.empty:
            df = pd.DataFrame({
                "Product ID": [],
                "Product Name": [],
                "Stock Quantity": [],
                "Reorder Level": [],
                "Last Restocked": [],
                "Expiration Date": [],
                "Supplier": [],
                "Barcode": []
            })
        
        # Display inventory data
        display_dataframe(df, "Inventory Levels")
        
        # Add new inventory item
        st.subheader("Add New Inventory Item")
        with st.form("inventory_form"):
            product_name = st.text_input("Product Name", placeholder="Enter product name")
            stock_quantity = st.number_input("Stock Quantity", min_value=1)
            reorder_level = st.number_input("Reorder Level", min_value=1)
            last_restocked = st.date_input("Last Restocked Date")
            expiration_date = st.date_input("Expiration Date")
            supplier = st.text_input("Supplier Name", placeholder="Enter supplier name")
            barcode = generate_barcode()
            submit = st.form_submit_button("Add to Inventory")
            
            if submit:
                if not product_name or not supplier:
                    st.error("Please fill in all fields.")
                elif reorder_level >= stock_quantity:
                    st.error("Reorder Level must be less than Stock Quantity.")
                else:
                    new_item = {
                        "Product ID": f"P{len(df) + 1:03d}",
                        "Product Name": product_name,
                        "Stock Quantity": stock_quantity,
                        "Reorder Level": reorder_level,
                        "Last Restocked": last_restocked.strftime("%Y-%m-%d"),
                        "Expiration Date": expiration_date.strftime("%Y-%m-%d"),
                        "Supplier": supplier,
                        "Barcode": barcode
                    }
                    df = df.append(new_item, ignore_index=True)
                    save_to_csv(df, inventory_file)
                    st.success(f"{product_name} added to inventory successfully! Generated Barcode: {barcode}")
    
    elif submenu == "Reorder Alerts":
        st.subheader("Reorder Alerts")
        st.write("View and manage reorder alerts.")
        # Add reorder alerts functionality here
    
    elif submenu == "Barcode Management":
        st.subheader("Barcode Management")
        st.write("Scan and manage barcodes.")
        
        # Barcode scanning
        uploaded_file = st.file_uploader("Upload Barcode Image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Barcode", use_column_width=True)
            barcode = scan_barcode(image)
            if barcode:
                st.success(f"Scanned Barcode: {barcode}")
            else:
                st.error("No barcode detected.")

# Point of Sale (POS) Module
def pos_module(submenu=None):
    st.title("Point of Sale (POS)")
    st.write("Process transactions and manage sales.")
    
    if submenu == "Process Sale":
        st.subheader("Process Sale")
        # Load or initialize sales data
        sales_file = "data/sales.csv"
        df = load_from_csv(sales_file)
        
        if df.empty:
            df = pd.DataFrame({
                "Sale ID": [],
                "Product ID": [],
                "Product Name": [],
                "Quantity Sold": [],
                "Total Price": [],
                "Sale Date": [],
                "Customer Name": [],
                "Payment Method": []
            })
        
        # Process a new sale
        with st.form("pos_form"):
            product_name = st.text_input("Product Name", placeholder="Enter product name")
            quantity_sold = st.number_input("Quantity Sold", min_value=1)
            total_price = st.number_input("Total Price", min_value=0.0)
            sale_date = st.date_input("Sale Date")
            customer_name = st.text_input("Customer Name", placeholder="Enter customer name")
            payment_method = st.selectbox("Payment Method", ["Cash", "Card", "Mobile Money"])
            submit = st.form_submit_button("Process Sale")
            
            if submit:
                if not product_name or not customer_name:
                    st.error("Please fill in all fields.")
                else:
                    new_sale = {
                        "Sale ID": f"S{len(df) + 1:03d}",
                        "Product ID": f"P{len(df) + 1:03d}",  # Placeholder, link to actual product ID
                        "Product Name": product_name,
                        "Quantity Sold": quantity_sold,
                        "Total Price": total_price,
                        "Sale Date": sale_date.strftime("%Y-%m-%d"),
                        "Customer Name": customer_name,
                        "Payment Method": payment_method
                    }
                    df = df.append(new_sale, ignore_index=True)
                    save_to_csv(df, sales_file)
                    st.success(f"Sale for {product_name} processed successfully!")
    
    elif submenu == "View Sales History":
        st.subheader("Sales History")
        # Load sales data
        sales_file = "data/sales.csv"
        df = load_from_csv(sales_file)
        
        if df.empty:
            st.warning("No sales data available.")
        else:
            display_dataframe(df, "Sales Transactions")

# Sales & Marketing Module
def sales_marketing(submenu=None):
    st.title("Sales & Marketing")
    
    if submenu == "Sales Performance":
        st.subheader("Sales Performance")
        # Load sales data
        sales_file = "data/sales.csv"
        df = load_from_csv(sales_file)
        
        if df.empty:
            st.warning("No sales data available.")
        else:
            # Display sales trends
            st.subheader("Sales Trends")
            st.line_chart(df.set_index("Sale Date")["Total Price"])
    
    elif submenu == "Customer Insights":
        st.subheader("Customer Insights")
        # Load sales data
        sales_file = "data/sales.csv"
        df = load_from_csv(sales_file)
        
        if df.empty:
            st.warning("No sales data available.")
        else:
            # Customer insights
            customer_data = df["Customer Name"].value_counts().reset_index()
            customer_data.columns = ["Customer Name", "Number of Purchases"]
            st.dataframe(customer_data)
    
    elif submenu == "Campaign Management":
        st.subheader("Campaign Management")
        st.write("Manage marketing campaigns.")
        # Add campaign management functionality here

# Personnel Management Module
def personnel_management(submenu=None):
    st.title("Personnel Management")
    
    if submenu == "Employee Records":
        st.subheader("Employee Records")
        # Load or initialize employee data
        employees_file = "data/employees.csv"
        df = load_from_csv(employees_file)
        
        if df.empty:
            df = pd.DataFrame({
                "Employee ID": [],
                "Employee Name": [],
                "Role": [],
                "Salary": [],
                "Join Date": [],
                "Attendance": []
            })
        
        # Display employee data
        display_dataframe(df, "Employee Records")
        
        # Add new employee
        st.subheader("Add New Employee")
        with st.form("employee_form"):
            employee_name = st.text_input("Employee Name", placeholder="Enter employee name")
            role = st.selectbox("Role", ["Production", "Sales", "HR", "Finance"])
            salary = st.number_input("Salary", min_value=0)
            join_date = st.date_input("Join Date")
            attendance = st.number_input("Attendance (%)", min_value=0, max_value=100)
            submit = st.form_submit_button("Add Employee")
            
            if submit:
                if not employee_name:
                    st.error("Please fill in all fields.")
                else:
                    new_employee = {
                        "Employee ID": f"E{len(df) + 1:03d}",
                        "Employee Name": employee_name,
                        "Role": role,
                        "Salary": salary,
                        "Join Date": join_date.strftime("%Y-%m-%d"),
                        "Attendance": attendance
                    }
                    df = df.append(new_employee, ignore_index=True)
                    save_to_csv(df, employees_file)
                    st.success(f"Employee {employee_name} added successfully!")
    
    elif submenu == "Payroll Processing":
        st.subheader("Payroll Processing")
        st.write("Process employee payroll.")
        # Add payroll processing functionality here
    
    elif submenu == "Attendance Tracking":
        st.subheader("Attendance Tracking")
        st.write("Track employee attendance.")
        # Add attendance tracking functionality here

# Financial Management Module
def financial_management(submenu=None):
    st.title("Financial Management")
    
    if submenu == "Revenue Tracking":
        st.subheader("Revenue Tracking")
        # Load financial data
        financial_file = "data/financial.csv"
        df = load_from_csv(financial_file)
        
        if df.empty:
            df = pd.DataFrame({
                "Transaction ID": [],
                "Description": [],
                "Amount": [],
                "Type": [],
                "Date": []
            })
        
        # Display revenue data
        revenue_df = df[df["Type"] == "Revenue"]
        display_dataframe(revenue_df, "Revenue Transactions")
    
    elif submenu == "Expense Tracking":
        st.subheader("Expense Tracking")
        # Load financial data
        financial_file = "data/financial.csv"
        df = load_from_csv(financial_file)
        
        if df.empty:
            df = pd.DataFrame({
                "Transaction ID": [],
                "Description": [],
                "Amount": [],
                "Type": [],
                "Date": []
            })
        
        # Display expense data
        expense_df = df[df["Type"] == "Expense"]
        display_dataframe(expense_df, "Expense Transactions")
    
    elif submenu == "Financial Reports":
        st.subheader("Financial Reports")
        st.write("Generate financial reports.")
        # Add financial reporting functionality here

# Analytics & Reporting Module
def analytics_reporting(submenu=None):
    st.title("Analytics & Reporting")
    
    if submenu == "Sales Analytics":
        st.subheader("Sales Analytics")
        # Load sales data
        sales_file = "data/sales.csv"
        df = load_from_csv(sales_file)
        
        if df.empty:
            st.warning("No sales data available.")
        else:
            # Sales trends
            st.subheader("Sales Trends")
            st.line_chart(df.set_index("Sale Date")["Total Price"])
            
            # Top products
            st.subheader("Top Products")
            top_products = df["Product Name"].value_counts().reset_index()
            top_products.columns = ["Product Name", "Units Sold"]
            st.bar_chart(top_products.set_index("Product Name"))
            
            # Sales Predictions
            st.subheader("Sales Predictions")
            st.write("Predict future sales using linear regression.")
            
            # Prepare data for prediction
            df["Sale Date"] = pd.to_datetime(df["Sale Date"])
            df["Days"] = (df["Sale Date"] - df["Sale Date"].min()).dt.days
            
            X = df[["Days"]]
            y = df["Total Price"]
            
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train linear regression model
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            # Predict future sales
            future_days = st.number_input("Enter number of days to predict:", min_value=1, value=30)
            future_X = np.array(range(df["Days"].max() + 1, df["Days"].max() + 1 + future_days)).reshape(-1, 1)
            future_y = model.predict(future_X)
            
            # Display predictions
            st.write(f"Predicted sales for the next {future_days} days:")
            st.line_chart(pd.DataFrame({"Days": future_X.flatten(), "Predicted Sales": future_y}).set_index("Days"))
    
    elif submenu == "Inventory Analytics":
        st.subheader("Inventory Analytics")
        # Load inventory data
        inventory_file = "data/inventory.csv"
        df = load_from_csv(inventory_file)
        
        if df.empty:
            st.warning("No inventory data available.")
        else:
            # Stock levels
            st.subheader("Stock Levels")
            st.bar_chart(df.set_index("Product Name")["Stock Quantity"])
    
    elif submenu == "Financial Analytics":
        st.subheader("Financial Analytics")
        # Load financial data
        financial_file = "data/financial.csv"
        df = load_from_csv(financial_file)
        
        if df.empty:
            st.warning("No financial data available.")
        else:
            # Revenue vs Expenses
            st.subheader("Revenue vs Expenses")
            revenue = df[df["Type"] == "Revenue"]["Amount"].sum()
            expenses = df[df["Type"] == "Expense"]["Amount"].sum()
            st.write(f"Total Revenue: Kes{revenue:,.2f}")
            st.write(f"Total Expenses: Kes{expenses:,.2f}")
            st.write(f"Net Profit: Kes{revenue - expenses:,.2f}")

if __name__ == "__main__":
    main()