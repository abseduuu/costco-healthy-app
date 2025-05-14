
import streamlit as st
import pandas as pd
import json
import io

# Load data
with open("products_wholefoods_with_nutrition.json") as f:
    PRODUCTS = json.load(f)

# Tag generator
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

# Tag style
def tag_html(tag):
    return f"<span style='background-color:#e6f4ea; color:#2e7d32; padding:2px 8px; margin:2px; display:inline-block; border-radius:12px; font-size:13px'>{tag}</span>"

# Floating header
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

# Filter products
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

# Display in columns
for i in range(0, len(filtered_products), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(filtered_products):
            with cols[j]:
                display_product(filtered_products[i + j], key_idx=i + j)

# Sidebar Cart
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

# Sidebar Favorites
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
