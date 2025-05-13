import streamlit as st
import requests
from bs4 import BeautifulSoup

# Healthy keyword tags to look for
HEALTHY_KEYWORDS = ["organic", "low carb", "keto", "gluten-free", "high protein", "no added sugar"]

# 🔹 Fallback sample data (mocked)
MOCK_HEALTHY_PRODUCTS = [
    {
        "name": "Kirkland Organic Almond Butter - No Added Sugar",
        "link": "https://www.costco.com/kirkland-signature-organic-almond-butter-27-oz%2C-2-count.product.100690406.html",
        "image": "https://mobilecontent.costco.com/live/resource/img/100690406_0.jpg"
    },
    {
        "name": "Thai Kitchen Organic Coconut Milk (Unsweetened)",
        "link": "https://www.costco.com/thai-kitchen-organic-coconut-milk-unsweetened-13.66-fl-oz%2C-6-count.product.100679472.html",
        "image": "https://mobilecontent.costco.com/live/resource/img/100679472_0.jpg"
    },
    {
        "name": "Wildbrine Korean Kimchi - Probiotic, Vegan",
        "link": "https://www.costco.com/wildbrine-korean-kimchi%2C-26-oz.product.100669365.html",
        "image": "https://mobilecontent.costco.com/live/resource/img/100669365_0.jpg"
    }
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
        if isinstance(item, dict):
            st.image(item["image"], width=100)
            st.markdown(f"[**{item['name']}**]({item['link']})", unsafe_allow_html=True)
            st.markdown("---")
        else:
            st.write("•", item)

