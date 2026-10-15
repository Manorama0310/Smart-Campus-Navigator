import math
import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation

from campus_data import LOCATIONS, EDGES, CAMPUS_OPTIONS
from algorithms import dijkstra, bfs_path, dfs_path
from trie import Trie

st.set_page_config(page_title="CampusGo | Campus Navigator", page_icon="🧭", layout="wide", initial_sidebar_state="expanded")

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp, [data-testid="stAppViewContainer"] { background: #f6f8fc; color: #152238; }
[data-testid="stHeader"] { background: rgba(246,248,252,0.96); }
.block-container { padding-top: 1.3rem; padding-bottom: 2rem; max-width: 1440px; }
/* Force readable text regardless of the browser/Streamlit theme. */
.stApp, .stApp p, .stApp label, .stApp li, .stApp span, .stApp small,
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
[data-testid="stCaptionContainer"] p, [data-testid="stWidgetLabel"] p,
[data-testid="stRadio"] label, [data-testid="stCheckbox"] label { color: #152238; }
[data-testid="stSidebar"] , [data-testid="stSidebar"] > div { background: #edf3fa !important; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span,
[data-testid="stSidebar"] label, [data-testid="stSidebar"] small,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { color: #18304b !important; }
[data-testid="stBaseButton-secondary"], div.stButton > button { color: #17304b !important; background: #ffffff !important; border: 1px solid #cbd8e8 !important; }
div.stButton > button[kind="primary"], [data-testid="stBaseButton-primary"] { color: #ffffff !important; background: #087e8b !important; border: 1px solid #087e8b !important; }
[data-testid="stTextInput"] input, [data-testid="stSelectbox"] div[data-baseweb="select"] > div { color: #152238 !important; background: #ffffff !important; border-color: #cbd8e8 !important; }
[data-testid="stTextInput"] input::placeholder { color: #64748b !important; opacity: 1; }
[data-testid="stAlert"] p { color: #18304b !important; }
.hero { background: linear-gradient(120deg,#10233f 0%,#174b69 58%,#087e8b 100%); padding: 1.8rem 2rem; border-radius: 24px; color: white; margin-bottom: 1.2rem; box-shadow: 0 12px 32px rgba(16,35,63,.15); }
.hero h1 { color: white; font-family: 'Manrope',sans-serif; font-size: clamp(2rem,4vw,3rem); margin: 0; letter-spacing: -1.5px; }
.hero p { color: #d9edf4; font-size: 1.03rem; margin: .55rem 0 0; }
.eyebrow { color:#a7f3e6; text-transform:uppercase; letter-spacing:2px; font-size:.72rem; font-weight:800; margin-bottom:.45rem; }
.section-title { font-family:'Manrope',sans-serif; font-weight:800; color:#142a43; font-size:1.45rem; margin:.2rem 0 .8rem; }
.mini-card { background:white; border:1px solid #e5eaf2; border-radius:18px; padding:1rem 1.1rem; min-height:108px; box-shadow:0 4px 16px rgba(22,43,72,.035); }
.mini-label { color:#6a7a90; font-size:.82rem; font-weight:600; }
.mini-value { color:#142a43; font-family:'Manrope',sans-serif; font-size:1.25rem; font-weight:800; margin-top:.35rem; }
.mini-sub { color:#8491a3; font-size:.78rem; margin-top:.15rem; }
.panel { background:white; border:1px solid #e5eaf2; border-radius:20px; padding:1.1rem 1.2rem; }
.route-step { padding:.65rem .8rem; border:1px solid #e8edf4; border-radius:12px; margin:.35rem 0; background:#fbfcfe; }
.small-muted { color:#6a7a90; font-size:.85rem; }
div.stButton > button { border-radius:12px; font-weight:700; min-height:2.8rem; }
[data-testid="stSidebar"] { background:#eef3f9; border-right:1px solid #e2e8f0; }
[data-testid="stMetric"] { background:white; padding:1rem; border:1px solid #e5eaf2; border-radius:16px; }
</style>
""", unsafe_allow_html=True)

# ---------- Graph helpers ----------
def build_graph(edges):
    graph = {name: {} for name in LOCATIONS}
    for a, b, distance in edges:
        graph[a][b] = distance
        graph[b][a] = distance
    return graph

graph = build_graph(EDGES)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🧭 CampusGo")
    st.caption("Find your way around campus")
    campus = st.selectbox("Your campus", CAMPUS_OPTIONS, index=0)
    st.markdown("---")
    page = st.radio("Navigate", ["Home & directions", "Live location", "Places directory"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Quick tips**")
    st.caption("📍 Allow location permission for your current position.")
    st.caption("🗺️ Walking routes depend on verified campus pathways.")
    st.caption("🔒 Your browser location is requested only when you open Live location.")

# ---------- Hero ----------
st.markdown(f"""
<div class="hero">
  <div class="eyebrow">YOUR CAMPUS, MADE SIMPLE</div>
  <h1>Find your way. Get there faster.</h1>
  <p>Search campus places, compare routes, and make every campus visit easier.</p>
</div>
""", unsafe_allow_html=True)
if campus != CAMPUS_OPTIONS[0]:
    st.info("Campus profile selected. Campus-specific building coordinates and verified walking paths still need to be added before these routes can be used as real directions.")

# Shared location permission helper
def get_location():
    try:
        return streamlit_geolocation()
    except Exception as exc:
        st.error("Location service could not start. Check the app dependencies and reload.")
        st.caption(str(exc))
        return None

if page == "Home & directions":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="mini-card"><div class="mini-label">📍 Campus selected</div><div class="mini-value">'+campus+'</div><div class="mini-sub">Change campus from the sidebar</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="mini-card"><div class="mini-label">🏫 Listed places</div><div class="mini-value">'+str(len(LOCATIONS))+' locations</div><div class="mini-sub">Campus directory</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="mini-card"><div class="mini-label">🧠 Route engine</div><div class="mini-value">Dijkstra</div><div class="mini-sub">Minimum distance on mapped paths</div></div>', unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1.05, 1], gap="large")
    with left:
        st.markdown('<div class="section-title">Where do you want to go?</div>', unsafe_allow_html=True)
        search_text = st.text_input("Search a place", placeholder="Try: library, lab, canteen…", label_visibility="collapsed")
        trie = Trie()
        for place in LOCATIONS:
            trie.insert(place)
        if search_text.strip():
            suggestions = trie.starts_with(search_text.strip())
            suggestions = [p for p in LOCATIONS if p.lower().startswith(search_text.strip().lower())]
            if suggestions:
                st.caption("Suggestions: " + " · ".join(suggestions[:5]))
            else:
                st.caption("No matching place yet. Try a different name.")
        c1, c2 = st.columns(2)
        with c1:
            start = st.selectbox("Starting point", LOCATIONS, index=0)
        with c2:
            quick_target = st.session_state.get("quick_target")
            target_default = LOCATIONS.index(quick_target) if quick_target in LOCATIONS else (LOCATIONS.index("Computer Lab") if "Computer Lab" in LOCATIONS else min(1, len(LOCATIONS)-1))
            target = st.selectbox("Destination", LOCATIONS, index=target_default)
        algorithm = st.selectbox("Route preference", ["Shortest walking distance", "Fewest path segments (BFS)", "Explore first available path (DFS)"])
        if st.button("✨ Find my route", type="primary", use_container_width=True):
            if start == target:
                st.info("You're already at your selected destination.")
                st.session_state["route_result"] = ( [start], 0, algorithm )
            elif algorithm == "Shortest walking distance":
                path, distance = dijkstra(graph, start, target)
                st.session_state["route_result"] = (path, distance, algorithm)
            elif algorithm.startswith("Fewest"):
                path = bfs_path(graph, start, target)
                st.session_state["route_result"] = (path, None, algorithm)
            else:
                path = dfs_path(graph, start, target)
                st.session_state["route_result"] = (path, None, algorithm)

        result = st.session_state.get("route_result")
        if result:
            path, distance, chosen_algorithm = result
            st.markdown("#### Your route")
            if path:
                st.success("Route found · " + str(len(path)-1) + " path segment(s)")
                if distance is not None:
                    a, b = st.columns(2)
                    a.metric("Mapped distance", f"{distance} m")
                    b.metric("Estimated walk", f"{max(1, round(distance/80))} min", help="Rough estimate at 80 metres/minute; actual time varies.")
                for i, place in enumerate(path):
                    st.markdown(f'<div class="route-step"><b>{i+1:02d}</b> &nbsp; {place}</div>', unsafe_allow_html=True)
                if distance is None:
                    st.caption("BFS/DFS shows a path, not necessarily the shortest physical distance.")
            else:
                st.warning("No connected path was found between these places in the current campus graph.")
        st.caption("Route distances use the campus graph configured in the project. Verify campus paths and distances before real-world use.")

    with right:
        st.markdown('<div class="section-title">Campus at a glance</div>', unsafe_allow_html=True)
        st.markdown("**Popular destinations**")
        popular = [p for p in ["Central Library", "Computer Lab", "Canteen", "Admin Block"] if p in LOCATIONS]
        cards = st.columns(2)
        icons = {"Central Library":"📚", "Computer Lab":"💻", "Canteen":"☕", "Admin Block":"🏢"}
        for i, place in enumerate(popular):
            with cards[i % 2]:
                if st.button(f"{icons.get(place,'📍')}  {place}", key="popular_"+place, use_container_width=True):
                    st.session_state["quick_target"] = place
                    st.session_state["route_result"] = None
                    st.rerun()
        if st.session_state.get("quick_target") in LOCATIONS:
            st.info(f"Quick destination selected: {st.session_state['quick_target']}. Press **Find my route** to calculate the route.")
        st.markdown("---")
        st.markdown("**How routing works**")
        st.write("Campus places are graph nodes. Walkable connections are weighted edges. Dijkstra checks these connections to find the minimum-distance route.")
        st.write("")
        st.info("Multi-campus ready: campus names can be added in `campus_data.py`. Each campus needs its own verified destinations and path data.")

elif page == "Live location":
    st.markdown('<div class="section-title">Your live location</div>', unsafe_allow_html=True)
    st.write("Allow your browser to share your location. The map uses OpenStreetMap tiles. Location access requires HTTPS on the deployed app, or localhost during development.")
    location = get_location()
    if location and location.get("latitude") is not None and location.get("longitude") is not None:
        lat, lon = float(location["latitude"]), float(location["longitude"])
        accuracy = location.get("accuracy")
        m1, m2, m3 = st.columns(3)
        m1.metric("Latitude", f"{lat:.6f}")
        m2.metric("Longitude", f"{lon:.6f}")
        m3.metric("Reported accuracy", f"±{round(float(accuracy))} m" if accuracy else "Not provided")
        map_obj = folium.Map(location=[lat, lon], zoom_start=17, tiles="OpenStreetMap", control_scale=True)
        folium.CircleMarker([lat, lon], radius=9, color="#087e8b", fill=True, fill_color="#16c7b7", fill_opacity=0.95, tooltip="Your current location").add_to(map_obj)
        folium.Marker([lat, lon], tooltip="You are here", icon=folium.Icon(color="blue", icon="user", prefix="fa")).add_to(map_obj)
        st_folium(map_obj, use_container_width=True, height=500, returned_objects=[])
        st.caption("Your coordinates are displayed in this session. This app does not store or send them to a custom server.")
    else:
        st.warning("Location not available yet. Allow location access in the browser prompt, then wait a moment or refresh this page.")
        st.caption("If you are on a desktop, location accuracy may be approximate and based on Wi-Fi/IP rather than GPS satellites.")
    st.markdown("#### What live location can and cannot do")
    c1, c2 = st.columns(2)
    c1.success("Can show your current browser-reported location on an outdoor map.")
    c2.warning("Does not automatically know campus buildings, indoor corridors, stairs, or safe walking paths.")
    st.markdown("To enable true campus-to-building routing, add verified coordinates for every destination and mapped pedestrian paths for this campus.")

else:  # Places directory
    st.markdown('<div class="section-title">Explore campus places</div>', unsafe_allow_html=True)
    query = st.text_input("Filter places", placeholder="Type a place name…")
    filtered = [p for p in sorted(LOCATIONS, key=str.casefold) if query.lower() in p.lower()]
    if filtered:
        cols = st.columns(2)
        for idx, place in enumerate(filtered):
            with cols[idx % 2]:
                st.markdown(f'<div class="mini-card"><div class="mini-label">CAMPUS PLACE</div><div class="mini-value">📍 {place}</div><div class="mini-sub">Available in the current route graph</div></div>', unsafe_allow_html=True)
                st.write("")
    else:
        st.info("No places match your search.")
    with st.expander("Project configuration: add or edit campus places"):
        st.write("Edit `LOCATIONS` and `EDGES` in `campus_data.py`, then redeploy. Distances should represent verified walkable path lengths in metres—not straight-line guesses.")

st.markdown("""
<hr style="border:0;border-top:1px solid #e2e8f0;margin-top:2rem;">
<div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;color:#7a899c;font-size:.82rem;">
<span>🧭 CampusGo · Smart Campus Navigation</span><span>Built with Python, Streamlit, OpenStreetMap & DSA</span>
</div>
""", unsafe_allow_html=True)
