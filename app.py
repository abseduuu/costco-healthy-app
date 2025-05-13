import streamlit as st

# ----------------------------
# Mock Product Data (No Images)
# ----------------------------
PRODUCTS = [
    {
        "name": "Kirkland Organic Almond Butter",
        "store": "Costco",
        "diet": "High-Protein, Low-Carb",
        "category": "Snacks",
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
        "nutrition": {
            "calories": 170,
            "protein": 13,
            "carbs": 3,
            "fat": 12
        }
    },
    {
        "name": "Kirkland Hard-Boiled Eggs 2-Pack",
        "store": "Costco",
        "diet": "High-Protein, Low-Carb",
        "category": "Dairy",
        "nutrition": {
            "calories": 140,
            "protein": 12,
            "carbs": 1,
            "fat": 10
        }
    },
    {
        "name": "Good Culture Cottage Cheese, 2%",
        "store": "Costco",
        "diet": "High-Protein, Low-Carb",
        "category": "Dairy",
        "nutrition": {
            "calories": 110,
            "protein": 14,
            "carbs": 3,
            "fat": 4
        }
    },
    {
        "name": "Chomps Grass-Fed Beef Stick",
        "store": "Costco",
        "diet": "High-Protein, Low-Carb",
        "category": "Snacks",
        "nutrition": {
            "calories": 100,
            "protein": 9,
            "carbs": 0,
            "fat": 6
        }
    },
    {
        "name": "Nature’s Garden Keto Snack Mix",
        "store": "Costco",
        "diet": "High-Protein, Low-Carb",
        "category": "Snacks",
        "nutrition": {
            "calories": 180,
            "protein": 6,
            "carbs": 4,
            "fat": 16
        }
    },
    {
        "name": "Kirkland Signature Turkey Burgers",
        "store": "Costco",
        "diet": "High-Protein, Low-Carb",
        "category": "Frozen",
        "nutrition": {
            "calories": 200,
            "protein": 21,
            "carbs": 0,
            "fat": 12
        }
    },
    {
        "name": "Organic Blueberries (Fresh)",
        "store": "Costco",
        "diet": "High-Protein, Low-Carb",
        "category": "Fruit",
        "nutrition": {
            "calories": 80,
            "protein": 1,
            "carbs": 18,
            "fat": 0
        }
    }
]


# ----------------------------
# Session State for Cart & Favorites
# ----------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

if "favorites" not in st.session_state:
    st.session_state.favorites = []

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
        st.subheader(product["name"])
        st.write(f"**Category:** {product['category']}")
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
# View Cart with Removal + Totals
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
                continue  # Skip adding to updated_cart to remove
            updated_cart.append(item)
            for key in total_macros:
                total_macros[key] += product["nutrition"][key]
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
# View Favorites
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
import pandas as pd
import io

if updated_cart:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧾 Export Your Cart")

    # Build product + macro list
    cart_data = []
    for item in updated_cart:
        product = next((p for p in PRODUCTS if p["name"] == item), None)
        if product:
            cart_data.append({
                "Product": product["name"],
                **product["nutrition"]
            })

    df = pd.DataFrame(cart_data)

    # Show text list
    st.sidebar.text_area("Copy List:", "\n".join(updated_cart), height=150)

    # Download as CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.sidebar.download_button(
        label="⬇️ Download as CSV",
        data=csv_buffer.getvalue(),
        file_name="my_healthy_cart.csv",
        mime="text/csv"
    )

