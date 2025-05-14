
import streamlit as st
import json

# ---------- Load Data ----------
with open('products_wholefoods_with_nutrition.json') as f:
    products = json.load(f)

# ---------- Config ----------
st.set_page_config(page_title="Doji Market", layout="wide")

# ---------- Header ----------
st.markdown("""
    <style>
    .header-title {
        font-size: 48px;
        font-weight: bold;
        font-family: 'Georgia', serif;
        padding-bottom: 20px;
    }
    .product-title {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .product-brand {
        font-size: 14px;
        font-style: italic;
        color: #666;
    }
    .product-price {
        font-size: 14px;
        font-weight: 500;
        margin-top: 2px;
        margin-bottom: 6px;
    }
    .product-tags {
        font-size: 12px;
        color: #aaa;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-title">Doji Market</div>', unsafe_allow_html=True)

# ---------- Filters ----------
categories = sorted(set([p.get("category", "Uncategorized") for p in products]))
selected_category = st.selectbox("Category", categories)

filtered = [p for p in products if p.get("category") == selected_category]

# ---------- Grid Display ----------
st.write("")  # space
columns = st.columns(3)

for idx, product in enumerate(filtered):
    col = columns[idx % 3]
    with col:
        st.image(product.get("image_url", ""), use_column_width=True)
        st.markdown(f"<div class='product-title'>{product['name']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='product-brand'>{product.get('brand', '')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='product-price'>${product['price']:.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='product-tags'>{', '.join(product.get('tags', []))}</div>", unsafe_allow_html=True)
