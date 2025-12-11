import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

# -----------------------------------------------------------
# GLOBAL UTILITY FUNCTIONS
# -----------------------------------------------------------

@st.cache_data
def load_distribution_data(excel_name, csv_name, project_columns):
    """
    Loads distribution data from the file, parsing by month.
    This function is cached to prevent reloading the file on every interaction.
    """
    df_distribution = None
    monthly_distribution_data = {}
    
    # Attempt to read the file silently
    try:
        # Priority to CSV if it's explicitly named/available, otherwise use Excel
        if os.path.exists(csv_name):
            df_distribution = pd.read_csv(csv_name, header=1)
        elif os.path.exists(excel_name):
            df_distribution = pd.read_excel(excel_name, header=1)
    except Exception:
        return {} # Return empty data on failure

    if df_distribution is not None and not df_distribution.empty:
        try:
            total_col_name = None
            if 'Month' in df_distribution.columns:
                month_col_index = df_distribution.columns.get_loc('Month')
                if month_col_index + 1 < len(df_distribution.columns):
                    # Assume the Total column is immediately after the Month column
                    total_col_name = df_distribution.columns[month_col_index + 1]

            if 'Month' in df_distribution.columns and total_col_name:
                
                for index, row in df_distribution.iterrows():
                    month_date = row['Month']
                    total_value = row.get(total_col_name)

                    # Helper function to standardize month string (defined outside this cache)
                    month_str = format_month_for_match(month_date)
                    
                    if month_str and pd.notna(total_value):
                        total_value = float(total_value)
                        
                        project_splits = {}
                        for proj_name in project_columns:
                            proj_amount = 0.0
                            
                            # Find the column in the DataFrame that matches the project name
                            found_col = next((col for col in df_distribution.columns if str(col).strip() == proj_name.strip()), None)
                                
                            if found_col:
                                val = row.get(found_col)
                                proj_amount = float(val) if pd.notna(val) else 0.0

                            project_splits[proj_name] = proj_amount
                        
                        monthly_distribution_data[month_str] = {
                            'total': total_value,
                            'splits': project_splits
                        }
                        
        except Exception:
            return {}
            
    return monthly_distribution_data

def format_month_for_match(date_val):
    """Converts various date formats (from Excel) into the Streamlit dropdown format (e.g., 'June 2025')."""
    if pd.notna(date_val):
        try:
            # Attempt to parse it as a date and format to "Month YYYY"
            return pd.to_datetime(date_val).strftime("%B %Y")
        except:
            # If it's not a date, return the string representation
            return str(date_val).strip()
    return None

# -----------------------------------------------------------
# HARDCODED DATA AND CONFIGURATION
# -----------------------------------------------------------

# --- Hardcoded Project Names (used for lookup in the file) ---
PROJECT_COLUMNS = [
    "HLL Malappuram", 
    "Power Grid Corporation of India Limited - Yelahanka, Bangalore",
    "Cochin Shipyard Limited - Andaman", 
    "IOCL - Panipat", 
    "HLL Cotton Hill, Trivandrum", 
    "Swasthya-An innovative behaviour change programme for Aneamia in women of reproductive age",
    "Counselling support for transgender individuals-pre and post surgery and non surgical pathways in gender transition",
    "Inclusive community mental health initiative in Wayanad district",
    "My City", 
    "Exploring the correlation and Diagnostic potential of Menstrual Blood",
    "HLL Maharashtra"
]

# --- FULL RANGE OF MONTHS FOR DROPDOWN (JUN 2025 to MAR 2026) ---
MONTHS = [
    "June 2025", "July 2025", "August 2025", "September 2025", 
    "October 2025", "November 2025", "December 2025", 
    "January 2026", "February 2026", "March 2026"
]

