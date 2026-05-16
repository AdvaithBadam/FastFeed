import streamlit as st
import requests
import base64
import urllib.parse
import os
from datetime import datetime

st.set_page_config(page_title="FastFeed", page_icon="◆", layout="wide", initial_sidebar_state="collapsed")

# ── API URL ──
API_URL = os.getenv("API_URL", "https://fastfeed.onrender.com")

# ── Session State ──
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'upload_key' not in st.session_state:
    st.session_state.upload_key = 0


# ── Premium CSS Injection ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Global ── */
.stApp {
    background-color: #0D0D0D;
    font-family: 'Inter', sans-serif;
}
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #E8E6E3;
}

/* ── Hide Streamlit chrome ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="manage-app-button"] {display: none !important;}
.viewerBadge_container__r5tak {display: none !important;}
/* Hide toolbar action buttons but keep the running indicator */
[data-testid="stToolbar"] {
    visibility: visible !important;
}
[data-testid="stToolbar"] button,
[data-testid="stToolbar"] a,
[data-testid="stToolbar"] [data-testid="stActionButton"] {
    display: none !important;
}
[data-testid="stStatusWidget"] {
    visibility: visible !important;
}
[data-testid="stStatusWidget"] [role="status"] {
    color: #E63946 !important;
}
/* Custom visible spinner override */
.stSpinner {
    text-align: center;
    padding: 16px 0;
}
.stSpinner > div {
    border-top-color: #E63946 !important;
}
.stSpinner > div > span {
    color: #888 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
}
header[data-testid="stHeader"] {
    background: rgba(13,13,13,0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid #1A1A1A;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #111111;
    border-right: 1px solid #1A1A1A;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] .stMarkdown li {
    color: #C8C5C0;
    font-family: 'Inter', sans-serif;
}
section[data-testid="stSidebar"] .stRadio label span {
    color: #C8C5C0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}
section[data-testid="stSidebar"] .stRadio label:hover span {
    color: #F0EDE8 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: #222 !important;
}

/* ── Text inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: #161616 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 2px !important;
    color: #E8E6E3 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    transition: border-color 0.2s ease;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #E63946 !important;
    box-shadow: none !important;
}
.stTextInput label, .stTextArea label {
    color: #888 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* ── Buttons ── */
.stButton > button {
    background-color: transparent !important;
    border: 1px solid #333 !important;
    border-radius: 2px !important;
    color: #C8C5C0 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    letter-spacing: 0.04em !important;
    padding: 8px 20px !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    border-color: #E63946 !important;
    color: #E63946 !important;
    background-color: rgba(230,57,70,0.06) !important;
}
.stButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"] {
    background-color: #E63946 !important;
    border: 1px solid #E63946 !important;
    color: #fff !important;
}
button[data-testid="stBaseButton-primary"]:hover {
    background-color: #c7303c !important;
    border-color: #c7303c !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background-color: #161616;
    border: 1px dashed #2A2A2A;
    border-radius: 2px;
    padding: 16px;
}
[data-testid="stFileUploader"] label {
    color: #888 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
[data-testid="stFileUploader"] button {
    background-color: #1A1A1A !important;
    border: 1px solid #333 !important;
    border-radius: 2px !important;
    color: #C8C5C0 !important;
}

/* ── Custom post card ── */
div.post-card {
    background: #161616;
    border: 1px solid #1E1E1E;
    border-left: 3px solid transparent;
    border-radius: 2px;
    padding: 20px 24px;
    margin-bottom: 2px;
    transition: all 0.15s ease;
}
div.post-card:hover {
    background: #1A1A1A;
    border-left-color: #E63946;
}
div.post-card .post-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}
div.post-card .post-user {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: #F0EDE8;
    letter-spacing: 0.02em;
}
div.post-card .post-time {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    color: #666;
    letter-spacing: 0.04em;
}
div.post-card .post-caption {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 16px;
    font-weight: 400;
    color: #D5D2CD;
    line-height: 1.5;
    margin-top: 14px;
}
div.post-card .post-dot {
    display: inline-block;
    width: 3px;
    height: 3px;
    border-radius: 50%;
    background: #444;
    margin: 0 10px;
    vertical-align: middle;
}

/* ── Divider ── */
div.feed-divider {
    border-top: 1px solid #1A1A1A;
    margin: 0;
}

/* ── Login page ── */
div.login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 80px 0 40px;
}
div.login-logo {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #F0EDE8;
    text-align: center;
    margin-bottom: 8px;
}
div.login-logo span {
    color: #E63946;
}
div.login-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    color: #555;
    text-align: center;
    margin-bottom: 48px;
    letter-spacing: 0.02em;
}
div.login-accent-line {
    width: 40px;
    height: 2px;
    background: #E63946;
    margin: 0 auto 24px;
}

