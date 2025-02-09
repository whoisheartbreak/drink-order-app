# A very simple interactive web app to take orders for drinks to help with quick meetup. 
# todo: downsize to functional previous version and cut the animation crap. 

import streamlit as st
import time
import csv
import datetime

# Empty dictionary, options to be filled from menu.csv.
drinks = {}

# Read from the CSV file
with open('menu.csv', mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    for row in csv_reader:
        # Add each row to the dictionary where 'name' is the key and 'ingredients' is the value
        drinks[row['name']] = row['ingredients']

# Initialise 
if 'name' not in st.session_state:
    st.session_state.name = ""

if 'drink' not in st.session_state:
    st.session_state.drink = ""


def order_confirmation():
    st.write(f"Thank you, {st.session_state.name}! Your {st.session_state.drink} will be ready soon.")
    # Record order. Do not manually modify the orders.csv file, it will be managed by the script here. 
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    order_data = [st.session_state.name, st.session_state.drink, timestamp]
    with open('orders.csv', mode='a', newline='', encoding='utf-8',) as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(order_data)

    # Buttons for further actions
    if st.button("New Order 🔁"):
        st.session_state.confirmed = False
        st.session_state.name = ""
        st.session_state.drink = ""
        st.rerun()

    if st.button("Cancel Order 🥂"):
        temp_data = []
        found = False
        with open('orders.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            header = next(reader)  
            for row in reader:
                # Check if the name, drink, and time match the current session state
                if (row[0] == st.session_state.name and 
                    row[1] == st.session_state.drink):
                    found = True
                else:
                    temp_data.append(row)
            # If the order was found, write back the data without the canceled order
            if found:
                with open('orders.csv', mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(header)  # Write header back
                    writer.writerows(temp_data)
                st.write(f"Your order ({st.session_state.drink} for {st.session_state.name}) has been canceled. You can order another drink in a while.") 
            else:
                st.write(f"Your order could not be cancelled. You can order an additional drink in a while.")
        st.session_state.confirmed = False
        st.session_state.name = ""
        st.session_state.drink = "" 
        time.sleep(2)
        st.rerun()

# Main Page
def main_page():
    st.title("Order Your Drink 🎉")
    
    # Name input
    st.session_state.name = st.text_input(label="Name:")
    
    # Drink selection
    st.session_state.drink = st.selectbox(
        "Choose your drink:", 
        list(drinks.keys()), 
        index=list(drinks.keys()).index(st.session_state.drink) if st.session_state.drink else None
    )
    
    # Display ingredients
    if st.session_state.drink:
        st.write(drinks[st.session_state.drink])
    
    # Order confirmation button
    if st.button('Confirm and Place Order') and st.session_state.name and st.session_state.drink:
        st.session_state.confirmed = True
        st.rerun()
    elif st.session_state.name == "" or not st.session_state.drink:
        st.warning("Please enter your name and select a drink.")

# Run time
if __name__ == "__main__":
    if 'confirmed' not in st.session_state:
        st.session_state.confirmed = False
    if st.session_state.confirmed:
        order_confirmation()
    else:
        main_page()

