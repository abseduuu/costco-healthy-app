import streamlit as st
import requests
from bs4 import BeautifulSoup

# Healthy keyword tags to look for
HEALTHY_KEYWORDS = ["organic", "low carb", "keto", "gluten-free", "high protein", "no added sugar"]

# 🔹 Fallback sample data (mocked)
MOCK_HEALTHY_PRODUCTS = [
    "Kirkland Organic Almond Butter - No Added Sugar",
    "Thai Kitchen Organic Coconut Milk (Unsweetened)",
    "Wildbrine Korean Kimchi - Probiotic, Vegan",
    "Kirkland Signature Cage-Free Egg Whites",
    "Aidells Chicken & Apple Sausage - Gluten-Free",
    "Kirkland Organic Roasted Seaweed Snacks",
]

def is_healthy(text):
    return any(keyword in text.lower() for keyword in HEALTHY_KEYWORDS)

def scrape_costco_products(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return [f"⚠️ Failed to fetch page (status code: {response.status_code})"]

        soup = BeautifulSoup(response.text, "html.parser")
        products = []

        product_elements = soup.find_all("div", class_="product-tile-set")
        if not product_elements:
            return ["⚠️ No product tiles found. Try a category page."]

        for product in product_elements:
            name = product.get_text(separator=" ").strip()
            if is_healthy(name):
                products.append(name)

        return products if products else ["ℹ️ No healthy products found on this page."]
    except Exception as e:
        return ["❌ Could not load Costco page — using mock data instead."] + MOCK_HEALTHY_PRODUCTS

# 🔷 Streamlit App UI
st.title("🥦 Costco Healthy Product Finder")
st.write("Paste a Costco category URL (like https://www.costco.com/frozen-food.html), and we’ll find healthy items!")

url = st.text_input("Enter Costco URL:")

if st.button("Find Healthy Products") and url:
    with st.spinner("Scanning Costco page..."):
        results = scrape_costco_products(url)

    st.success(f"Found {len(results)} healthy product(s):")
    for item in results:
        st.write("•", item)
