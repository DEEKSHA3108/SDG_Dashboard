import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import warnings

warnings.filterwarnings("ignore")

# ---------------- Streamlit Config ----------------
st.set_page_config(page_title="SDG Dashboard", layout="wide")

# ------------- Load and Encode Logo -------------------
def get_image_base64(img_path):
    img = Image.open(img_path)
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode()

logo_base64 = get_image_base64("sdg_logo.jpeg")

def load_local_image_as_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo = load_local_image_as_base64("logo.png")

# ---------- Hide Streamlit default sidebar navigation ----------
hide_streamlit_style = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ------------------ Header ---------------------
st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 20px; padding: 1rem 0;">
        <img src="data:image/jpeg;base64,{logo_base64}" style="height: 80px; width: auto;" />
        <h1 style='font-size: 2.8rem; font-weight: 800; margin: 0; color: white;'>
            SDG Dashboard: Gender Inequality & Economic Growth
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------ Info Cards ---------------------
st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

info_card_style = """
    <div style='background-color: #F2F2F2; padding: 1.2rem; border-radius: 15px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1); text-align: center; height: 100%;'>
        <div style='font-size: 1.4rem; font-weight: 700; color: #333;'>{}</div>
        <div style='font-size: 1rem; color: #555; margin-top: 0.3rem;'>{}</div>
    </div>
"""

with col1:
    st.markdown(info_card_style.format("Goal 5 and Goal 8", "SDG Goals Involved"), unsafe_allow_html=True)
with col2:
    st.markdown(info_card_style.format("India and Germany", "Countries Involved"), unsafe_allow_html=True)
with col3:
    st.markdown(info_card_style.format("1995 to 2023", "Year Range"), unsafe_allow_html=True)

# ------------------ Sidebar Styling ------------------
# 

# ------------------ Sidebar Selectbox ------------------
st.sidebar.title("Menu")
side_bar_menu = st.sidebar.selectbox(
    "Choose Section",
    ["Introduction", "Data Gap Analysis", "EDA", "Forecasting Model"]
)
# ------------------ Conditional Sidebar Links ------------------
if side_bar_menu == "Introduction":
    st.sidebar.markdown("""
        <div class='sidebar-item white'>• Overview</div>
        <div class='sidebar-item white'>• About</div>
    """, unsafe_allow_html=True)

# ------------------ Fixed Logo Bottom Sidebar ------------------
with st.sidebar:
    st.markdown(
        f"""
        <style>
            .fixed-logo {{
                position: fixed;
                bottom: 20px;
                left: 8px;
                width: 240px;
                text-align: center;
            }}
            .fixed-logo img {{
                width: 90px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                border-radius: 8px;
            }}
            .fixed-logo p {{
                font-size: 12px;
                color: grey;
                margin-top: 6px;
            }}
        </style>

        <div class="fixed-logo">
            <img src="data:image/png;base64,{logo}">
            <p>University of Strathclyde</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------ Dynamic Page Renderer ------------------
try:
    if side_bar_menu == "Introduction":
        import introduction
        introduction.render()

    elif side_bar_menu == "Data Gap Analysis":
        import dataGap
        dataGap.render()

    elif side_bar_menu == "EDA":
        import eda
        eda.render()

    elif side_bar_menu == "Forecasting Model":
        import forcastingModel
        forcastingModel.render()

except AttributeError as e:
    st.error(f"Error loading page: `{e}`\nMake sure the `{side_bar_menu}` module has a `render()` function.")
except ModuleNotFoundError as e:
    st.error(f"Missing module: `{e}`. Ensure the file `{e.name}.py` exists in your project folder.")
