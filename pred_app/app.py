import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Function to load sales prediction models
def load_sales_models():
    sales_models = {}
    for product_id in range(1, 79):
        sales_models[product_id] = joblib.load(f'svr_model_productid_{product_id}.joblib')
    total_sales_model = joblib.load('svr_model_total_sales.joblib')
    return sales_models, total_sales_model

# Predict prices
def predict_price(model, year, month):
    return model.predict(pd.DataFrame({'Year': [year], 'Month': [month]}))[0]

# Predict sales
def predict_sales(model, past_sales):
    return model.predict([past_sales])[0]

# Plot sales data
def plot_sales(past_sales, prediction):
    plt.figure(figsize=(10, 4))
    plt.plot(past_sales, label='Historical Sales', marker='o')
    plt.plot(len(past_sales), prediction, 'ro', label='Predicted Sales')
    plt.plot([len(past_sales)-1, len(past_sales)], [past_sales[-1], prediction], 'r--')
    plt.xlabel('Days')
    plt.ylabel('Sales')
    plt.title('Sales Prediction')
    plt.legend()
    st.pyplot(plt)

# Provide restocking advice
def provide_restocking_advice(current_price, last_price):
    if current_price < last_price:
        return "Our suggestion on restocking: Buy"
    elif current_price > last_price:
        return "Our suggestion on restocking: Wait"
    else:
        return "Our suggestion on restocking: Hold"


def main():
    st.title("Coffee Shop Sales and Price Predicting")

    # Load models
    coffee_model = joblib.load('coffee_model.joblib')
    tea_model = joblib.load('tea_model.joblib')
    sales_models, total_sales_model = load_sales_models()

    # Sidebar for user input
    st.sidebar.header("Input Data")

    # Inputs for sales predictions
    st.sidebar.subheader("Sales Prediction")
    product_id = st.sidebar.selectbox("Select Product ID", options=list(range(1, 88)) + ['Total Sale'])
    past_sales_input = st.sidebar.text_input("Enter Past 14 Days' Sales (comma-separated)", value="")
    uploaded_file = st.sidebar.file_uploader("Or upload CSV file", type=['csv'])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, header=None)
        past_sales = data.iloc[0].tolist()
    elif past_sales_input:
        past_sales = list(map(float, past_sales_input.split(',')))
    else:
        past_sales = []

    # Inputs for price predictions
    year = st.sidebar.number_input("Year", min_value=1990, max_value=2020, value=2019)
    month = st.sidebar.number_input("Month", min_value=1, max_value=12, value=1)

    # Price prediction buttons
    if st.sidebar.button('Predict Coffee Bean Price'):
        coffee_price = predict_price(coffee_model, year, month)
        st.success(f'Predicted Coffee Bean Price for {year}-{month}: ${coffee_price:.2f}')

    if st.sidebar.button('Predict Loose Tea Price'):
        tea_price = predict_price(tea_model, year, month)
        st.success(f'Predicted Loose Tea Price for {year}-{month}: ${tea_price:.2f}')

    if st.sidebar.button('Predict Sales') and past_sales:
        if product_id == 'Total Sale':
            prediction = predict_sales(total_sales_model, past_sales)
        else:
            prediction = predict_sales(sales_models[product_id], past_sales)

        plot_sales(past_sales, prediction)
        st.success(f'Predicted Sales for Product ID {product_id}: {prediction:.2f}')

        # Restocking advice for coffee (product IDs 1-10)
        if 1 <= product_id <= 10:
            current_coffee_price = predict_price(coffee_model, year, month)
            last_month = month - 1 if month > 1 else 12
            last_year = year - 1 if month == 1 else year
            last_coffee_price = predict_price(coffee_model, last_year, last_month)
            restocking_advice = provide_restocking_advice(current_coffee_price, last_coffee_price)
            st.write(f'Predicted Coffee Bean Price: ${current_coffee_price:.2f}')
            st.write(restocking_advice)

        # Restocking advice for tea (product IDs 11-18)
        elif 11 <= product_id <= 18:
            current_tea_price = predict_price(tea_model, year, month)
            last_month = month - 1 if month > 1 else 12
            last_year = year - 1 if month == 1 else year
            last_tea_price = predict_price(tea_model, last_year, last_month)
            restocking_advice = provide_restocking_advice(current_tea_price, last_tea_price)
            st.write(f'Predicted Loose Tea Price: ${current_tea_price:.2f}')
            st.write(restocking_advice)

if __name__ == '__main__':
    main()







#%%
