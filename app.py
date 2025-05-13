import streamlit as st

# ----------------------------
# Mock Product Data with Images
# ----------------------------
PRODUCTS = [
    {
        "name": "Kirkland Organic Almond Butter",
        "store": "Costco",
        "diet": "High-Protein, Low-Carb",
        "category": "Snacks",
        "image": "https://via.placeholder.com/100?text=Almond+Butter",
        "nutrition": {
            "calories": 190,
            "protein": 7,
            "carbs": 6,
            "fat": 16
        }
    },
    {
        "name": "Thai Kitchen Organic Coconut Milk",
        "store": "Costco",
        "diet": "High-Protein, Low-Carb",
        "category": "Pantry",
        "image": "https://via.placeholder.com/100?text=Coconut+Milk",
        "nutrition": {
            "calories": 120,
            "protein": 1,
            "carbs": 2,
            "fat": 12
        }
    },
    {
        "name": "Aidells Chicken & Apple Sausage",
        "store": "Costco",
        "diet": "High-Protein, Low-Carb",
        "category": "Meat",
        "image": "https://via.placeholder.com/100?text=Sausage",
        "nutrition": {
            "calories": 170,
            "protein": 13,
            "carbs": 3,
            "fat": 12
        }
    }
]

# ----------------------------
# Session State for Cart
# ----------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filter Products")
store = st.sidebar.selectbox("Where are you shopping?", ["Costco"])
diet = st.sidebar.selectbox("Choose a diet", ["High-Protein, Low-Carb"])
category = st.sidebar.selectbox("Select a category", ["All"] + sorted(list(set(p["category"] for p in PRODUCTS))))

# ----------------------------
# Product Filtering
# ----------------------------
filtered_products = [
    p for p in PRODUCTS
    if p["store"] == store and p["diet"] == diet and (category == "All" or p["category"] == category)
]

# ----------------------------
# Main App Content
# ----------------------------
st.title("🥦 Healthy Grocery Finder")
st.markdown("Use the sidebar to choose your store, diet, and category.")

for product in filtered_products:
    with st.container():
        st.image(product.get("image", "https://via.placeholder.com/100"), width=100)
        st.subheader(product["name"])
        st.write(f"**Category:** {product['category']}")
        st.write("**Nutrition per serving:**")
        st.write(product["nutrition"])
        if st.button(f"Add to Cart: {product['name']}"):
            st.session_state.cart.append(product["name"])
            st.success(f"Added to cart: {product['name']}")
        st.markdown("---")

# ----------------------------
# View Cart
# ----------------------------
st.sidebar.header("🛒 Your Cart")
if st.session_state.cart:
    for item in st.session_state.cart:
        st.sidebar.write("•", item)
else:
    st.sidebar.write("Cart is empty.")
