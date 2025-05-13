# app.py

import streamlit as st
import requests
from bs4 import BeautifulSoup

# Healthy keyword tags to look for in product names
HEALTHY_KEYWORDS = ["organic", "low carb", "keto", "gluten-free", "high protein", "no added sugar"]

def is_healthy(text):
    return any(keyword in text.lower() for keyword in HEALTHY_KEYWORDS)

def scrape_costco_products(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        products = []

        # Look for product tiles (Costco layout is dynamic, so this may need adjusting)
        product_elements = soup.find_all("div", class_="product-tile-set")

        for product in product_elements:
            name = product.get_text(separator=" ").strip()
            if is_healthy(name):
                products.append(name)

        return products
    except Exception as e:
        return [f"Error scraping site: {e}"]

# Streamlit app layout
st.title("🥦 Costco Healthy Product Finder")
st.write("Paste a Costco category URL (like https://www.costco.com/frozen-food.html), and we’ll find healthy items!")

url = st.text_input("Enter Costco URL:")

if st.button("Find Healthy Products") and url:
    with st.spinner("Scanning Costco page..."):
        results = scrape_costco_products(url)
    if results:
        st.success(f"Found {len(results)} healthy product(s):")
        for item in results:
            st.write("•", item)
    else:
        st.warning("No healthy products found or scraping failed. Try another page.")
