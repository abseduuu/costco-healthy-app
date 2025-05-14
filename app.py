
import streamlit as st
import pandas as pd
import json
import io

# ----------------------------
# Load and Tag Products
# ----------------------------
with open("products_wholefoods_with_nutrition.json") as f:
    PRODUCTS = json.load(f)

def generate_tags(product):
    tags = []
    n = product.get("nutrition", {})
    if not all(k in n and n[k] is not None for k in ["protein", "fat", "carbs", "calories"]):
        return tags
    if n["protein"] >= 20:
        tags.append("High Protein")
    if n["carbs"] <= 10:
        tags.append("Low Carb")
    if n["fat"] <= 5:
        tags.append("Low Fat")
    if n["calories"] <= 200:
        tags.append("Light Meal")
    return tags

for p in PRODUCTS:
    p["tags"] = generate_tags(p)

# ----------------------------
# Streamlit App
# ----------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# Sidebar filters
st.sidebar.header("Filter Products")
category_options = sorted(list(set(p["category"] for p in PRODUCTS)))
category = st.sidebar.selectbox("Select a category", ["All"] + category_options)
search_query = st.sidebar.text_input("Search by product name:")

# Tag filters
all_tags = ["High Protein", "Low Carb", "Low Fat", "Light Meal"]
selected_tags = st.sidebar.multiselect("Filter by Tags", all_tags)

# Filtered products
filtered_products = []
for p in PRODUCTS:
    if category != "All" and p["category"] != category:
        continue
    if search_query.lower() not in p["name"].lower():
        continue
    if selected_tags and not all(tag in p["tags"] for tag in selected_tags):
        continue
    filtered_products.append(p)

# Main content
st.title("🥦 Whole Foods Product Finder")

for idx, product in enumerate(filtered_products):
    with st.container():
        st.subheader(product["name"])
        st.write(f"**Category:** {product['category']}")
        if product.get("image"):
            st.image(product["image"], width=150)
        st.write("**Nutrition per serving:**")
        st.write(product["nutrition"])
        if product.get("tags"):
            st.write("**Tags:**", ", ".join(product["tags"]))

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

# Cart display
st.sidebar.header("🛒 Your Cart")
total_macros = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
updated_cart = []

if st.session_state.cart:
    for idx, item in enumerate(st.session_state.cart):
        product = next((p for p in PRODUCTS if p["name"] == item), None)
        if product:
            st.sidebar.write(f"**{item}**")
            if st.sidebar.button(f"Remove {item}", key=f"remove_{idx}"):
                continue
            updated_cart.append(item)
            for k in total_macros:
                if product["nutrition"][k] is not None:
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

# Favorites
st.sidebar.header("⭐ Favorites")
if st.session_state.favorites:
    for item in st.session_state.favorites:
        st.sidebar.write(f"• {item}")
else:
    st.sidebar.write("No favorites yet.")

# Export
if updated_cart:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧾 Export Your Cart")
    cart_data = []
    for item in updated_cart:
        product = next((p for p in PRODUCTS if p["name"] == item), None)
        if product:
            cart_data.append({
                "Product": product["name"],
                **product["nutrition"]
            })

    df = pd.DataFrame(cart_data)
    st.sidebar.text_area("Copy List:", "\n".join(updated_cart), height=150)

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.sidebar.download_button(
        label="⬇️ Download as CSV",
        data=csv_buffer.getvalue(),
        file_name="my_wholefoods_cart.csv",
        mime="text/csv"
    )