/* ── Feed header ── */
div.feed-header {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #555;
    padding: 20px 0 16px;
    border-bottom: 1px solid #1A1A1A;
    margin-bottom: 2px;
}

/* ── Upload section ── */
div.upload-header {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 28px;
    font-weight: 500;
    color: #F0EDE8;
    margin-bottom: 8px;
}
div.upload-sub {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    color: #555;
    margin-bottom: 32px;
}

/* ── Top branding bar ── */
div.brand-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #1A1A1A;
    margin-bottom: 0;
}
div.brand-logo {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #F0EDE8;
}
div.brand-logo span {
    color: #E63946;
}
div.brand-tagline {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    color: #444;
    letter-spacing: 0.06em;
}

/* ── Empty state ── */
div.empty-state {
    text-align: center;
    padding: 80px 20px;
    color: #444;
}
div.empty-state .empty-icon {
    font-size: 48px;
    margin-bottom: 16px;
    opacity: 0.3;
}
div.empty-state .empty-text {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    color: #555;
}

/* ── Success/error banners ── */
.stSuccess, .stInfo, .stError, .stWarning {
    border-radius: 2px !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Image/video containers ── */
.stImage, .stVideo {
    border-radius: 2px;
    overflow: hidden;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #E63946 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0D0D0D; }
::-webkit-scrollbar-thumb { background: #2A2A2A; border-radius: 2px; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1px solid #1A1A1A;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #555 !important;
    border-radius: 0 !important;
    padding: 12px 24px !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #F0EDE8 !important;
    border-bottom: 2px solid #E63946 !important;
}

/* ── Column gaps ── */
[data-testid="stHorizontalBlock"] {
    gap: 2px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──
def get_headers():
    """Get authorization headers with token"""
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def encode_text_for_overlay(text):
    """Encode text for ImageKit overlay - base64 then URL encode"""
    if not text:
        return ""
    base64_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    return urllib.parse.quote(base64_text)


def create_transformed_url(original_url, transformation_params, caption=None):
    if caption:
        encoded_caption = encode_text_for_overlay(caption)
        text_overlay = f"l-text,ie-{encoded_caption},ly-N20,lx-20,fs-100,co-white,bg-000000A0,l-end"
        transformation_params = text_overlay

    if not transformation_params:
        return original_url

    parts = original_url.split("/")

    if len(parts) < 5:
        return original_url

    imagekit_id = parts[3]
    file_path = "/".join(parts[4:])
    base_url = "/".join(parts[:4])
    return f"{base_url}/tr:{transformation_params}/{file_path}"


def format_time(iso_string):
    """Format ISO timestamp to a relative or short readable time."""
    try:
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.utcnow()
        diff = now - dt
        if diff.days > 0:
            return dt.strftime("%b %d, %Y")
        hours = diff.seconds // 3600
        if hours > 0:
            return f"{hours}h ago"
        minutes = diff.seconds // 60
        if minutes > 0:
            return f"{minutes}m ago"
        return "Just now"
    except Exception:
        return iso_string[:10] if iso_string else ""


# ── Login Page ──
def login_page():
    # Center the login form
    _, center, _ = st.columns([1.2, 1, 1.2])
    with center:
        st.markdown("""
        <div class="login-container">
            <div class="login-logo">FAST<span>FEED</span></div>
            <div class="login-accent-line"></div>
            <div class="login-subtitle">Share moments. See the world.</div>
        </div>
        """, unsafe_allow_html=True)

        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")

        if email and password:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Login", type="primary", use_container_width=True):
                    login_data = {"username": email, "password": password}
                    response = requests.post(f"{API_URL}/auth/jwt/login", data=login_data)
                    if response.status_code == 200:
                        token_data = response.json()
                        st.session_state.token = token_data["access_token"]
                        user_response = requests.get(f"{API_URL}/users/me", headers=get_headers())
                        if user_response.status_code == 200:
                            st.session_state.user = user_response.json()
                            st.rerun()
                        else:
                            st.error("Failed to get user info")
                    else:
                        st.error("Invalid email or password")
            with col2:
                if st.button("Sign Up", use_container_width=True):
                    signup_data = {"email": email, "password": password}
                    response = requests.post(f"{API_URL}/auth/register", json=signup_data)
                    if response.status_code == 201:
                        st.success("Account created — now log in.")
                    else:
                        error_detail = response.json().get("detail", "Registration failed")
                        st.error(f"{error_detail}")
        else:
            st.markdown(
                "<p style='text-align:center;color:#444;font-size:12px;margin-top:24px;'>"
                "Enter credentials to continue</p>",
                unsafe_allow_html=True,
            )


# ── Upload Page ──
def upload_page():
    st.markdown("""
    <div class="upload-header">Share Something</div>
    <div class="upload-sub">Photos and videos, shared with everyone.</div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose media",
        type=['png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov', 'mkv', 'webm'],
        key=f"uploader_{st.session_state.upload_key}",
    )
    caption = st.text_area(
        "Caption",
        placeholder="What's on your mind?",
        key=f"caption_{st.session_state.upload_key}",
    )

    if uploaded_file and st.button("Share", type="primary"):
        with st.spinner("Uploading…"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {"caption": caption}
            response = requests.post(f"{API_URL}/upload", files=files, data=data, headers=get_headers())
            if response.status_code == 200:
                st.success("Posted!")
                st.session_state.upload_key += 1
                st.rerun()
            else:
                st.error("Upload failed")


# ── Feed Page ──
def feed_page():
    # Top branding bar
    st.markdown("""
    <div class="brand-bar">
        <div class="brand-logo">FAST<span>FEED</span></div>
        <div class="brand-tagline">YOUR FEED</div>
    </div>
    """, unsafe_allow_html=True)

    response = requests.get(f"{API_URL}/feed", headers=get_headers())
    if response.status_code != 200:
        st.error("Failed to load feed")
        return

    posts = response.json()["posts"]

    if not posts:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">◇</div>
            <div class="empty-text">No posts yet — be the first to share something.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f'<div class="feed-header">{len(posts)} POST{"S" if len(posts) != 1 else ""}</div>',
                unsafe_allow_html=True)

    # ── Render posts in 2-column grid ──
    col_count = 2
    for row_start in range(0, len(posts), col_count):
        cols = st.columns(col_count)
        for i, col in enumerate(cols):
            idx = row_start + i
            if idx >= len(posts):
                break
            post = posts[idx]

            with col:
                # Post card header
                user_email = post.get("email", "Unknown")
                display_name = user_email.split("@")[0]
                time_str = format_time(post.get("created_at", ""))
                caption = post.get("caption", "")

                st.markdown(f"""
                <div class="post-card">
                    <div class="post-header">
                        <span class="post-user">{display_name}</span>
                        <span class="post-time">{time_str}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Media
                if post['file_type'] == 'image':
                    uniform_url = create_transformed_url(post['url'], "")
                    st.image(uniform_url, use_container_width=True)
                else:
                    uniform_video_url = create_transformed_url(
                        post['url'], "w-400,h-200,cm-pad_resize,bg-blurred"
                    )
                    st.video(uniform_video_url)

                # Caption
                if caption:
                    st.markdown(
                        f'<div class="post-card"><div class="post-caption">{caption}</div></div>',
                        unsafe_allow_html=True,
                    )

                # Delete button (only for post owner)
                if post.get('is_owner', False):
                    if st.button("✕ Delete", key=f"delete_{post['id']}"):
                        del_resp = requests.delete(
                            f"{API_URL}/posts/{post['id']}", headers=get_headers()
                        )
                        if del_resp.status_code == 200:
                            st.success("Deleted")
                            st.rerun()
                        else:
                            st.error("Failed to delete")

                # Divider between posts
                st.markdown('<div class="feed-divider"></div>', unsafe_allow_html=True)
                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)


# ── Main App Logic ──
if st.session_state.user is None:
    login_page()
else:
    # Sidebar
    with st.sidebar:
        user_email = st.session_state.user.get("email", "")
        display_name = user_email.split("@")[0]
        st.markdown(
            f"<div style='font-family:Inter,sans-serif;font-size:13px;color:#888;"
            f"letter-spacing:0.06em;text-transform:uppercase;padding:8px 0 4px;'>"
            f"Signed in as</div>"
            f"<div style='font-family:Inter,sans-serif;font-size:16px;font-weight:600;"
            f"color:#F0EDE8;padding-bottom:16px;'>{display_name}</div>",
            unsafe_allow_html=True,
        )

        if st.button("Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.token = None
            st.rerun()

        st.markdown("---")

    # Tab-based navigation
    tab_feed, tab_upload = st.tabs(["FEED", "SHARE"])

    with tab_feed:
        feed_page()

    with tab_upload:
        upload_page()