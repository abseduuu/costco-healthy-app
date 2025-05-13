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
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Almonds_in_shell_and_shelled.jpg/320px-Almonds_in_shell_and_shelled.jpg",
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
        "image": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Coconut_milk_in_glass.jpg",
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
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Chicken_sausages.JPG",
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