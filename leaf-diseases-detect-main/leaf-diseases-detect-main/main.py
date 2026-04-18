import streamlit as st
import requests

# -------- PAGE CONFIG --------
st.set_page_config(
    page_title="Leaf AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------- FULL CSS --------
st.markdown("""
<style>

/* GLOBAL */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background: #f6f8fb;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

/* CONTAINER */
.main-container {
    max-width: 1100px;
    margin: auto;
    width: 100%;
}

/* HEADER */
.header {
    text-align: center;
    margin: 2rem 0 2.5rem 0;
}

.subheader {
    display:flex;
    align-items:center;
    justify-content:center;
    gap:10px;
}

.header h1 {
    font-size: 2.4rem;
    font-weight: 600;
    margin: 0;
    color: #111827;
}

.header p {
    color: #6b7280;
    font-size: 1rem;
    margin-top: 6px;
}

/* CARD */
.card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(8px);
    padding: 1.6rem;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    transition: all 0.2s ease;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(0,0,0,0.10);
}

/* BUTTON */
.stButton>button {
    width: 100%;
    height: 46px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 500;
    background: #16a34a;
    color: white;
    border: none;
    transition: all 0.2s ease;
}

.stButton>button:hover {
    background: #15803d;
    transform: translateY(-1px);
}

/* TITLE */
.title {
    font-size: 1.4rem;
    font-weight: 600;
    color: #111827;
}

/* SECTION */
.section {
    margin-top: 1.3rem;
}

.section h4 {
    font-size: 0.85rem;
    color: #16a34a;
    margin-bottom: 6px;
    font-weight: 600;
    letter-spacing: 0.4px;
    text-transform: uppercase;
}

/* BADGE */
.badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: #f0fdf4;
    color: #166534;
    font-size: 12px;
    margin-right: 6px;
    margin-top: 6px;
}

/* LIST */
ul, li {
    color: #374151;
    font-size: 14px;
}

/* IMAGE */
img {
    border-radius: 12px;
    margin-top: 10px;
}

/* CAPTION */
.caption {
    font-size: 13px;
    color: #6b7280;
    margin-top: 8px;
}

/* DIVIDER */
.divider {
    height: 1px;
    background: #e5e7eb;
    margin: 14px 0;
}

/* FOOTER */
.footer {
    margin-top: auto;
    padding: 1.5rem 0;
    border-top: 1px solid #e5e7eb;
    text-align: center;
    color: #6b7280;
    font-size: 13px;
}

.sub-footer {
    display:flex;
    justify-content:center;
    align-items:center;
    gap:8px;
}

.footer-links {
    margin-top: 8px;
}

.footer-links a {
    color: #6b7280;
    text-decoration: none;
    margin: 0 10px;
    transition: 0.2s;
}

.footer-links a:hover {
    color: #16a34a;
}

/* MOBILE */
@media(max-width: 768px){
    .header h1 {
        font-size: 1.8rem;
    }
}

</style>
""", unsafe_allow_html=True)

# -------- HEADER --------
st.markdown("""
<div class="header">
    <div class="subheader">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
            <path d="M5 21C5 10 12 3 21 3C21 12 14 21 5 21Z"
                  stroke="#16a34a" stroke-width="2"/>
            <path d="M5 21C9 17 13 13 21 3"
                  stroke="#16a34a" stroke-width="2"/>
        </svg>
        <h1>Leaf AI</h1>
    </div>
    <p>Smart plant disease detection powered by AI</p>
</div>
""", unsafe_allow_html=True)

# -------- API --------
api_url = "http://leaf-diseases-detect.vercel.app"

st.markdown('<div class="main-container">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

# -------- UPLOAD --------
with col1:
    container = st.container()

    with container:
        st.markdown('<div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload Leaf Image",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )

        st.markdown('<div class="caption">Upload a clear leaf image</div>', unsafe_allow_html=True)

        if uploaded_file:
            st.image(uploaded_file, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

# -------- PROCESS --------
with col2:
    if uploaded_file:
        if st.button("Analyze Leaf"):
            with st.spinner("Analyzing leaf health..."):
                try:
                    files = {
                        "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                    }

                    response = requests.post(
                        f"{api_url}/disease-detection-file",
                        files=files
                    )

                    if response.status_code == 200:
                        result = response.json()

                        st.markdown('<div>', unsafe_allow_html=True)

                        # INVALID
                        if result.get("disease_type") == "invalid_image":
                            st.markdown('<div class="title">⚠️ Invalid Image</div>', unsafe_allow_html=True)
                            st.write("Upload a proper leaf image.")

                        # DISEASE
                        elif result.get("disease_detected"):
                            st.markdown(
                                f'<div class="title">🦠 {result.get("disease_name")}</div>',
                                unsafe_allow_html=True
                            )

                            st.markdown(
                                f'<div class="badge">{result.get("disease_type")}</div>'
                                f'<div class="badge">Severity: {result.get("severity")}</div>'
                                f'<div class="badge">Confidence: {result.get("confidence")}%</div>',
                                unsafe_allow_html=True
                            )

                            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

                            st.markdown('<div class="section"><h4>Symptoms</h4></div>', unsafe_allow_html=True)
                            for s in result.get("symptoms", []):
                                st.write(f"• {s}")

                            st.markdown('<div class="section"><h4>Causes</h4></div>', unsafe_allow_html=True)
                            for c in result.get("possible_causes", []):
                                st.write(f"• {c}")

                            st.markdown('<div class="section"><h4>Treatment</h4></div>', unsafe_allow_html=True)
                            for t in result.get("treatment", []):
                                st.write(f"• {t}")

                        # HEALTHY
                        else:
                            st.markdown('<div class="title">✅ Healthy Leaf</div>', unsafe_allow_html=True)
                            st.success("No disease detected")

                        st.markdown('</div>', unsafe_allow_html=True)

                    else:
                        st.error(f"API Error: {response.status_code}")

                except Exception as e:
                    st.error(str(e))

st.markdown('</div>', unsafe_allow_html=True)

# -------- FOOTER --------
st.markdown("""
<div class="footer">
    <div class="sub-footer">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path d="M5 21C5 10 12 3 21 3C21 12 14 21 5 21Z"
                  stroke="#16a34a" stroke-width="2"/>
            <path d="M5 21C9 17 13 13 21 3"
                  stroke="#16a34a" stroke-width="2"/>
        </svg>
        <span>Leaf AI</span>
    </div>
    <div style="margin-top:6px;">
        © 2026 Leaf AI. All rights reserved.
    </div>
    <div class="footer-links">
        <a href="#">Privacy</a>
        <a href="#">Terms</a>
        <a href="#">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)