# --- Hardcoded Lists for Page 2 (Core Team) ---
core_team_names = [
    "Gayatri Vijay L", "Vishnu", "Anakha Joy", "Jeena Raju", "Sujitha S", 
    "Sudheesh", "Sukumaran", "Soumya S K", "Vignesh Kumar P B", "Ashitha Vins V M", 
    "Savitha Y", "Silpa", "Preethima", "Sakshi Baliram Savare", "Rakhee", 
    "Jayalekshmi J", "Sushila", "Syamili", "Saidali Safar", "Titu S Jayan", 
    "Dhanya B L", "Heksy Sebastian", "Manjusha V", "Mariyathul Hibthiya", "Ruksana Beegum Pakkichippura", 
    "Greeshma Kuriakose", "Ashwini Bhausaheb Ranjane", "Swathy Krishna S", "Anjali Prakash K", "Ajila Mohan N J", 
    "Elizabeth Packim", "Arathy A S Kumar", "Juhaina C K", "Navya M", "Alka Wadhwa", 
    "Anjaly V", "Anjali A S", "Rakhi Mohan", "Abhirami N A", "Sarika P S Krishna", 
    "Bhavya R J", "Jesna C", "Rasna K S", "Lenita G Lawrence", "Devika Prasad", 
    "Jayalekshmi M J", "K Anakha Soman", "Jithin Dominic", "Divya Vinod", "Sherin Jacob", 
    "Arjuna V Nath", "Rejitha Ravi", "Devika HS", "Jijo Pramod"
]

core_team_designations = [
    "Project Associate",
    "Project Associate (Public Health)",
    "Project Associate (Community Development)",
    "Field Assistant",
    "Accounts Assistant",
    "Administrative Assistant (Projects)",
    "Project Facilitator",
    "Office Assistant",
    "Backend Support",
]

# --- Hardcoded Lists for Page 4 (HMA CSR Admin Expenses) ---
CSR_VENDORS = [
    "Manjith Travels", 
    "Alchemy IBS", 
    "Oval Blue Technologies", 
    "Volks Electronics", 
    "Asianet", 
    "Stationary SERVICES"
]

CSR_EXPENSE_TYPES = [
    "Contract Vehicle", 
    "Website", 
    "Photocopier SDP", 
    "Desktop rental", 
    "Internet Services", 
    "Stationary"
]

CSR_PAYMENT_FREQUENCY = [
    "Monthly", 
    "Quarterly", 
    "Half Yearly"
]

# --- Hardcoded Lists for Page 3 (HR Expenses) ---
HR_VENDOR_OPTIONS = [
    "Dr Anandam", "BSNL", "KSEB", "KWA", "Subramania Industries", "Imprest",
    "Geejey Solutions", "VRS infosystems", "M/sArmtech Computer Services", "Nu aire",
    "Miscellaneous", "Microsoft 365", "Asterisk", "Indian Postal Department",
    "Pradeep Kumar Cost Accountant", "Vismaya Services", "Naveen Security Services",
    "Other (Enter Manually)"
]

HR_SERVICE_OPTIONS = [
    "House Rent", "Land Line", "Electricity Bill", "Water Bill", "DG AMC",
    "Monthly Imprest", "Epabx AMC", "Tally Software Renewal", "CAMC computer hardware",
    "AC AMC", "Repair & Maintenance", "Software", "Photocopier (Admin & DVP)",
    "Speed post", "Financial Consultant", "Accounts Assistance", "HK salary",
    "My city salary", "Security salary",
    "Other (Enter Manually)"
]


# -----------------------------------------------------------
# PAGE STYLE 
# -----------------------------------------------------------
st.set_page_config(page_title="HMA Project Expenses", layout="centered")

