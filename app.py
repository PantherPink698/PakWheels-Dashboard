import streamlit as st
import pandas as pd
import plotly.express as px

# Load CSV
df = pd.read_csv("used cars.csv")

# Cleaning the Data
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['mileage_km'] = pd.to_numeric(df.get('mileage_km', df.get('mileage')), errors='coerce')

df = df.dropna(subset=['price', 'year'])
df = df[(df['price'] > 300000) & (df['price'] < 100000000)]
df = df[df['year'].between(1995, 2025)]

df['make'] = df['make'].str.title()
df['model'] = df['model'].str.title()

st.title("PakWheels Used Cars Dashboard")
st.write("70,000+ cars from Pakistan")

make = st.sidebar.selectbox("Choose Brand", ["All"] + sorted(df['make'].unique().tolist()))
data = df if make == "All" else df[df['make'] == make]

st.metric("Total Cars", len(data))
st.metric("Average Price", f"₨ {data['price'].mean():,.0f}")

st.plotly_chart(px.scatter(data.sample(min(1000, len(data))), 
                 x='year', y='price', color='make', hover_data=['model']))

st.write("Top 10 Most Expensive")
top10 = data.nlargest(10, 'price')[['make', 'model', 'year', 'price']].copy()
top10['price'] = top10['price'].apply(lambda x: f"₨ {x:,.0f}")
st.table(top10)

st.success("CONGRATULATIONS! Your first dashboard is LIVE!")

st.balloons()
