
import streamlit as st
import pandas as pd
import json
import io

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

if "cart" not in st.session_state:
    st.session_state.cart = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []

def tag_html(tag):
    return f"<span style='background-color:#e6f4ea; color:#2e7d32; padding:2px 8px; margin:2px; display:inline-block; border-radius:12px; font-size:13px'>{tag}</span>"

st.markdown("""
<style>
.floating-header {
    position: sticky;
    top: 0;
    background: white;
    padding: 0.5rem 0;
    z-index: 999;
    border-bottom: 1px solid #f0f0f0;
}
.floating-header h1 {
    font-size: 28px;
    margin-bottom: 0;
}
</style>
<div class='floating-header'><h1>🥦 Whole Foods Product Finder</h1></div>
""", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("Filter Products")
category_options = sorted(list(set(p["category"] for p in PRODUCTS)))
category = st.sidebar.selectbox("Select a category", ["All"] + category_options)
search_query = st.sidebar.text_input("Search by product name:")
all_tags = ["High Protein", "Low Carb", "Low Fat", "Light Meal"]
selected_tags = st.sidebar.multiselect("Filter by Tags", all_tags)

# Product filtering
filtered_products = []
for p in PRODUCTS:
    if category != "All" and p["category"] != category:
        continue
    if search_query.lower() not in p["name"].lower():
        continue
    if selected_tags and not all(tag in p["tags"] for tag in selected_tags):
        continue
    filtered_products.append(p)

# Display function
def display_product(product, key_idx):
    st.markdown(f"<h4>{product['name']}</h4>", unsafe_allow_html=True)
    st.caption(f"Category: {product['category']}")
    if product.get("image"):
        st.image(product["image"], width=140)
    n = product.get("nutrition", {})
    if all(k in n and n[k] is not None for k in ["calories", "protein", "carbs", "fat"]):
        st.markdown(
            f"""
            <div style='display: flex; gap: 1rem; margin: 0.5rem 0; font-size: 15px;'>
                <div>🔥 <strong>Calories:</strong> {n['calories']} kcal</div>
                <div>💪 <strong>Protein:</strong> {n['protein']}g</div>
                <div>🍞 <strong>Carbs:</strong> {n['carbs']}g</div>
                <div>🧈 <strong>Fat:</strong> {n['fat']}g</div>
            </div>
            """, unsafe_allow_html=True)
    if product.get("tags"):
        tags_html = "".join([tag_html(tag) for tag in product["tags"]])
        st.markdown(f"<div style='margin-bottom: 0.5rem;'>Tags: {tags_html}</div>", unsafe_allow_html=True)

    b1, b2 = st.columns([1, 1])
    with b1:
        if st.button("🛒 Add to Cart", key=f"add_{key_idx}"):
            st.session_state.cart.append(product["name"])
            st.success(f"Added to cart: {product['name']}")
    with b2:
        if product["name"] in st.session_state.favorites:
            if st.button("⭐ Unfavorite", key=f"unfav_{key_idx}"):
                st.session_state.favorites.remove(product["name"])
                st.warning(f"Removed from favorites: {product['name']}")
        else:
            if st.button("⭐ Favorite", key=f"fav_{key_idx}"):
                st.session_state.favorites.append(product["name"])
                st.success(f"Added to favorites: {product['name']}")
    st.markdown("---")

# 2-column layout
for i in range(0, len(filtered_products), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(filtered_products):
            with cols[j]:
                display_product(filtered_products[i + j], key_idx=i + j)
