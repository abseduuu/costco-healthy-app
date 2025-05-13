import streamlit as st
import pandas as pd
import io

# ----------------------------
# Mock Product Data
# ----------------------------
PRODUCTS = [
    {
        "name": "Kirkland Organic Almond Butter",
        "store": "Costco",
        "diet": ["High-Protein, Low-Carb", "Keto"],
        "category": "Snacks",
        "nutrition": {"calories": 190, "protein": 7, "carbs": 6, "fat": 16}
    },
    {
        "name": "Thai Kitchen Organic Coconut Milk",
        "store": "Costco",
        "diet": ["High-Protein, Low-Carb", "Keto", "Gluten-Free"],
        "category": "Pantry",
        "nutrition": {"calories": 120, "protein": 1, "carbs": 2, "fat": 12}
    },
    {
        "name": "Aidells Chicken & Apple Sausage",
        "store": "Costco",
        "diet": ["High-Protein, Low-Carb", "Gluten-Free"],
        "category": "Meat",
        "nutrition": {"calories": 170, "protein": 13, "carbs": 3, "fat": 12}
    },
    {
        "name": "Kirkland Hard-Boiled Eggs 2-Pack",
        "store": "Costco",
        "diet": ["High-Protein, Low-Carb", "Keto", "Gluten-Free"],
        "category": "Dairy",
        "nutrition": {"calories": 140, "protein": 12, "carbs": 1, "fat": 10}
    },
    {
        "name": "Good Culture Cottage Cheese, 2%",
        "store": "Costco",
        "diet": ["High-Protein, Low-Carb", "Gluten-Free"],
        "category": "Dairy",
        "nutrition": {"calories": 110, "protein": 14, "carbs": 3, "fat": 4}
    },
    {
        "name": "Chomps Grass-Fed Beef Stick",
        "store": "Costco",
        "diet": ["High-Protein, Low-Carb", "Keto", "Gluten-Free"],
        "category": "Snacks",
        "nutrition": {"calories": 100, "protein": 9, "carbs": 0, "fat": 6}
    },
    {
        "name": "Nature’s Garden Keto Snack Mix",
        "store": "Costco",
        "diet": ["High-Protein, Low-Carb", "Keto"],
        "category": "Snacks",
        "nutrition": {"calories": 180, "protein": 6, "carbs": 4, "fat": 16}
    },
    {
        "name": "Kirkland Signature Turkey Burgers",
        "store": "Costco",
        "diet": ["High-Protein, Low-Carb", "Keto", "Gluten-Free"],
        "category": "Frozen",
        "nutrition": {"calories": 200, "protein": 21, "carbs": 0, "fat": 12}
    },
    {
        "name": "Organic Blueberries (Fresh)",
        "store": "Costco",
        "diet": ["Gluten-Free"],
        "category": "Fruit",
        "nutrition": {"calories": 80, "protein": 1, "carbs": 18, "fat": 0}
    },
    {
        "name": "365 Organic Cage-Free Eggs",
        "store": "Whole Foods",
        "diet": ["High-Protein, Low-Carb", "Keto", "Gluten-Free"],
        "category": "Dairy",
        "nutrition": {"calories": 70, "protein": 6, "carbs": 0, "fat": 5}
    },
    {
        "name": "365 Almond Flour Crackers",
        "store": "Whole Foods",
        "diet": ["High-Protein, Low-Carb", "Keto"],
        "category": "Snacks",
        "nutrition": {"calories": 150, "protein": 5, "carbs": 8, "fat": 12}
    },
    {
        "name": "Whole Foods Organic Chicken Breast",
        "store": "Whole Foods",
        "diet": ["High-Protein, Low-Carb", "Keto", "Gluten-Free"],
        "category": "Meat",
        "nutrition": {"calories": 140, "protein": 26, "carbs": 0, "fat": 3}
    }
]

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
store_options = sorted(list(set(p["store"] for p in PRODUCTS)))
store = st.sidebar.selectbox("Where are you shopping?", store_options)

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
    if p["store"] == store
    and diet in p["diet"]
    and (category == "All" or p["category"] == category)
    and (search_query.lower() in p["name"].lower())
]

# ----------------------------
# Main Content
# ----------------------------
st.title("🥦 Healthy Grocery Finder")

for product in filtered_products:
    with st.container():
        st.subheader(product["name"])
        st.write(f"**Store:** {product['store']}  |  **Category:** {product['category']}")
        st.write("**Diet Tags:**", ", ".join(product["diet"]))
        st.write("**Nutrition per serving:**")
        st.write(product["nutrition"])

        if st.button(f"Add to Cart: {product['name']}"):
            st.session_state.cart.append(product["name"])
            st.success(f"Added to cart: {product['name']}")

        if product["name"] in st.session_state.favorites:
            if st.button(f"Unfavorite: {product['name']}"):
                st.session_state.favorites.remove(product["name"])
                st.warning(f"Removed from favorites: {product['name']}")
        else:
            if st.button(f"⭐ Favorite: {product['name']}"):
                st.session_state.favorites.append(product["name"])
                st.success(f"Added to favorites: {product['name']}")

        st.markdown("---")

# ----------------------------
# Cart and Favorites in Sidebar
# ----------------------------
st.sidebar.header("🛒 Your Cart")
total_macros = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
updated_cart = []

if st.session_state.cart:
    for item in st.session_state.cart:
        product = next((p for p in PRODUCTS if p["name"] == item), None)
        if product:
            st.sidebar.write(f"**{item}**")
            if st.sidebar.button(f"Remove {item}"):
                continue
            updated_cart.append(item)
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
