import streamlit as st
import pandas as pd
import random
from datetime import datetime
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image

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

# Main Function
def main():
    st.set_page_config(page_title="Cinta Beauty ERP", layout="wide")
    
    # Sidebar Navigation
    st.sidebar.title("Cinta Beauty ERP")
    
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
    
    choice = st.sidebar.radio("Select Module", list(menu.keys()))
    
    # Call the selected function
    menu[choice]()

# Home Page
def home():
    st.title("Welcome to Cinta Beauty ERP")
    st.write("Your all-in-one solution for managing production, inventory, sales, and more.")
    
    # Display key metrics
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", "$10,000")
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
def production_management():
    st.title("Production Management")
    
    # Submenus
    submenu = st.sidebar.radio(
        "Select Submenu",
        ["Production Tracking", "Workflow Management", "Product Formulations"]
    )
    
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
def inventory_management():
    st.title("Inventory Management")
    
    # Submenus
    submenu = st.sidebar.radio(
        "Select Submenu",
        ["Stock Levels", "Reorder Alerts", "Barcode Management"]
    )
    
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
def pos_module():
    st.title("Point of Sale (POS)")
    st.write("Process transactions and manage sales.")
    
    # Submenus
    submenu = st.sidebar.radio(
        "Select Submenu",
        ["Process Sale", "View Sales History"]
    )
    
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
def sales_marketing():
    st.title("Sales & Marketing")
    
    # Submenus
    submenu = st.sidebar.radio(
        "Select Submenu",
        ["Sales Performance", "Customer Insights", "Campaign Management"]
    )
    
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
def personnel_management():
    st.title("Personnel Management")
    
    # Submenus
    submenu = st.sidebar.radio(
        "Select Submenu",
        ["Employee Records", "Payroll Processing", "Attendance Tracking"]
    )
    
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
def financial_management():
    st.title("Financial Management")
    
    # Submenus
    submenu = st.sidebar.radio(
        "Select Submenu",
        ["Revenue Tracking", "Expense Tracking", "Financial Reports"]
    )
    
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
def analytics_reporting():
    st.title("Analytics & Reporting")
    
    # Submenus
    submenu = st.sidebar.radio(
        "Select Submenu",
        ["Sales Analytics", "Inventory Analytics", "Financial Analytics"]
    )
    
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
            st.write(f"Total Revenue: ${revenue:,.2f}")
            st.write(f"Total Expenses: ${expenses:,.2f}")
            st.write(f"Net Profit: ${revenue - expenses:,.2f}")

if __name__ == "__main__":
    main()