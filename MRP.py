# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import warnings

# Ignore warnings
warnings.filterwarnings('ignore')

# Title
st.title('Material Requirements Planning')
st.divider()
st.markdown('Lot Size = 100 units')
st.divider()
# Read data


# Tent's Gross Requirements and part quantities as previously defined
tent_gross_requirements = [0, 100, 100, 0, 100, 0, 100, 100, 100, 0, 100, 100]
part_quantities = {
    1000: 1, 1100: 1, 1110: 12.5, 1120: 4, 1130: 5, 1131: 10, 1132: 9, 1133: 10,
    1200: 1, 1210: 1, 1211: 1, 1212: 6.5, 1220: 1, 1221: 1, 1222: 1, 999: 4.5,
    1230: 3, 1240: 24, 1250: 8, 1260: 2, 1300: 1, 1310: 4, 1400: 6, 1500: 4,
    1510: 4, 1520: 4
}
large_tent_part_quantities = {
    2000: 1, 2100: 1, 1110: 24.8, 1120: 2, 1130: 5, 1131: 10, 1132: 9, 1133: 10,
    2200: 1, 2210: 1, 1211: 2, 1212: 11, 2220: 1, 1221: 1, 1222: 1, 999: 10,
    2230: 5, 1240: 24, 1250: 6, 1260: 4, 1400: 10, 1500: 6, 1510: 6, 1520: 6
}
# Combine part quantities for both tent types
total_part_quantities = part_quantities.copy()  # Start with 3-Season Tent quantities

# Add quantities from Large Summer Tent, updating existing entries or adding new ones
for part, quantity in large_tent_part_quantities.items():
    if part in total_part_quantities:
        total_part_quantities[part] += quantity  # Add to existing part quantities
    else:
        total_part_quantities[part] = quantity  # Add new part entry