st.markdown("""
    <style>
        /* Pastel Background */
        [data-testid="stAppViewContainer"] {
            background: 
                radial-gradient(circle at 10% 20%, rgba(255, 210, 250, 0.35) 0%, transparent 60%),
                radial-gradient(circle at 80% 10%, rgba(210, 230, 255, 0.35) 0%, transparent 60%),
                radial-gradient(circle at 20% 80%, rgba(240, 255, 220, 0.35) 0%, transparent 60%),
                linear-gradient(135deg, #FFF7FD 0%, #FFFFFF 100%);
            font-family: 'Montserrat', sans-serif;
        }

        .sidebar-title {
            font-weight: 900;
            font-size: 20px;
        }

        .sidebar-option {
            font-weight: 800 !important;
            font-size: 18px !important;
        }
        
        /* Custom CSS for the Distribution Table (Light Blue, Bold) */
        .distribution-table table {
            background-color: #D7F7FF !important; /* Light blue color */
            border-collapse: collapse;
            width: 100%;
        }
        .distribution-table th, .distribution-table td {
            font-weight: bold !important;
            color: black !important;
            border: 1px solid black !important;
            padding: 8px !important;
        }
        
        /* Highlight the LSGB row specifically in Page 2 */
        .distribution-table tr:last-child {
            background-color: #B2EBF2 !important; /* Slightly darker blue for LSGB row */
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# SIDEBAR — BOLD MENU
# -----------------------------------------------------------
with st.sidebar:
    st.markdown("<div class='sidebar-title'>Menu</div>", unsafe_allow_html=True)
    menu = st.radio(
        "",
        ["HMA PROJECT EXPENSES CALCULATOR", 
         "HMA CORE TEAM",
         "HMA CSR ADMIN EXPENSES", 
         "HR EXPENSES",
         "HMA HR REVENUE"],
        format_func=lambda x: f"**{x}**"
    )

# -----------------------------------------------------------
# PAGE 1 — HMA PROJECT EXPENSES CALCULATOR 
# -----------------------------------------------------------
if menu == "HMA PROJECT EXPENSES CALCULATOR":

    st.markdown("<h2>📘 HMA PROJECT EXPENSES CALCULATOR</h2>", unsafe_allow_html=True)

    project_name = st.text_input("Project Name")
    project_type = st.text_input("Project Type")
    project_value = st.number_input("Project Value (₹)", min_value=0.0, format="%.2f")

    # CALCULATE button
    if st.button("CALCULATE"):

        if project_value <= 0:
            st.error("Please enter a valid Project Value.")
        else:
            core_team_salary = project_value * 0.05
            csr_admin_exp = project_value * 0.05
            hr_expenses = project_value * 0.05
            total_15 = project_value * 0.15
            direct_exp = project_value * 0.85

            st.markdown("---")
            st.subheader("📊 Calculation Results")

            # TABLE DATA
            df_calc = pd.DataFrame({
                "Description": [
                    "HMA Core Team Salary (5%)",
                    "HMA CSR Admin Expenses (5%)",
                    "HR Expenses (5%)",
                    "Total (15%)",
                    "Project Direct Expenses (85%)"
                ],
                "Amount (₹)": [
                    core_team_salary,
                    csr_admin_exp,
                    hr_expenses,
                    total_15,
                    direct_exp
                ]
            })

            # CUSTOM TABLE DESIGN for PAGE 1
            table_css_page1 = """
            <style>
            table {
                background-color: #cfe2ff !important;
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                font-weight: bold !important;
                color: black !important;
                border: 1px solid black !important;
                padding: 8px !important;
            }
            </style>
            """
            st.markdown(table_css_page1, unsafe_allow_html=True)

            st.write(df_calc.to_html(index=False), unsafe_allow_html=True)

            # Save to Excel
            if st.button("Save to Excel"):
                df_output = pd.DataFrame({
                    "Project Name": [project_name],
                    "Project Type": [project_type],
                    "Project Value": [project_value],
                    "Core Team Salary (5%)": [core_team_salary],
                    "CSR Admin Expenses (5%)": [csr_admin_exp],
                    "HR Expenses (5%)": [hr_expenses],
                    "Total 15%": [total_15],
                    "Project Direct Expenses (85%)": [direct_exp]
                })

                df_output.to_excel("hma_project_expenses_output.xlsx", index=False)
                st.success("Excel File Saved as **hma_project_expenses_output.xlsx**")


# -----------------------------------------------------------
# PAGE 2 — HMA CORE TEAM 
# -----------------------------------------------------------
elif menu == "HMA CORE TEAM":

    st.header("👥 HMA CORE TEAM SALARY DISTRIBUTION")
    st.markdown("---")

    # --- Step 1: Month Dropdown ---
    st.subheader("🗓Select Month")
    
    # --- File configuration and loading ---
    FILE_NAME_EXCEL = "BOOK12.xlsx"
    FILE_NAME_CSV = "BOOK12.xlsx - CORE MANPOWER.csv" 

    # Load data from file (cached)
    monthly_distribution_data = load_distribution_data(FILE_NAME_EXCEL, FILE_NAME_CSV, PROJECT_COLUMNS)
    
    # GUARANTEE FULL RANGE: Use the hardcoded MONTHS list for the dropdown options.
    available_months = MONTHS

    selected_month = st.selectbox("Month (JUN 2025 to MAR 2026)", available_months)
    
    # --- Set Monthly Values based on selected month ---
    default_total = 0.0
    default_splits = {proj: 0.0 for proj in PROJECT_COLUMNS}

    current_total_distribution_with_lsgb = default_total
    current_project_distribution_amounts = default_splits
    total_monthly_value = default_total
    
    # Check if data exists for the selected month in the file
    if selected_month in monthly_distribution_data:
        file_data = monthly_distribution_data[selected_month]
        # This overwrites the total with the value from the Excel file
        current_total_distribution_with_lsgb = file_data['total']
        current_project_distribution_amounts = file_data['splits']
        total_monthly_value = current_total_distribution_with_lsgb

    st.markdown(f"### **Selected Month's Total Value: ₹{total_monthly_value:,.2f}**")
    
    st.markdown("---")


    # --- Step 2: Employee Details ---
    st.subheader("👤 Enter Employee Details")

    # 1. NAME Dropdown/Manual Entry
    name_options = ["(Enter New Name Manually)"] + sorted(core_team_names)
    selected_name_option = st.selectbox("Name", name_options)
    
    if selected_name_option == "(Enter New Name Manually)":
        name = st.text_input("Enter New Employee Name Manually")
    else:
        name = selected_name_option

    # 2. DESIGNATION Dropdown/Manual Entry
    designation_options = ["(Enter New Designation Manually)"] + sorted(core_team_designations)
    selected_designation_option = st.selectbox("Designation", designation_options)
    
    if selected_designation_option == "(Enter New Designation Manually)":
        designation = st.text_input("Enter New Designation Manually")
    else:
        designation = selected_designation_option

    # 3. Project (Manual Entry, since it varies)
    project = st.text_input("Project")
    
    # 4. CTC/Attendance/Amount (Manual Entry/Calculation)
    monthly_ctc = st.number_input("Monthly CTC (₹)", min_value=0.0)
    attendance_max_days = st.number_input("Total Days in Month (For CTC split)", min_value=28, max_value=31, value=30)
    attendance = st.number_input("Attendance Days (Manual)", min_value=0, max_value=attendance_max_days, value=attendance_max_days)

    if attendance_max_days > 0 and monthly_ctc > 0:
        amount = (monthly_ctc / attendance_max_days) * attendance
    else:
        amount = 0.0


    # --- Step 3: Salary Distribution Split ---
    st.subheader("📌 Distribution Split")
    
    if total_monthly_value <= 0.0:
        st.warning(f"Total monthly value for **{selected_month}** is ₹0.00. Distribution cannot be calculated. Please check the value in your **{FILE_NAME_EXCEL}** file.")
    elif current_total_distribution_with_lsgb <= 0:
        st.error(f"Cannot calculate distribution. Base distribution total is zero. Please ensure your file (**{FILE_NAME_EXCEL}** or **{FILE_NAME_CSV}**) is correct and contains valid data for **{selected_month}**.")
    else:
        # Calculate scaling factor
        scaling_factor = total_monthly_value / current_total_distribution_with_lsgb
        
        split_amounts = {}
        sum_of_project_splits = 0
        
        # Calculate project splits
        for project_name_key, base_amount in current_project_distribution_amounts.items():
            scaled_amount = float(base_amount) * scaling_factor
            split_amounts[project_name_key] = scaled_amount
            sum_of_project_splits += scaled_amount

        # Calculate LSGB as the balance (remaining amount)
        lsgb_balance = total_monthly_value - sum_of_project_splits
        split_amounts["LSGB (Balance)"] = lsgb_balance 
        
        # Prepare and style DataFrame
        df_display = pd.DataFrame({
            "Project": list(split_amounts.keys()),
            "Amount (₹)": [f"₹{val:,.2f}" for val in split_amounts.values()]
        })

        # Apply custom HTML/CSS for light blue background and bold text
        html_table = df_display.to_html(index=False)
        styled_html = f'<div class="distribution-table">{html_table}</div>'

        st.markdown(styled_html, unsafe_allow_html=True)

# -----------------------------------------------------------
# PAGE 3 — HR EXPENSES
# -----------------------------------------------------------
elif menu == "HR EXPENSES":
    st.header("💼 HR Expenses Entry Form")
    st.markdown("---")

    OUTPUT_FILE_HR = "EXPENSE- MASTER SHEET.xlsx"

    with st.form("hr_expenses_form", clear_on_submit=True):
        st.subheader("Vendor, Service, and Payment Details")

        col1, col2 = st.columns(2)

        # 1. Vendor Dropdown/Manual
        with col1:
            selected_vendor = st.selectbox(
                "Vendor", 
                HR_VENDOR_OPTIONS, 
                index=None,
                placeholder="Select or Choose Manual Entry",
                key="hr_vendor_select"
            )
            final_vendor = selected_vendor
            # Check for manual entry requirement
            if selected_vendor == "Other (Enter Manually)":
                custom_vendor = st.text_input("Enter New Vendor Name Manually", key="hr_custom_vendor")
                if custom_vendor:
                    final_vendor = custom_vendor
                else:
                    # Keep as None if 'Other' is selected but not entered
                    final_vendor = None

        # 2. Services Dropdown/Manual
        with col2:
            selected_service = st.selectbox(
                "Service", 
                HR_SERVICE_OPTIONS, 
                index=None,
                placeholder="Select or Choose Manual Entry",
                key="hr_service_select"
            )
            final_service = selected_service
            # Check for manual entry requirement
            if selected_service == "Other (Enter Manually)":
                custom_service = st.text_input("Enter New Service Name Manually", key="hr_custom_service")
                if custom_service:
                    final_service = custom_service
                else:
                    # Keep as None if 'Other' is selected but not entered
                    final_service = None
        
        # 3. Payment Dropdown
        final_payment = st.selectbox(
            "Payment Frequency", 
            CSR_PAYMENT_FREQUENCY, # Re-using CSR list as it's the same
            index=None,
            placeholder="Select Payment Frequency",
            key="hr_payment_select"
        )
        
        st.markdown("---")
        st.subheader("Financial Commitments (Manual Input)")
        
        # 4. Manual Input Fields (Annual Commitment, Monthly Average, Actual)
        col3, col4, col5 = st.columns(3)
        
        with col3:
            annual_commitment = st.number_input("Annual commitment (₹)", min_value=0.0, format="%.2f", key="hr_annual_commitment")
        
        with col4:
            monthly_average = st.number_input("Monthly Average (₹)", min_value=0.0, format="%.2f", key="hr_monthly_average")
            
        with col5:
            actual_expense = st.number_input("Actual (₹)", min_value=0.0, format="%.2f", key="hr_actual_expense")

        st.markdown("---")
        submitted = st.form_submit_button("Submit HR Expense Entry and Update Master Sheet")

        if submitted:
            # Basic validation
            if not final_vendor or not final_service or not final_payment:
                st.error("Please ensure Vendor, Service, and Payment Frequency are selected/entered.")
            elif final_vendor == "Other (Enter Manually)" and not st.session_state.hr_custom_vendor:
                 st.error("Please enter the custom Vendor Name.")
            elif final_service == "Other (Enter Manually)" and not st.session_state.hr_custom_service:
                 st.error("Please enter the custom Service Name.")
            else:
                # 5. Data Update Requirement: Save to EXPENSE- MASTER SHEET.xlsx
                
                # Prepare data for saving
                new_entry = {
                    "Vendor": final_vendor,
                    "Service": final_service,
                    "Payment frequency": final_payment,
                    "Annual commitment": annual_commitment,
                    "Monthly Average": monthly_average,
                    "Actual expense": actual_expense,
                    # Placeholder columns to match the expense master sheet structure from file snippet
                    "Date Saved": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # Add project columns and LSGB for consistency with the expected Excel output structure
                # Initializing them to 0.0 as this page doesn't calculate distribution.
                project_cols_to_add = PROJECT_COLUMNS + ["LSGB"]
                for p_col in project_cols_to_add:
                     if p_col not in new_entry:
                         new_entry[p_col] = 0.0

                # Ensure order of columns for initial dataframe creation (optional but good practice)
                # Note: The actual columns in the master sheet might be much larger, but we stick to the core fields + projects.
                output_columns = ["Date Saved", "Vendor", "Service", "Payment frequency", 
                                  "Annual commitment", "Monthly Average", "Actual expense"] + project_cols_to_add
                
                df_output_hr = pd.DataFrame([new_entry], columns=output_columns)

                # Handle file reading/appending
                try:
                    if os.path.exists(OUTPUT_FILE_HR):
                        existing_df = pd.read_excel(OUTPUT_FILE_HR)
                        # Concatenate new data, ensuring column alignment
                        updated_df = pd.concat([existing_df, df_output_hr], ignore_index=True)
                    else:
                        updated_df = df_output_hr
                        
                    updated_df.to_excel(OUTPUT_FILE_HR, index=False)
                    st.success(f"HR Expense details for **{final_vendor}** saved successfully and updated in **{OUTPUT_FILE_HR}**.")
                    
                    # Optional: Display the saved entry
                    st.markdown("---")
                    st.subheader("Saved Entry Details")
                    st.dataframe(df_output_hr.head(1).T.rename(columns={0: "Value"}))
                    
                except Exception as e:
                    st.error(f"An error occurred while saving the data to the master sheet: {e}")

# -----------------------------------------------------------
# PAGE 4 — HMA CSR ADMIN EXPENSES
# -----------------------------------------------------------
elif menu == "HMA CSR ADMIN EXPENSES":
    st.header("🏢 HMA CSR ADMIN EXPENSES (5% HR)")
    st.markdown("---")

    # The block for loading base data (Step 0) has been removed as it's no longer needed for ratio-based calculation.

    # --- Step 1: Input Fields ---
    st.subheader("📝 Expense Details")
    
    col1, col2 = st.columns(2)
    with col1:
        # Month Dropdown (uses the full range) - Kept as requested
        selected_month = st.selectbox("Month (JUN 2025 to MAR 2026)", MONTHS, key="csr_month_select")
        vendor = st.selectbox("Vendor", CSR_VENDORS, key="csr_vendor_select")
        payment_frequency = st.selectbox("Payment Frequency", CSR_PAYMENT_FREQUENCY, key="csr_freq_select")
        annual_commitment = st.number_input("Annual Commitment (₹)", min_value=0.0, format="%.2f", key="csr_annual")
        
    with col2:
        expense_type = st.selectbox("Expense Type", CSR_EXPENSE_TYPES, key="csr_type_select")
        # Monthly Average is now the key distribution budget
        monthly_average = st.number_input("Monthly Average (₹)", min_value=0.0, format="%.2f", key="csr_monthly_avg")
        # Actual Expense is recorded separately
        actual_expense = st.number_input("**Actual (₹)** - Record Only", min_value=0.0, format="%.2f", key="csr_actual")
        
        st.markdown(f"**Monthly Average Value (Distribution Budget):** ₹{monthly_average:,.2f}")

    st.markdown("---")

    # --- Step 2: Manual Project Distribution Input ---
    st.subheader("💰 Project Distribution (Manual Entry)")
    st.info("The amounts for these projects must be entered manually. The balance from the **Monthly Average** will be automatically allocated to **LSGB (Balance)**.")
    st.markdown("---") 
    
    # Dictionary to store manual inputs
    manual_project_inputs = {}
    
    # Use 3 columns for a cleaner layout
    input_cols = st.columns(3)
    
    # Create input fields for the 11 fixed projects
    for i, project_name in enumerate(PROJECT_COLUMNS):
        with input_cols[i % 3]:
            manual_project_inputs[project_name] = st.number_input(
                f"**{project_name}** (₹)", 
                min_value=0.0, 
                format="%.2f", 
                value=0.0,
                key=f"csr_input_{project_name}"
            )
            
    sum_of_manual_inputs = sum(manual_project_inputs.values())
    
    st.markdown("---")

    # --- Step 3: LSGB Auto-Calculation and Display ---
    st.subheader("📌 Distributed Values (LSGB Calculated Automatically)")
    
    # The distribution budget is now monthly_average
    if monthly_average > 0:
        
        # 1. Validation Check: Manual inputs must not exceed the Monthly Average
        if sum_of_manual_inputs > monthly_average:
            st.error(f"❌ **Error:** The total manual input (₹{sum_of_manual_inputs:,.2f}) exceeds the Monthly Average budget (₹{monthly_average:,.2f}). Please correct the inputs.")
            lsgb_balance = 0.0 # Set to zero on error
        else:
            # 2. Calculate LSGB as the BALANCE
            # LSGB = Monthly Average - Sum of Manual Inputs
            lsgb_balance = monthly_average - sum_of_manual_inputs

        # Final distribution dictionary
        split_amounts_csr = manual_project_inputs.copy()
        split_amounts_csr["LSGB (Balance)"] = lsgb_balance
        
        # Total distributed must equal monthly_average (if no error occurred)
        total_distributed = sum_of_manual_inputs + lsgb_balance 
        
        # Prepare and style DataFrame
        df_display_csr = pd.DataFrame({
            "Project/Head": list(split_amounts_csr.keys()),
            "Distributed Amount (₹)": [val for val in split_amounts_csr.values()]
        })

        # Display Total Distributed to verify against Monthly Average
        st.info(f"Total Distributed Amount: **₹{total_distributed:,.2f}** (Matches Monthly Average Budget: ₹{monthly_average:,.2f})")
        
        # Format for display
        df_display_csr['Distributed Amount (₹)'] = df_display_csr['Distributed Amount (₹)'].apply(lambda x: f"₹{x:,.2f}")
        
        # Apply custom HTML/CSS for light blue background and bold text
        html_table_csr = df_display_csr.to_html(index=False)
        styled_html_csr = f'<div class="distribution-table">{html_table_csr}</div>'
        st.markdown(styled_html_csr, unsafe_allow_html=True)
        
    elif monthly_average == 0.0:
        st.info("Enter a value in the **Monthly Average (₹)** field to calculate the distribution split.")

    # --- Save to Excel button ---
    if st.button("Save CSR Expense Details"):
        # Validation check based on the new logic
        if monthly_average > 0 and sum_of_manual_inputs <= monthly_average:
            # Prepare data for saving
            output_data = {
                "Month": selected_month,
                "Vendor": vendor,
                "Expense Type": expense_type,
                "Payment Frequency": payment_frequency,
                "Annual Commitment (₹)": annual_commitment,
                "Monthly Average (₹)": monthly_average,
                "Actual (₹)": actual_expense
            }
            
            # Recalculate balance using session state for saving consistency
            sum_on_save = sum(st.session_state[f"csr_input_{p}"] for p in PROJECT_COLUMNS)
            lsgb_balance_on_save = st.session_state.csr_monthly_avg - sum_on_save
            
            output_data.update({p: st.session_state[f"csr_input_{p}"] for p in PROJECT_COLUMNS})
            output_data["LSGB (Balance)"] = lsgb_balance_on_save
            
            df_output_csr = pd.DataFrame([output_data])
            
            OUTPUT_FILE = "hma_csr_admin_expenses_output.xlsx"
            
            # Handle file reading/appending
            try:
                if os.path.exists(OUTPUT_FILE):
                    existing_df = pd.read_excel(OUTPUT_FILE)
                    updated_df = pd.concat([existing_df, df_output_csr], ignore_index=True)
                else:
                    updated_df = df_output_csr
                    
                updated_df.to_excel(OUTPUT_FILE, index=False)
                st.success(f"CSR Expense details saved successfully to **{OUTPUT_FILE}**.")
            except Exception as e:
                st.error(f"An error occurred while saving the data: {e}")
        else:
            st.warning("Please ensure the **Monthly Average** value is greater than zero and manual inputs do not exceed the Monthly Average before saving.")

# -----------------------------------------------------------
# PAGE 5 — HMA HR REVENUE (NEW)
# -----------------------------------------------------------
elif menu == "HMA HR REVENUE":
    st.header("💵 HMA HR REVENUE - INTERNSHIP DETAILS")
    st.markdown("---")

    # Input Form using st.form to enable clear_on_submit
    with st.form("internship_form", clear_on_submit=True):
        st.subheader("Enter Internship Student Details")
        
        student_name = st.text_input("Student Name")
        educational_qualification = st.text_input("Educational Qualification")
        phone_number = st.text_input("Phone Number")
        internship_amount = st.number_input("Internship Amount to be Paid (₹)", min_value=0.0, format="%.2f")

        submitted = st.form_submit_button("Save Details to Excel")

        if submitted:
            # 1. Validation
            if not student_name or not educational_qualification or not phone_number:
                st.error("Please fill in all mandatory fields (Name, Qualification, Phone Number).")
            else:
                # 2. Prepare new data
                new_data = pd.DataFrame([{
                    "Student Name": student_name,
                    "Educational Qualification": educational_qualification,
                    "Phone Number": phone_number,
                    "Internship Amount (₹)": internship_amount,
                    "Date Saved": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                
                OUTPUT_FILE = "hma_hr_revenue_output.xlsx"
                
                # 3. Handle file reading/appending
                try:
                    if os.path.exists(OUTPUT_FILE):
                        # File exists, read old data and append new data
                        existing_df = pd.read_excel(OUTPUT_FILE)
                        updated_df = pd.concat([existing_df, new_data], ignore_index=True)
                    else:
                        # File does not exist, use new data
                        updated_df = new_data
                        
                    # 4. Save the combined data
                    updated_df.to_excel(OUTPUT_FILE, index=False)
                    st.success(f"Details for **{student_name}** saved successfully to **{OUTPUT_FILE}**.")

                    # 5. Show confirmation/latest data
                    st.markdown("---")
                    st.subheader("Latest Intern Entry Saved")
                    # Use st.dataframe for a styled output of the last entry
                    st.dataframe(new_data)
                    
                except Exception as e:
                    st.error(f"An error occurred while saving the data: {e}")
