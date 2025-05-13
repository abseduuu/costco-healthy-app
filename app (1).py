
import streamlit as st
import pandas as pd
import io
import json
import os

# ----------------------------
# Load Products from JSON
# ----------------------------
store_files = {
    "Costco": "products_costco.json",
    "Whole Foods": "products_wholefoods.json"
}

store = st.sidebar.selectbox("Where are you shopping?", list(store_files.keys()))

# Load selected store's product data
try:
    with open(store_files[store], "r") as f:
        PRODUCTS = json.load(f)
except Exception as e:
    st.error(f"Error loading products for {store}: {e}")
    PRODUCTS = []

# ----------------------------
# Session State
# ----------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filter Products")
diet_options = sorted(list(set(d for p in PRODUCTS for d in p["diet"])))
diet = st.sidebar.selectbox("Choose a diet", diet_options)

category = st.sidebar.selectbox(
    "Select a category", ["All"] + sorted(list(set(p["category"] for p in PRODUCTS)))
)

search_query = st.sidebar.text_input("Search by product name:")

# ----------------------------
# Filter Products
# ----------------------------
filtered_products = [
    p for p in PRODUCTS
    if diet in p["diet"]
    and (category == "All" or p["category"] == category)
    and (search_query.lower() in p["name"].lower())
]

# ----------------------------
# Main Content
# ----------------------------
st.title("🥦 Healthy Grocery Finder")

for idx, product in enumerate(filtered_products):
    with st.container():
        st.subheader(product["name"])
        st.write(f"**Store:** {product['store']}  |  **Category:** {product['category']}")
        st.write("**Diet Tags:**", ", ".join(product["diet"]))
        st.write(f"**Price:** ${product['price']:.2f}")
        st.markdown(f"[🔗 View Product]({product['link']})", unsafe_allow_html=True)
        st.write("**Nutrition per serving:**")
        st.write(product["nutrition"])

        if st.button(f"Add to Cart: {product['name']}", key=f"add_{idx}"):
            st.session_state.cart.append(product["name"])
            st.success(f"Added to cart: {product['name']}")

        if product["name"] in st.session_state.favorites:
            if st.button(f"Unfavorite: {product['name']}", key=f"unfav_{idx}"):
                st.session_state.favorites.remove(product["name"])
                st.warning(f"Removed from favorites: {product['name']}")
        else:
            if st.button(f"⭐ Favorite: {product['name']}", key=f"fav_{idx}"):
                st.session_state.favorites.append(product["name"])
                st.success(f"Added to favorites: {product['name']}")

        st.markdown("---")

# ----------------------------
# Cart and Favorites in Sidebar
# ----------------------------
st.sidebar.header("🛒 Your Cart")
total_macros = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
total_price = 0.0
updated_cart = []

if st.session_state.cart:
    for idx, item in enumerate(st.session_state.cart):
        product = next((p for p in PRODUCTS if p["name"] == item), None)
        if product:
            st.sidebar.write(f"**{item}** - ${product['price']:.2f}")
            if st.sidebar.button(f"Remove {item}", key=f"remove_{idx}"):
                continue
            updated_cart.append(item)
            total_price += product["price"]
            for k in total_macros:
                total_macros[k] += product["nutrition"][k]
else:
    st.sidebar.write("Cart is empty.")

st.session_state.cart = updated_cart

if updated_cart:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Total Macros")
    st.sidebar.write(f"Calories: {total_macros['calories']}")
    st.sidebar.write(f"Protein: {total_macros['protein']}g")
    st.sidebar.write(f"Carbs: {total_macros['carbs']}g")
    st.sidebar.write(f"Fat: {total_macros['fat']}g")
    st.sidebar.write(f"💵 **Total Price:** ${total_price:.2f}")

# ----------------------------
# Favorites
# ----------------------------
st.sidebar.header("⭐ Favorites")
if st.session_state.favorites:
    for item in st.session_state.favorites:
        st.sidebar.write(f"• {item}")
else:
    st.sidebar.write("No favorites yet.")

# ----------------------------
# Export / Copy Cart
# ----------------------------
if updated_cart:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧾 Export Your Cart")

    cart_data = []
    for item in updated_cart:
        product = next((p for p in PRODUCTS if p["name"] == item), None)
        if product:
            cart_data.append({
                "Product": product["name"],
                "Price": product["price"],
                **product["nutrition"]
            })

    df = pd.DataFrame(cart_data)
    st.sidebar.text_area("Copy List:", "\n".join(updated_cart), height=150)

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.sidebar.download_button(
        label="⬇️ Download as CSV",
        data=csv_buffer.getvalue(),
        file_name="my_healthy_cart.csv",
        mime="text/csv"
    )