initial_order_release = [25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Initial order release for tents

part_descriptions = {
    1000: "3-Season Tent",
    1100: "Bag",
    1110: "Nylon Fabric",
    1120: "Decal",
    1130: "Zipper",
    1131: "Metal Teeth",
    1132: "Metal Slider",
    1133: "Tape",
    1200: "Fabric Frame",
    1210: "Flooring",
    1211: "Tarp",
    1212: "Thread",
    1220: "Front Wall",
    1221: "Door",
    1222: "Window",
    999:  "Mesh",
    1230: "Non-Front Wall",
    1240: "Pole Clip",
    1250: "Stake Ring",
    1260: "Pocket",
    1300: "Rain Fly",
    1310: "Polyester Fabric",
    1400: "Stake",
    1500: "Frame Pole",
    1510: "Crimp",
    1520: "Elastic Connector",
}

part_descriptions_large_summer = {
    2000: "Large Summer Tent",
    2100: "Large Bag",
    2200: "Large Fabric Frame",
    2210: "Large Flooring",
    2220: "Large Front Wall",
    2230: "Large Non-Front Wall",
    1110: "Nylon Fabric",  # Shared parts
    1120: "Decal",         # Shared parts
    1130: "Zipper",        # Shared parts
    1131: "Metal Teeth",   # Shared parts
    1132: "Metal Slider",  # Shared parts
    1133: "Tape",          # Shared parts
    1211: "Tarp",          # Shared parts
    1212: "Thread",        # Shared parts
    1221: "Door",          # Shared parts
    1222: "Window",        # Shared parts
    999:  "Mesh",          # Shared parts
    1240: "Pole Clip",     # Shared parts
    1250: "Stak Ring",     # Shared parts
    1260: "Pocket",        # Shared parts
    1400: "Stake",         # Shared parts
    1500: "Frame Pole",    # Shared parts
    1510: "Crimp",         # Shared parts
    1520: "Elastic Connector"  # Shared parts
}

def compute_mrp(part_id, main_product_quantity):
    days = 7  # Total number of days in the MRP plan
    part_multiplier = part_quantities[part_id]  # Get the multiplier for the part
    total_part_need = main_product_quantity * part_multiplier  # Calculate total need for the part
    # Initialize all fields to zero
    df_mrp = pd.DataFrame({
        'Day': range(1, days + 1),
        'Gross Requirements': [0] * days,
        'Projected Available': [0] * days,
        'Net Requirement': [0] * days,
        'Planned Order Receipt': [0] * days,
        'Planned Order Release': [0] * days
    })

    # Determine the timing based on the number of zeros in the part number
    zero_count = sum(c == '0' for c in str(part_id))
    if zero_count == 3:
        due_day = days-1  # 3 days before Day 7
    elif zero_count == 2:
        due_day = days-2  # 2 days before Day 7
    elif zero_count == 1:
        due_day = days-3  # 1 day before Day 7
    elif zero_count == 0:
        due_day = days-4
    else:
        due_day = days-days+1  # On Day 7

    if part_id == 1000:  # For the main product
        # Set values for main product on Day 7
        df_mrp.at[6, 'Gross Requirements'] = main_product_quantity
        df_mrp.at[6, 'Net Requirement'] = main_product_quantity
        df_mrp.at[6, 'Planned Order Receipt'] = main_product_quantity
        if days > 5:
            df_mrp.at[5, 'Planned Order Release'] = main_product_quantity
    else:
        if 1 <= due_day <= days:  # Check due_day within the valid range
            df_mrp.at[due_day, 'Gross Requirements'] = total_part_need
            df_mrp.at[due_day, 'Net Requirement'] = total_part_need
            df_mrp.at[due_day, 'Planned Order Receipt'] = total_part_need
            if due_day > 1:  # Ensure there's a day before to place a release
                df_mrp.at[due_day - 1, 'Planned Order Release'] = total_part_need

    return df_mrp
def compute_mrp_large(part_id2, main_product_quantity2):
    days = 7  # Total number of days in the MRP plan
    part_multiplier = large_tent_part_quantities[part_id2]  # Get the multiplier for the part
    total_part_need = main_product_quantity2 * part_multiplier  # Calculate total need for the part
    # Initialize all fields to zero
    df_mrp2 = pd.DataFrame({
        'Day': range(1, days + 1),
        'Gross Requirements': [0] * days,
        'Projected Available': [0] * days,
        'Net Requirement': [0] * days,
        'Planned Order Receipt': [0] * days,
        'Planned Order Release': [0] * days
    })

    # Determine the timing based on the number of zeros in the part number
    zero_count = sum(c == '0' for c in str(part_id))
    if zero_count == 3:
        due_day = days-1  # 3 days before Day 7
    elif zero_count == 2:
        due_day = days-2  # 2 days before Day 7
    elif zero_count == 1:
        due_day = days-3  # 1 day before Day 7
    elif zero_count == 0:
        due_day = days-4
    else:
        due_day = days-days+1  # On Day 7

    if part_id2 == 2000:  # For the main product
        # Set values for main product on Day 7
        df_mrp2.at[6, 'Gross Requirements'] = main_product_quantity2
        df_mrp2.at[6, 'Net Requirement'] = main_product_quantity2
        df_mrp2.at[6, 'Planned Order Receipt'] = main_product_quantity2
        if days > 5:
            df_mrp2.at[5, 'Planned Order Release'] = main_product_quantity2
    else:
        if 1 <= due_day <= days:  # Check due_day within the valid range
            df_mrp2.at[due_day, 'Gross Requirements'] = total_part_need
            df_mrp2.at[due_day, 'Net Requirement'] = total_part_need
            df_mrp2.at[due_day, 'Planned Order Receipt'] = total_part_need
            if due_day > 1:  # Ensure there's a day before to place a release
                df_mrp2.at[due_day - 1, 'Planned Order Release'] = total_part_need

    return df_mrp2

with st.form("tent_input_form"):
    main_product_quantity = st.number_input('Quantity of 3-Season Tents Needed', min_value=1, value=100, step=1)
    part_id = st.selectbox('Select Part Number for 3-Season Tents MRP', options=list(part_descriptions.keys()), format_func=lambda x: f"{x} - {part_descriptions[x]}")
    main_product_quantity2 = st.number_input('Quantity of Large Summer Tents Needed', min_value=1, value=100, step=1)
    part_id2 = st.selectbox('Select Part Number for Large Summer Tents MRP', options=list(part_descriptions_large_summer.keys()), format_func=lambda x: f"{x} - {part_descriptions_large_summer[x]}")
    submitted = st.form_submit_button("Submit")


if submitted:
    st.subheader('3-Season Tent MRP')
    st.write(f"MRP for {part_descriptions[part_id]} (Part {part_id}):")
    df_mrp = compute_mrp(part_id, main_product_quantity)
    df_mrp=df_mrp.T
    st.table(df_mrp)
    # Summary Table of Total Parts Needed
    # Calculate the total parts needed multiplying by the main product quantity
    total_parts = {part_id: int(quantity * main_product_quantity) for part_id, quantity in part_quantities.items()}
    # Create a DataFrame from the dictionary and ensure integers are used for quantities
    df_total_parts = pd.DataFrame(list(total_parts.items()), columns=['Part ID', 'Total Quantity'])
    df_total_parts['Total Quantity'] = df_total_parts['Total Quantity'].astype(int)  # Convert to int if not already
    st.write(f"Total parts required for {main_product_quantity} 3-season Tents:")
    st.table(df_total_parts.set_index('Part ID'))

    st.divider()
    st.subheader('Large Summer Tent MRP')
    st.write(f"MRP for {part_descriptions_large_summer[part_id2]} (Part {part_id2}):")
    df_mrp2 = compute_mrp_large(part_id2, main_product_quantity2)
    df_mrp2=df_mrp2.T
    st.table(df_mrp2)
    # Summary Table of Total Parts Needed
    # Calculate the total parts needed multiplying by the main product quantity
    total_parts2 = {part_id2: int(quantity * main_product_quantity2) for part_id2, quantity in large_tent_part_quantities.items()}
    # Create a DataFrame from the dictionary and ensure integers are used for quantities
    df_total_parts2 = pd.DataFrame(list(total_parts2.items()), columns=['Part ID', 'Total Quantity'])
    df_total_parts2['Total Quantity'] = df_total_parts2['Total Quantity'].astype(int)  # Convert to int if not already
    st.write(f"Total parts required for {main_product_quantity2} Large Summer Tents:")
    st.table(df_total_parts2.set_index('Part ID'))

    st.divider()
    st.subheader('Total Parts Required')
    df_total_parts.set_index('Part ID', inplace=True)
    df_total_parts2.set_index('Part ID', inplace=True)

    # Combine the dataframes by adding them together
    combined_df = df_total_parts.add(df_total_parts2, fill_value=0)

    # Reset index to move 'Part ID' back to a column
    combined_df.reset_index(inplace=True)

    # Ensure the 'Total Quantity' column is integer
    combined_df['Total Quantity'] = combined_df['Total Quantity'].astype(int)

    # Display combined table in Streamlit
    st.write(f"Total parts required for {main_product_quantity} 3-season Tents and {main_product_quantity2} Large Summer Tents:")
    st.table(combined_df.set_index('Part ID'))
