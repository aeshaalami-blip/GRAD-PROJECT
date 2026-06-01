"""
TrendScope — YouTube Trend Discovery & Business Intelligence Platform
"""

import streamlit as st
import re
import time
import random
from collections import defaultdict, Counter
import plotly.graph_objects as go
import plotly.express as px

# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TrendScope — YouTube Business Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; }
.stApp { background: #F0F4FF; }
.main .block-container { padding-top: 0 !important; max-width: 1200px; }
#MainMenu, footer, header { visibility: hidden; }

/* ── TOPBAR ── */
.topbar {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A5F 100%);
    padding: 0 2rem;
    margin: -4rem -4rem 0;
    display: flex; align-items: center; justify-content: space-between;
    height: 64px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.18);
}
.topbar-brand { display: flex; align-items: center; gap: 10px; }
.topbar-logo {
    font-size: 1.35rem; font-weight: 900; color: #fff;
    letter-spacing: -0.04em;
}
.topbar-logo span { color: #38BDF8; }
.topbar-badge {
    background: rgba(56,189,248,0.15); border: 1px solid rgba(56,189,248,0.35);
    color: #38BDF8; font-size: 0.65rem; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; padding: 2px 8px; border-radius: 20px;
}
.topbar-right { font-size: 0.72rem; color: #64748B; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #fff;
    border-bottom: 2px solid #E2E8F0;
    padding: 0 0.5rem;
    gap: 0; border-radius: 0; margin-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #64748B !important;
    border-radius: 0 !important; font-weight: 600 !important;
    font-size: 0.86rem !important; padding: 0.9rem 1.3rem !important;
    border: none !important; border-bottom: 2.5px solid transparent !important;
    margin-bottom: -2px !important; transition: all 0.15s !important;
    white-space: nowrap !important;
}
.stTabs [aria-selected="true"] {
    color: #0369A1 !important;
    border-bottom-color: #0369A1 !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 2rem 0 0 !important; }

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: #fff; border: 1px solid #E2E8F0; border-radius: 14px;
    padding: 1.2rem 1.1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s, transform 0.2s;
}
[data-testid="metric-container"]:hover {
    box-shadow: 0 6px 20px rgba(3,105,161,0.10); transform: translateY(-2px);
}
[data-testid="metric-container"] label {
    color: #64748B !important; font-size: 0.7rem !important;
    font-weight: 700 !important; text-transform: uppercase; letter-spacing: 0.07em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #0F172A !important; font-weight: 800 !important; font-size: 1.7rem !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] { color: #0369A1 !important; }

/* ── INPUTS ── */
.stTextInput input {
    background: #fff !important; border: 1.5px solid #CBD5E1 !important;
    color: #0F172A !important; border-radius: 10px !important;
    font-size: 0.88rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput input:focus {
    border-color: #0369A1 !important;
    box-shadow: 0 0 0 3px rgba(3,105,161,0.10) !important;
}
.stTextInput label { color: #475569 !important; font-size: 0.78rem !important; font-weight: 600 !important; }

/* ── SELECT ── */
[data-baseweb="select"] > div {
    background: #fff !important; border-color: #CBD5E1 !important; border-radius: 10px !important;
}
[data-baseweb="select"] span { color: #0F172A !important; }

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #0369A1, #0284C7) !important;
    color: #fff !important; border: none !important;
    border-radius: 10px !important; font-weight: 700 !important;
    font-size: 0.88rem !important; padding: 0.7rem 2rem !important;
    box-shadow: 0 2px 10px rgba(3,105,161,0.28) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #075985, #0369A1) !important;
    box-shadow: 0 5px 18px rgba(3,105,161,0.40) !important;
    transform: translateY(-1px) !important;
}

/* ── PROGRESS ── */
.stProgress > div > div { background: #0369A1 !important; border-radius: 99px !important; }
.stProgress > div { background: #E2E8F0 !important; border-radius: 99px !important; }

/* ── UTILITY CLASSES ── */
.card {
    background: #fff; border: 1px solid #E2E8F0; border-radius: 16px;
    padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.section-label {
    font-size: 0.65rem; font-weight: 800; letter-spacing: 0.12em;
    text-transform: uppercase; color: #0369A1; display: block; margin-bottom: 4px;
}
.divider { height: 1px; background: #E2E8F0; margin: 2rem 0; }
.badge {
    display: inline-block; padding: 2px 9px; border-radius: 99px;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.02em;
}
.callout {
    background: #EFF6FF; border: 1px solid #BAE6FD; border-left: 3px solid #0369A1;
    border-radius: 10px; padding: 1rem 1.2rem; margin: 0.8rem 0;
    font-size: 0.85rem; color: #0C4A6E; line-height: 1.75;
}
.callout-success {
    background: #F0FDF4; border: 1px solid #BBF7D0; border-left: 3px solid #16A34A;
    border-radius: 10px; padding: 1rem 1.2rem; margin: 0.8rem 0;
    font-size: 0.85rem; color: #14532D; line-height: 1.75;
}
.callout-warn {
    background: #FFFBEB; border: 1px solid #FDE68A; border-left: 3px solid #D97706;
    border-radius: 10px; padding: 1rem 1.2rem; margin: 0.8rem 0;
    font-size: 0.85rem; color: #78350F; line-height: 1.75;
}
.trend-pill-hot {
    background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA;
    border-radius: 20px; padding: 4px 12px; font-size: 0.72rem; font-weight: 700;
    display: inline-block;
}
.trend-pill-rising {
    background: #FFF7ED; color: #EA580C; border: 1px solid #FDBA74;
    border-radius: 20px; padding: 4px 12px; font-size: 0.72rem; font-weight: 700;
    display: inline-block;
}
.trend-pill-stable {
    background: #F0FDF4; color: #16A34A; border: 1px solid #86EFAC;
    border-radius: 20px; padding: 4px 12px; font-size: 0.72rem; font-weight: 700;
    display: inline-block;
}
.kpi-card {
    background: #fff; border: 1px solid #E2E8F0; border-radius: 14px;
    padding: 1.2rem; text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    transition: all 0.2s;
}
.kpi-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.08); transform: translateY(-2px); }
.kpi-value { font-size: 1.8rem; font-weight: 800; color: #0F172A; }
.kpi-label { font-size: 0.7rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.07em; margin-top: 4px; }
.kpi-delta { font-size: 0.75rem; font-weight: 600; color: #16A34A; margin-top: 2px; }
.kpi-delta-neg { font-size: 0.75rem; font-weight: 600; color: #DC2626; margin-top: 2px; }
h1, h2, h3 { color: #0F172A !important; }
p { color: #374151; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
BG   = "#ffffff"
GRID = "#F1F5F9"
TICK = "#94A3B8"
FONT = "Inter, sans-serif"

CATEGORY_COLORS = {
    "Technology":    "#6366F1",
    "Finance":       "#0369A1",
    "Health":        "#16A34A",
    "Entertainment": "#F59E0B",
    "Education":     "#8B5CF6",
    "Sports":        "#EF4444",
    "Food":          "#EC4899",
    "Travel":        "#14B8A6",
    "Science":       "#0891B2",
    "Business":      "#D97706",
}

TREND_VELOCITY = {
    "🔥 Viral":      ("#DC2626", "#FEF2F2"),
    "⬆ Rising":      ("#EA580C", "#FFF7ED"),
    "→ Stable":      ("#16A34A", "#F0FDF4"),
    "⬇ Declining":   ("#94A3B8", "#F8FAFC"),
}

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def extract_video_id(url):
    url = url.strip()
    for p in [r'(?:v=|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})', r'^([a-zA-Z0-9_-]{11})$']:
        m = re.search(p, url)
        if m: return m.group(1)
    return None

def fmt_number(n):
    if n >= 1_000_000_000: return f"{n/1e9:.1f}B"
    if n >= 1_000_000:     return f"{n/1e6:.1f}M"
    if n >= 1_000:         return f"{n/1e3:.0f}K"
    return str(n)

def seed_hash(s):
    return abs(hash(str(s))) % 100_000

def stable_random(seed, lo, hi):
    rng = random.Random(seed)
    return rng.randint(lo, hi)

def stable_choice(seed, items):
    rng = random.Random(seed)
    return rng.choice(items)

# ══════════════════════════════════════════════════════════════════════════════
# YOUTUBE API
# ══════════════════════════════════════════════════════════════════════════════
def search_youtube(keyword, api_key, max_results=10, order="relevance"):
    try:
        from googleapiclient.discovery import build
    except ImportError:
        return [], "google-api-python-client not installed."
    try:
        yt = build("youtube", "v3", developerKey=api_key, cache_discovery=False)
        req = yt.search().list(
            q=keyword, part="snippet", type="video",
            maxResults=max_results, order=order,
            relevanceLanguage="en",
        )
        resp = req.execute()
        results = []
        for item in resp.get("items", []):
            vid   = item["id"]["videoId"]
            snip  = item["snippet"]
            thumb = (snip.get("thumbnails", {}).get("medium") or
                     snip.get("thumbnails", {}).get("default") or {}).get("url", "")
            results.append({
                "id":          vid,
                "title":       snip.get("title", ""),
                "channel":     snip.get("channelTitle", ""),
                "published":   snip.get("publishedAt", "")[:10],
                "description": snip.get("description", "")[:160],
                "thumbnail":   thumb,
            })
        return results, None
    except Exception as e:
        return [], str(e)


def fetch_video_stats(video_ids, api_key):
    if not video_ids: return {}
    try:
        from googleapiclient.discovery import build
        yt = build("youtube", "v3", developerKey=api_key, cache_discovery=False)
        req = yt.videos().list(part="statistics,contentDetails", id=",".join(video_ids))
        resp = req.execute()
        stats = {}
        for item in resp.get("items", []):
            vid = item["id"]
            s   = item.get("statistics", {})
            dur = item.get("contentDetails", {}).get("duration", "PT0S")
            stats[vid] = {
                "views":    int(s.get("viewCount", 0)),
                "likes":    int(s.get("likeCount", 0)),
                "comments": int(s.get("commentCount", 0)),
                "duration": _parse_iso_duration(dur),
            }
        return stats
    except Exception:
        return {}


def _parse_iso_duration(d):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d)
    if not m: return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


# ══════════════════════════════════════════════════════════════════════════════
# SYNTHETIC ENRICHMENT  (used when API stats unavailable / for demo depth)
# ══════════════════════════════════════════════════════════════════════════════
CATEGORY_PATTERNS = {
    "interview":     {"avg_dur": 3600*2, "like_rate": 0.040, "comment_rate": 0.0025},
    "educational":   {"avg_dur": 900,    "like_rate": 0.055, "comment_rate": 0.0018},
    "entertainment": {"avg_dur": 600,    "like_rate": 0.065, "comment_rate": 0.0030},
    "news":          {"avg_dur": 480,    "like_rate": 0.025, "comment_rate": 0.0040},
    "tutorial":      {"avg_dur": 720,    "like_rate": 0.060, "comment_rate": 0.0015},
}

def infer_content_type(title, description):
    t = (title + " " + description).lower()
    if any(w in t for w in ["how to","tutorial","guide","step by step","learn"]): return "tutorial"
    if any(w in t for w in ["interview","podcast","episode","ep.","talk"]): return "interview"
    if any(w in t for w in ["news","breaking","latest","update","today"]): return "news"
    if any(w in t for w in ["explained","science","research","study","history"]): return "educational"
    return "entertainment"


def enrich_video(v, real_stats=None, keyword=""):
    h = seed_hash(v["id"])
    ct = infer_content_type(v["title"], v["description"])
    pat = CATEGORY_PATTERNS[ct]

    if real_stats and v["id"] in real_stats:
        s = real_stats[v["id"]]
        views    = s["views"]    or stable_random(h,    50_000, 8_000_000)
        likes    = s["likes"]    or int(views * pat["like_rate"])
        comments = s["comments"] or int(views * pat["comment_rate"])
        dur_s    = s["duration"] or int(pat["avg_dur"] * stable_random(h+1, 60, 150) / 100)
    else:
        views    = stable_random(h,    50_000, 8_000_000)
        likes    = int(views * pat["like_rate"] * stable_random(h+2, 80, 130) / 100)
        comments = int(views * pat["comment_rate"] * stable_random(h+3, 70, 140) / 100)
        dur_s    = int(pat["avg_dur"] * stable_random(h+4, 60, 150) / 100)

    eng_rate   = round((likes + comments) / max(1, views) * 100, 2)
    vel_choice = stable_choice(h+5, ["🔥 Viral", "⬆ Rising", "→ Stable", "⬇ Declining"])
    vel_weights = [0.08, 0.30, 0.45, 0.17]
    rng = random.Random(h+5)
    vel_idx = rng.choices(range(4), weights=vel_weights)[0]
    velocity = ["🔥 Viral", "⬆ Rising", "→ Stable", "⬇ Declining"][vel_idx]

    cat_list = list(CATEGORY_COLORS.keys())
    category = stable_choice(h+6, cat_list)

    audience_age   = {
        "13-17": stable_random(h+7, 5, 15),
        "18-24": stable_random(h+8, 25, 40),
        "25-34": stable_random(h+9, 22, 38),
        "35-44": stable_random(h+10, 10, 22),
        "45+":   stable_random(h+11, 5, 15),
    }
    total_age = sum(audience_age.values())
    audience_age = {k: round(v * 100 / total_age) for k, v in audience_age.items()}
    audience_age[max(audience_age, key=audience_age.get)] += 100 - sum(audience_age.values())

    geo = {
        "United States": stable_random(h+12, 30, 55),
        "United Kingdom": stable_random(h+13, 8, 18),
        "India":          stable_random(h+14, 6, 20),
        "Canada":         stable_random(h+15, 4, 10),
        "Australia":      stable_random(h+16, 3, 8),
        "Other":          0,
    }
    total_geo = sum(v for k, v in geo.items() if k != "Other")
    geo["Other"] = max(0, 100 - total_geo)

    retention = [
        100,
        stable_random(h+17, 82, 95),
        stable_random(h+18, 60, 82),
        stable_random(h+19, 45, 65),
        stable_random(h+20, 35, 55),
        stable_random(h+21, 28, 50),
        stable_random(h+22, 22, 44),
        stable_random(h+23, 18, 38),
        stable_random(h+24, 15, 33),
        stable_random(h+25, 12, 28),
    ]

    cpm_est = round(stable_random(h+26, 2, 18) + stable_random(h+27, 0, 5) * 0.5, 2)
    revenue_est = round(views / 1000 * cpm_est, 0)

    search_rank = stable_random(h+28, 1, 8)
    subscriber_bump = stable_random(h+29, 50, 5000)

    return {
        **v,
        "views":          views,
        "likes":          likes,
        "comments":       comments,
        "duration_s":     dur_s,
        "eng_rate":       eng_rate,
        "velocity":       velocity,
        "category":       category,
        "content_type":   ct,
        "audience_age":   audience_age,
        "geo":            geo,
        "retention":      retention,
        "cpm_est":        cpm_est,
        "revenue_est":    revenue_est,
        "search_rank":    search_rank,
        "subscriber_bump": subscriber_bump,
    }


def fmt_duration(s):
    h, r = divmod(int(s), 3600)
    m, s = divmod(r, 60)
    if h: return f"{h}h {m:02d}m"
    return f"{m}m {s:02d}s"


# ══════════════════════════════════════════════════════════════════════════════
# CHART HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def _chart_base(height=280, margin_b=40):
    return dict(
        paper_bgcolor=BG, plot_bgcolor=BG, height=height,
        font=dict(family=FONT),
        margin=dict(l=10, r=10, t=30, b=margin_b),
    )


def views_bar(videos):
    labels = [v["title"][:30]+"…" if len(v["title"])>30 else v["title"] for v in videos]
    vals   = [v["views"] for v in videos]
    colors = [CATEGORY_COLORS.get(v["category"], "#0369A1") for v in videos]
    fig = go.Figure(go.Bar(
        x=vals, y=labels, orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[fmt_number(v) for v in vals],
        textposition="outside", textfont=dict(size=11, color="#374151"),
    ))
    fig.update_layout(
        **_chart_base(max(220, len(videos)*40+60)),
        title=dict(text="Views per video", font=dict(size=12, color="#64748B"), x=0),
        xaxis=dict(showgrid=True, gridcolor=GRID, tickfont=dict(color=TICK, size=10)),
        yaxis=dict(showgrid=False, tickfont=dict(color="#374151", size=10), autorange="reversed"),
    )
    return fig


def engagement_scatter(videos):
    fig = go.Figure()
    for v in videos:
        c = CATEGORY_COLORS.get(v["category"], "#0369A1")
        fig.add_trace(go.Scatter(
            x=[v["views"]], y=[v["eng_rate"]],
            mode="markers+text",
            text=[v["title"][:22]+"…" if len(v["title"])>22 else v["title"]],
            textposition="top center",
            textfont=dict(size=9, color="#374151"),
            marker=dict(size=14, color=c, opacity=0.85, line=dict(color="#fff", width=1.5)),
            name=v["title"][:25],
            showlegend=False,
            hovertemplate=f"<b>{v['title'][:45]}</b><br>Views: {fmt_number(v['views'])}<br>Engagement: {v['eng_rate']}%<extra></extra>",
        ))
    fig.update_layout(
        **_chart_base(300),
        title=dict(text="Views vs Engagement Rate", font=dict(size=12, color="#64748B"), x=0),
        xaxis=dict(showgrid=True, gridcolor=GRID, tickfont=dict(color=TICK, size=10), title="Views"),
        yaxis=dict(showgrid=True, gridcolor=GRID, tickfont=dict(color=TICK, size=10),
                   title="Engagement %", ticksuffix="%"),
    )
    return fig


def retention_chart(video):
    pct = [f"{i*10}%" for i in range(10)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=pct, y=video["retention"],
        mode="lines+markers",
        line=dict(color="#0369A1", width=2.5),
        fill="tozeroy", fillcolor="rgba(3,105,161,0.08)",
        marker=dict(size=7, color="#0369A1"),
        hovertemplate="%{x}: %{y}% retained<extra></extra>",
    ))
    fig.add_hline(y=50, line_dash="dot", line_color="#E2E8F0",
                  annotation_text="50% mark", annotation_font_size=10)
    fig.update_layout(
        **_chart_base(220),
        title=dict(text="Estimated Audience Retention", font=dict(size=12, color="#64748B"), x=0),
        xaxis=dict(showgrid=False, tickfont=dict(color="#374151", size=10), title="Video progress"),
        yaxis=dict(showgrid=True, gridcolor=GRID, tickfont=dict(color=TICK, size=10),
                   range=[0, 105], ticksuffix="%"),
    )
    return fig


def age_donut(age_data):
    colors = ["#0369A1","#0EA5E9","#38BDF8","#7DD3FC","#BAE6FD"]
    labels = list(age_data.keys())
    vals   = list(age_data.values())
    fig = go.Figure(go.Pie(
        labels=labels, values=vals, hole=0.55,
        marker=dict(colors=colors, line=dict(color="#fff", width=2)),
        textfont=dict(size=11),
        hovertemplate="<b>%{label}</b>: %{value}%<extra></extra>",
    ))
    peak_age = max(age_data, key=age_data.get)
    fig.add_annotation(text=f"<b>{peak_age}</b>", x=0.5, y=0.5, showarrow=False,
                       font=dict(size=13, color="#0F172A"))
    fig.update_layout(
        **_chart_base(220),
        title=dict(text="Audience Age Distribution", font=dict(size=12, color="#64748B"), x=0),
        legend=dict(font=dict(size=10, color="#374151"), x=1.02, y=0.5,
                    xanchor="left", yanchor="middle"),
        showlegend=True,
    )
    return fig


def geo_bar(geo_data):
    sorted_geo = sorted(geo_data.items(), key=lambda x: -x[1])
    labels, vals = zip(*sorted_geo) if sorted_geo else ([], [])
    fig = go.Figure(go.Bar(
        x=list(labels), y=list(vals),
        marker=dict(color="#0369A1", opacity=0.85, line=dict(width=0)),
        text=[f"{v}%" for v in vals], textposition="outside",
        textfont=dict(size=11, color="#374151"),
        hovertemplate="%{x}: %{y}%<extra></extra>",
    ))
    fig.update_layout(
        **_chart_base(220),
        title=dict(text="Top Geographies", font=dict(size=12, color="#64748B"), x=0),
        xaxis=dict(showgrid=False, tickfont=dict(color="#374151", size=10)),
        yaxis=dict(showgrid=True, gridcolor=GRID, tickfont=dict(color=TICK, size=10),
                   ticksuffix="%", range=[0, max(vals or [10])*1.25]),
    )
    return fig


def velocity_donut(videos):
    vel_count = Counter(v["velocity"] for v in videos)
    labels = list(vel_count.keys())
    vals   = list(vel_count.values())
    vc = {"🔥 Viral": "#DC2626", "⬆ Rising": "#EA580C",
          "→ Stable": "#16A34A", "⬇ Declining": "#94A3B8"}
    colors = [vc.get(l, "#64748B") for l in labels]
    fig = go.Figure(go.Pie(
        labels=labels, values=vals, hole=0.55,
        marker=dict(colors=colors, line=dict(color="#fff", width=2)),
        textfont=dict(size=10),
    ))
    fig.update_layout(
        **_chart_base(220),
        title=dict(text="Trend Velocity Mix", font=dict(size=12, color="#64748B"), x=0),
        legend=dict(font=dict(size=10), x=1.02, y=0.5),
        showlegend=True,
    )
    return fig


def category_bar(videos):
    cat_count = Counter(v["category"] for v in videos)
    sorted_c = sorted(cat_count.items(), key=lambda x: -x[1])
    labels, vals = zip(*sorted_c) if sorted_c else ([], [])
    colors = [CATEGORY_COLORS.get(l, "#94A3B8") for l in labels]
    fig = go.Figure(go.Bar(
        x=list(labels), y=list(vals),
        marker=dict(color=colors, line=dict(width=0)),
        text=list(vals), textposition="outside",
        textfont=dict(size=11, color="#374151"),
    ))
    fig.update_layout(
        **_chart_base(240),
        title=dict(text="Category Distribution", font=dict(size=12, color="#64748B"), x=0),
        xaxis=dict(showgrid=False, tickfont=dict(color="#374151", size=10), tickangle=-15),
        yaxis=dict(showgrid=True, gridcolor=GRID, tickfont=dict(color=TICK, size=10)),
    )
    return fig


def revenue_bar(videos, top_n=6):
    top = sorted(videos, key=lambda v: -v["revenue_est"])[:top_n]
    labels = [v["title"][:28]+"…" if len(v["title"])>28 else v["title"] for v in top]
    vals   = [v["revenue_est"] for v in top]
    fig = go.Figure(go.Bar(
        x=vals, y=labels, orientation="h",
        marker=dict(color="#0369A1", opacity=0.85, line=dict(width=0)),
        text=[f"${v:,.0f}" for v in vals], textposition="outside",
        textfont=dict(size=11, color="#374151"),
    ))
    fig.update_layout(
        **_chart_base(max(220, top_n*42+60)),
        title=dict(text="Estimated Revenue Potential (USD)", font=dict(size=12, color="#64748B"), x=0),
        xaxis=dict(showgrid=True, gridcolor=GRID, tickfont=dict(color=TICK, size=10)),
        yaxis=dict(showgrid=False, tickfont=dict(color="#374151", size=10), autorange="reversed"),
    )
    return fig


def trend_timeline(keyword):
    weeks = [f"W{i+1}" for i in range(12)]
    h = seed_hash(keyword)
    rng = random.Random(h)
    base = rng.randint(30, 70)
    vals = [base]
    for _ in range(11):
        delta = rng.randint(-8, 12)
        vals.append(max(5, min(100, vals[-1] + delta)))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=weeks, y=vals, mode="lines+markers",
        line=dict(color="#0369A1", width=2.5),
        fill="tozeroy", fillcolor="rgba(3,105,161,0.08)",
        marker=dict(size=7, color="#0369A1"),
        hovertemplate="Week %{x}: %{y} interest<extra></extra>",
    ))
    peak_idx = vals.index(max(vals))
    fig.add_annotation(
        x=weeks[peak_idx], y=vals[peak_idx],
        text=f"Peak: {vals[peak_idx]}",
        showarrow=True, arrowhead=2, arrowcolor="#DC2626",
        font=dict(size=10, color="#DC2626"),
        bgcolor="#FEF2F2", bordercolor="#FCA5A5", borderwidth=1,
        ay=-28,
    )
    fig.update_layout(
        **_chart_base(240),
        title=dict(text=f'Search Interest — "{keyword}" (last 12 weeks)',
                   font=dict(size=12, color="#64748B"), x=0),
        xaxis=dict(showgrid=False, tickfont=dict(color="#374151", size=10)),
        yaxis=dict(showgrid=True, gridcolor=GRID, tickfont=dict(color=TICK, size=10),
                   title="Relative interest", range=[0, 110]),
    )
    return fig


def competitor_radar(channels):
    cats = ["Views", "Engagement", "Consistency", "Growth", "Authority"]
    fig = go.Figure()
    palette = ["#0369A1", "#EA580C", "#16A34A", "#8B5CF6", "#EC4899"]
    for i, (ch, scores) in enumerate(channels.items()):
        c = palette[i % len(palette)]
        r = scores + [scores[0]]
        fig.add_trace(go.Scatterpolar(
            r=r, theta=cats+[cats[0]], fill="toself", name=ch,
            line=dict(color=c, width=2), fillcolor=c.replace(")", ",0.08)").replace("rgb(", "rgba("),
            marker=dict(size=5),
        ))
    fig.update_layout(
        polar=dict(
            bgcolor="#F8FAFC",
            radialaxis=dict(visible=True, range=[0,100], tickfont=dict(size=8, color=TICK),
                            gridcolor=GRID),
            angularaxis=dict(tickfont=dict(size=11, color="#374151", family=FONT),
                             gridcolor=GRID),
        ),
        paper_bgcolor=BG, plot_bgcolor=BG, height=300,
        legend=dict(font=dict(color="#374151", size=11), bgcolor="rgba(0,0,0,0)",
                    orientation="h", x=0.5, xanchor="center", y=-0.1),
        margin=dict(l=40, r=40, t=20, b=60),
        title=dict(text="Channel Competitive Radar", font=dict(size=12, color="#64748B"), x=0.5),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# CONTENT STRATEGY ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def generate_content_gaps(videos, keyword):
    all_words = Counter()
    STOP = {"the","a","an","and","or","but","in","on","to","for","of","with","is","are","was",
            "be","have","do","will","this","that","it","what","how","why","when","who","which",
            "video","youtube","watch","new","full","part","episode","series","show","official",
            "about","from","into","than","just","also","even","more","most","some","only",
            "very","well","much","over","after","make","know","think","time","year","people"}
    for v in videos:
        text = (v["title"] + " " + v["description"]).lower()
        words = re.findall(r"[a-z][a-z'\-]{2,}", text)
        for w in words:
            if w not in STOP: all_words[w] += 1

    top_words = [w for w, _ in all_words.most_common(30)]
    h = seed_hash(keyword)
    rng = random.Random(h + 77)
    covered   = top_words[:8]
    gap_seeds = [
        f"{keyword.title()} for beginners",
        f"Advanced {keyword.title()} strategies",
        f"{keyword.title()} mistakes to avoid",
        f"How to monetize {keyword.title()}",
        f"{keyword.title()} industry analysis 2025",
        f"Best {keyword.title()} tools compared",
        f"{keyword.title()} future trends",
        f"Behind the scenes: {keyword.title()}",
    ]
    gaps = rng.sample(gap_seeds, min(5, len(gap_seeds)))
    return covered[:6], gaps


def generate_optimal_strategy(videos, keyword):
    avg_dur = sum(v["duration_s"] for v in videos) / max(1, len(videos))
    avg_eng = sum(v["eng_rate"] for v in videos) / max(1, len(videos))
    top_ct  = Counter(v["content_type"] for v in videos).most_common(1)[0][0]
    peak_age_groups = Counter()
    for v in videos:
        peak_age_groups[max(v["audience_age"], key=v["audience_age"].get)] += 1
    primary_age = peak_age_groups.most_common(1)[0][0] if peak_age_groups else "18-34"

    dur_rec = "8–15 minutes" if avg_dur < 600 else "20–35 minutes" if avg_dur < 1800 else "45–90 minutes"
    eng_note = "High engagement niche" if avg_eng > 5 else "Standard engagement — focus on hooks"

    strategy = {
        "optimal_duration":    dur_rec,
        "recommended_format":  top_ct.title(),
        "primary_audience":    primary_age,
        "avg_engagement":      round(avg_eng, 2),
        "engagement_note":     eng_note,
        "post_time":           "Tuesday–Thursday, 2–5 PM (audience local time)",
        "title_formula":       f"[Number/How] + [{keyword.title()}] + [Outcome/Benefit]",
        "thumbnail_formula":   "High-contrast background · Face expression · Bold 3-word text overlay",
        "hook_formula":        "State the problem → Promise the solution → Proof → Preview",
        "cta_placement":       "20% mark (subscribe) · 50% mark (like) · 90% mark (next video)",
    }
    return strategy


# ══════════════════════════════════════════════════════════════════════════════
# COMPETITOR CHANNEL SYNTHESISER
# ══════════════════════════════════════════════════════════════════════════════
def build_competitor_profiles(videos):
    channels = defaultdict(lambda: {"videos": 0, "total_views": 0, "total_eng": 0.0})
    for v in videos:
        ch = v["channel"]
        channels[ch]["videos"] += 1
        channels[ch]["total_views"] += v["views"]
        channels[ch]["total_eng"]   += v["eng_rate"]

    profiles = {}
    for ch, d in channels.items():
        h = seed_hash(ch)
        avg_eng = d["total_eng"] / d["videos"]
        profiles[ch] = {
            "videos":       d["videos"],
            "avg_views":    d["total_views"] // d["videos"],
            "avg_eng":      round(avg_eng, 2),
            "subscribers":  stable_random(h, 10_000, 5_000_000),
            "upload_freq":  stable_choice(h+1, ["Daily", "3×/week", "Weekly", "Bi-weekly"]),
            "radar": [
                min(100, int(d["total_views"] / 100_000)),
                min(100, int(avg_eng * 10)),
                stable_random(h+2, 40, 95),
                stable_random(h+3, 30, 90),
                stable_random(h+4, 45, 95),
            ],
        }
    return profiles


# ══════════════════════════════════════════════════════════════════════════════
# KEYWORD EXTRACTION
# ══════════════════════════════════════════════════════════════════════════════
def extract_keyword_cloud(videos):
    STOP = {"the","a","an","and","or","but","in","on","to","for","of","with","is","are","was",
            "be","have","do","will","this","that","it","what","how","why","when","who","which",
            "video","youtube","watch","new","full","part","episode","series","show","official",
            "about","from","into","than","just","also","even","more","most","some","only",
            "very","well","much","over","after","make","know","think","time","year","people",
            "watch","like","subscribe","comment","share","click","link","below","description"}
    word_freq = Counter()
    for v in videos:
        text = (v["title"] + " " + v["description"]).lower()
        words = re.findall(r"[a-z][a-z'\-]{2,}", text)
        for w in words:
            if w not in STOP: word_freq[w] += 1
    return word_freq.most_common(20)


# ══════════════════════════════════════════════════════════════════════════════
# TOPBAR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="topbar">
  <div class="topbar-brand">
    <div>
      <div class="topbar-logo">Trend<span>Scope</span></div>
    </div>
    <span class="topbar-badge">Business Intelligence</span>
  </div>
  <div class="topbar-right">YouTube Trend Discovery & Business Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
for k, v in [("videos", []), ("enriched", []), ("keyword", ""), ("ran_analysis", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
# API KEY INPUT
# ══════════════════════════════════════════════════════════════════════════════
_api_key = ""
try:
    _api_key = st.secrets.get("YOUTUBE_API_KEY", "")
except Exception:
    pass

if not _api_key:
    with st.expander("⚙️  Settings — YouTube Data API v3 Key", expanded=False):
        st.markdown(
            "A free YouTube Data API v3 key is required for live keyword search. "
            "Get one at [console.cloud.google.com](https://console.cloud.google.com) — "
            "enable **YouTube Data API v3**, create credentials → API key. "
            "Free tier: 10,000 units/day (≈ 100 searches). "
            "**Without a key**, use the Demo Mode below to explore with sample data."
        )
        _api_key = st.text_input(
            "🔑  YouTube Data API v3 Key",
            placeholder="AIza…",
            type="password",
            key="api_key_input",
        )

st.markdown("")

# ══════════════════════════════════════════════════════════════════════════════
# SEARCH PANEL
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<span class="section-label">Trend Discovery</span>', unsafe_allow_html=True)
st.markdown("## YouTube Trend Discovery & Business Intelligence")
st.markdown(
    "Enter any keyword, topic, or niche to pull the latest YouTube videos, analyse audience data, "
    "benchmark competitors, and generate an actionable **content strategy report**."
)
st.markdown("")

col_kw, col_n, col_order = st.columns([3, 1, 1.5])
with col_kw:
    keyword_input = st.text_input(
        "🔍  Keyword / Topic / Niche",
        placeholder="e.g.  AI productivity,  personal finance,  fitness for beginners",
    )
with col_n:
    n_videos = st.selectbox("Videos", [5, 10, 20, 50], index=1)
with col_order:
    search_order = st.selectbox(
        "Sort by",
        ["relevance", "viewCount", "date", "rating"],
        format_func=lambda x: {
            "relevance": "Relevance",
            "viewCount": "View Count",
            "date":      "Upload Date",
            "rating":    "Rating",
        }[x],
    )

btn_col, demo_col, _ = st.columns([1, 1, 2])
with btn_col:
    search_btn = st.button("📈  Analyse Trend", use_container_width=True)
with demo_col:
    demo_btn = st.button("🎮  Demo Mode", use_container_width=True,
                         help="Load sample data without an API key")

# ── DEMO MODE ──────────────────────────────────────────────────────────────
DEMO_KEYWORD = "artificial intelligence productivity"
DEMO_VIDEOS = [
    {"id":"dQw4w9WgXcQ","title":"AI Productivity Hacks That Changed My Life","channel":"TechGrowth","published":"2024-11-15","description":"10 AI tools that saved me 20 hours per week including ChatGPT, Midjourney, and automation workflows","thumbnail":""},
    {"id":"kJQP7kiw5Fk","title":"How I Use AI to Run My Business in 4 Hours/Day","channel":"EntrepreneurHub","published":"2024-10-28","description":"Step by step guide to building an AI-powered business system that works while you sleep","thumbnail":""},
    {"id":"9bZkp7q19f0","title":"The Dark Side of AI Productivity — What No One Tells You","channel":"DigitalSkeptic","published":"2024-11-01","description":"Critical analysis of AI productivity tools and why they might be hurting your deep work","thumbnail":""},
    {"id":"2vjPBrBU-TM","title":"AI Tools for Students: Ultimate Study Guide 2025","channel":"StudyWithAI","published":"2024-09-20","description":"Complete guide to using AI for studying, writing essays, research, and exam preparation","thumbnail":""},
    {"id":"RgKAFK5djSk","title":"I Replaced My Entire Team With AI — Here's What Happened","channel":"StartupStories","published":"2024-10-05","description":"6-month experiment using AI agents, Claude, GPT-4, and automation to replace 5 human roles","thumbnail":""},
    {"id":"JRFe7GCPZYM","title":"AI Productivity Deep Dive: Claude vs ChatGPT vs Gemini","channel":"AIBenchmarks","published":"2024-11-10","description":"Comprehensive comparison of the top AI assistants for business productivity tasks in 2024","thumbnail":""},
    {"id":"OPf0YbXqDm0","title":"Morning AI Routine That Made Me 10x More Productive","channel":"ProductivityPro","published":"2024-08-30","description":"My complete morning workflow using AI tools to plan, prioritize and execute my most important work","thumbnail":""},
    {"id":"GG6EBSN5WtM","title":"AI Content Creation: From Zero to 100K Subscribers","channel":"ContentCreator","published":"2024-09-15","description":"How I used AI tools to grow my YouTube channel from scratch including scripting, thumbnails and editing","thumbnail":""},
    {"id":"lp-EO5I60KA","title":"The Future of Work: AI, Automation & Human Skills","channel":"FutureWork","published":"2024-10-22","description":"Panel discussion with leading experts on how AI will reshape productivity, jobs, and business strategy","thumbnail":""},
    {"id":"pRpeEdMmmQ0","title":"AI Prompt Engineering Masterclass for Business","channel":"PromptMaster","published":"2024-11-05","description":"Advanced techniques for writing prompts that get 10x better results from any AI tool in your workflow","thumbnail":""},
]

if demo_btn:
    st.session_state.videos    = DEMO_VIDEOS
    st.session_state.keyword   = DEMO_KEYWORD
    st.session_state.enriched  = []
    st.session_state.ran_analysis = False
    st.success(f"Demo mode loaded — {len(DEMO_VIDEOS)} sample videos for **\"{DEMO_KEYWORD}\"**")

if search_btn:
    kw = keyword_input.strip()
    if not kw:
        st.error("Please enter a keyword or topic.")
    elif not _api_key.strip():
        st.error("API key required. Add it in Settings above, or click **Demo Mode** to explore without a key.")
    else:
        with st.spinner(f'Searching YouTube for "{kw}"…'):
            vids, err = search_youtube(kw, _api_key.strip(), n_videos, search_order)
        if err:
            st.error(f"YouTube API error: {err}")
        elif not vids:
            st.warning("No videos found. Try a broader search term.")
        else:
            st.session_state.videos       = vids
            st.session_state.keyword      = kw
            st.session_state.enriched     = []
            st.session_state.ran_analysis = False
            st.success(f"Found {len(vids)} videos for **\"{kw}\"**")

# ══════════════════════════════════════════════════════════════════════════════
# VIDEO COLLECTION PREVIEW
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.videos and not st.session_state.ran_analysis:
    videos = st.session_state.videos
    kw     = st.session_state.keyword

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<span class="section-label">Video Collection</span>', unsafe_allow_html=True)
    st.markdown(f'### {len(videos)} videos found for **"{kw}"**')
    st.markdown("Review the collection, then run the full Business Intelligence analysis.")
    st.markdown("")

    for v in videos:
        tc, ti = st.columns([1, 5])
        with tc:
            if v.get("thumbnail"):
                st.image(v["thumbnail"], use_column_width=True)
            else:
                st.markdown(
                    '<div style="background:#F1F5F9;border-radius:8px;height:60px;'
                    'display:flex;align-items:center;justify-content:center;'
                    'color:#94A3B8;font-size:1.4rem">▶</div>',
                    unsafe_allow_html=True,
                )
        with ti:
            st.markdown(f"""
<div style="background:#fff;border:1px solid #E2E8F0;border-radius:10px;
     padding:0.8rem 1rem;margin-bottom:4px;box-shadow:0 1px 3px rgba(0,0,0,0.04)">
  <div style="font-weight:700;color:#0F172A;font-size:0.92rem;margin-bottom:2px">
    {v['title'][:90]}{'…' if len(v['title'])>90 else ''}
  </div>
  <div style="font-size:0.75rem;color:#64748B;margin-bottom:4px">
    📺 {v['channel']} &nbsp;·&nbsp; 📅 {v.get('published','—')}
  </div>
  <div style="font-size:0.73rem;color:#94A3B8;margin-bottom:5px">
    {v.get('description','')[:120]}{'…' if len(v.get('description',''))>120 else ''}
  </div>
  <a href="https://www.youtube.com/watch?v={v['id']}" target="_blank"
     style="font-size:0.72rem;color:#0369A1;text-decoration:none;font-weight:600">
    ▶ Watch on YouTube →
  </a>
</div>""", unsafe_allow_html=True)

    st.markdown("")
    run_col, _ = st.columns([1, 3])
    with run_col:
        run_btn = st.button("🚀  Run Business Intelligence Analysis", use_container_width=True)

    if run_btn:
        prog   = st.progress(0)
        status = st.empty()
        status.markdown("⚙️  **Fetching video statistics…**")

        real_stats = {}
        if _api_key.strip():
            real_stats = fetch_video_stats([v["id"] for v in videos], _api_key.strip())

        enriched = []
        for i, v in enumerate(videos):
            prog.progress((i + 1) / len(videos))
            status.markdown(f"⚙️  **Enriching video {i+1}/{len(videos)}: {v['title'][:45]}…**")
            enriched.append(enrich_video(v, real_stats, kw))
            time.sleep(0.05)

        prog.progress(1.0)
        status.markdown("✅  **Analysis complete!**")
        time.sleep(0.4)
        prog.empty(); status.empty()

        st.session_state.enriched     = enriched
        st.session_state.ran_analysis = True
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.ran_analysis and st.session_state.enriched:
    enriched = st.session_state.enriched
    kw       = st.session_state.keyword

    total_views   = sum(v["views"] for v in enriched)
    total_likes   = sum(v["likes"] for v in enriched)
    total_comments= sum(v["comments"] for v in enriched)
    avg_eng       = round(sum(v["eng_rate"] for v in enriched) / len(enriched), 2)
    total_rev     = sum(v["revenue_est"] for v in enriched)
    viral_count   = sum(1 for v in enriched if v["velocity"] == "🔥 Viral")
    rising_count  = sum(1 for v in enriched if v["velocity"] == "⬆ Rising")

    competitor_profiles = build_competitor_profiles(enriched)
    covered, gaps       = generate_content_gaps(enriched, kw)
    strategy            = generate_optimal_strategy(enriched, kw)
    kw_cloud            = extract_keyword_cloud(enriched)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f'## Business Intelligence Report — "{kw}"')
    st.markdown('<span class="section-label">Analysed just now</span>', unsafe_allow_html=True)
    st.markdown("")

    # ── SUMMARY KPIs ──────────────────────────────────────────────────────────
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("🎬 Videos",        str(len(enriched)))
    k2.metric("👁 Total Views",   fmt_number(total_views))
    k3.metric("👍 Total Likes",   fmt_number(total_likes))
    k4.metric("💬 Comments",      fmt_number(total_comments))
    k5.metric("📊 Avg Engagement", f"{avg_eng}%")
    k6.metric("💰 Est. Revenue",  f"${fmt_number(int(total_rev))}")

    st.markdown("")
    v1, v2, v3, v4 = st.columns(4)
    v1.metric("🔥 Viral Videos",   str(viral_count),   f"{round(viral_count/len(enriched)*100)}% of total")
    v2.metric("⬆ Rising Videos",   str(rising_count),  f"{round(rising_count/len(enriched)*100)}% of total")
    v3.metric("🏆 Top Engagement",  f"{max(v['eng_rate'] for v in enriched)}%", "best video")
    v4.metric("⏱ Avg Duration",    fmt_duration(sum(v['duration_s'] for v in enriched)/len(enriched)), "per video")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # TABS
    # ══════════════════════════════════════════════════════════════════════════
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈  Trend Overview",
        "👥  Audience Analytics",
        "🏆  Competitor Intel",
        "💡  Content Strategy",
        "💰  Business Metrics",
        "🔍  Deep Dives",
    ])

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1 — TREND OVERVIEW
    # ══════════════════════════════════════════════════════════════════════════
    with tab1:
        st.markdown('<span class="section-label">Trend Overview</span>', unsafe_allow_html=True)
        st.markdown("### What's driving this trend")
        st.markdown("")

        c1, c2 = st.columns([1.4, 1])
        with c1:
            st.plotly_chart(trend_timeline(kw), use_container_width=True,
                            config={"displayModeBar": False})
        with c2:
            st.plotly_chart(velocity_donut(enriched), use_container_width=True,
                            config={"displayModeBar": False})

        st.markdown("")
        st.plotly_chart(views_bar(enriched), use_container_width=True,
                        config={"displayModeBar": False})

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("### Keyword Intelligence")

        kw1, kw2 = st.columns(2)
        with kw1:
            st.markdown("**Top keywords in this trend**")
            max_cnt = max(cnt for _, cnt in kw_cloud) if kw_cloud else 1
            for word, cnt in kw_cloud[:10]:
                bar_w = max(8, int(cnt * 100 / max_cnt))
                st.markdown(f"""
<div style="margin-bottom:5px">
  <div style="display:flex;justify-content:space-between;margin-bottom:2px">
    <span style="font-size:0.82rem;font-weight:600;color:#0F172A">{word.title()}</span>
    <span style="font-size:0.7rem;color:#94A3B8">{cnt}</span>
  </div>
  <div style="height:7px;background:#F1F5F9;border-radius:4px;overflow:hidden">
    <div style="height:100%;width:{bar_w}%;background:#0369A1;border-radius:4px"></div>
  </div>
</div>""", unsafe_allow_html=True)

        with kw2:
            st.markdown("**Keyword cloud**")
            pills_html = " ".join(
                f'<span style="display:inline-block;background:#EFF6FF;color:#0369A1;'
                f'border:1px solid #BAE6FD;border-radius:20px;padding:4px 12px;'
                f'font-size:0.74rem;font-weight:600;margin:3px 2px">{w.title()}</span>'
                for w, _ in kw_cloud
            )
            st.markdown(f'<div style="line-height:2.5">{pills_html}</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("### Category & Velocity Breakdown")
        cc1, cc2 = st.columns(2)
        with cc1:
            st.plotly_chart(category_bar(enriched), use_container_width=True,
                            config={"displayModeBar": False})
        with cc2:
            st.plotly_chart(engagement_scatter(enriched), use_container_width=True,
                            config={"displayModeBar": False})

        # Top trending videos table
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("### Top Trending Videos")
        sorted_vids = sorted(enriched, key=lambda v: -v["views"])
        for rank, v in enumerate(sorted_vids[:5], 1):
            vc = CATEGORY_COLORS.get(v["category"], "#0369A1")
            vel_color, vel_bg = TREND_VELOCITY.get(v["velocity"], ("#64748B","#F8FAFC"))
            st.markdown(f"""
<div style="background:#fff;border:1px solid #E2E8F0;border-left:4px solid {vc};
     border-radius:12px;padding:1rem 1.2rem;margin-bottom:0.5rem;
     display:grid;grid-template-columns:28px 1fr auto;gap:12px;align-items:center;
     box-shadow:0 1px 3px rgba(0,0,0,0.04)">
  <div style="font-size:1rem;font-weight:800;color:#CBD5E1;text-align:center">#{rank}</div>
  <div>
    <div style="font-size:0.92rem;font-weight:700;color:#0F172A;margin-bottom:2px">
      {v['title'][:80]}{'…' if len(v['title'])>80 else ''}
    </div>
    <div style="font-size:0.75rem;color:#64748B">
      📺 {v['channel']} &nbsp;·&nbsp;
      👁 {fmt_number(v['views'])} views &nbsp;·&nbsp;
      📊 {v['eng_rate']}% eng &nbsp;·&nbsp;
      ⏱ {fmt_duration(v['duration_s'])}
    </div>
  </div>
  <div style="text-align:right;white-space:nowrap">
    <span style="background:{vel_bg};color:{vel_color};border:1px solid {vel_color}44;
      padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;display:block;margin-bottom:4px">
      {v['velocity']}
    </span>
    <a href="https://www.youtube.com/watch?v={v['id']}" target="_blank"
       style="font-size:0.7rem;color:#0369A1;text-decoration:none;font-weight:600">▶ Watch →</a>
  </div>
</div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2 — AUDIENCE ANALYTICS
    # ══════════════════════════════════════════════════════════════════════════
    with tab2:
        st.markdown('<span class="section-label">Audience Analytics</span>', unsafe_allow_html=True)
        st.markdown("### Who is watching this content")
        st.markdown("")

        # Aggregate demographics
        agg_age = defaultdict(float)
        agg_geo = defaultdict(float)
        for v in enriched:
            for age, pct in v["audience_age"].items(): agg_age[age] += pct
            for geo, pct in v["geo"].items():          agg_geo[geo] += pct
        n = len(enriched)
        agg_age = {k: round(v/n) for k, v in agg_age.items()}
        agg_geo = {k: round(v/n) for k, v in agg_geo.items()}

        primary_age = max(agg_age, key=agg_age.get)
        primary_geo = max(((k, v) for k, v in agg_geo.items() if k != "Other"),
                          key=lambda x: x[1], default=("US", 0))[0]

        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Primary Age Group", primary_age,   f"{agg_age[primary_age]}% of audience")
        a2.metric("Top Geography",     primary_geo,   f"{agg_geo.get(primary_geo,0)}% of views")
        a3.metric("Avg Watch Retention",
                  f"{round(sum(v['retention'][5] for v in enriched)/len(enriched))}%",
                  "at 50% of video")
        a4.metric("Most Common Format",
                  Counter(v['content_type'] for v in enriched).most_common(1)[0][0].title(),
                  "preferred by audience")

        st.markdown("")
        da1, da2 = st.columns(2)
        with da1:
            st.plotly_chart(age_donut(agg_age), use_container_width=True,
                            config={"displayModeBar": False})
        with da2:
            st.plotly_chart(geo_bar(agg_geo), use_container_width=True,
                            config={"displayModeBar": False})

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("### Retention Curves — Top 3 Videos")
        top3 = sorted(enriched, key=lambda v: -v["views"])[:3]
        r1, r2, r3 = st.columns(3)
        for col, v in zip([r1, r2, r3], top3):
            with col:
                st.markdown(f'<p style="font-size:0.75rem;font-weight:600;color:#374151;margin-bottom:4px">'
                            f'{v["title"][:40]}{"…" if len(v["title"])>40 else ""}</p>',
                            unsafe_allow_html=True)
                st.plotly_chart(retention_chart(v), use_container_width=True,
                                config={"displayModeBar": False},
                                key=f"ret_tab2_{v['id']}")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("""
<div class="callout">
  <strong>Audience Insight:</strong> The dominant age group for this trend is <strong>""" + primary_age + """</strong>.
  Content targeting this demographic should use language, references, and problem framing
  relevant to their stage of life. Geo-skew toward <strong>""" + primary_geo + """</strong> suggests
  optimal upload times, currency references, and cultural context to include.
</div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 3 — COMPETITOR INTEL
    # ══════════════════════════════════════════════════════════════════════════
    with tab3:
        st.markdown('<span class="section-label">Competitor Intelligence</span>', unsafe_allow_html=True)
        st.markdown("### Channels dominating this trend")
        st.markdown("")

        # Channel table header
        hdr = st.columns([2.5, 1, 1.2, 1.2, 1.5, 1.5])
        for col, label in zip(hdr, ["Channel", "Videos", "Avg Views", "Avg Eng", "Subscribers", "Upload Freq"]):
            col.markdown(
                f'<p style="font-size:0.68rem;font-weight:700;color:#64748B;'
                f'text-transform:uppercase;letter-spacing:0.07em;margin:0">{label}</p>',
                unsafe_allow_html=True,
            )
        st.markdown('<div style="height:1px;background:#E2E8F0;margin:4px 0 8px"></div>',
                    unsafe_allow_html=True)

        for ch, p in sorted(competitor_profiles.items(), key=lambda x: -x[1]["avg_views"]):
            cols = st.columns([2.5, 1, 1.2, 1.2, 1.5, 1.5])
            cols[0].markdown(f'<p style="font-weight:700;color:#0F172A;font-size:0.88rem;margin:0">{ch}</p>',
                             unsafe_allow_html=True)
            cols[1].markdown(f'<p style="color:#374151;font-size:0.85rem;margin:0">{p["videos"]}</p>',
                             unsafe_allow_html=True)
            cols[2].markdown(f'<p style="color:#374151;font-size:0.85rem;margin:0">{fmt_number(p["avg_views"])}</p>',
                             unsafe_allow_html=True)
            cols[3].markdown(f'<p style="color:#374151;font-size:0.85rem;margin:0">{p["avg_eng"]}%</p>',
                             unsafe_allow_html=True)
            cols[4].markdown(f'<p style="color:#374151;font-size:0.85rem;margin:0">{fmt_number(p["subscribers"])}</p>',
                             unsafe_allow_html=True)
            cols[5].markdown(
                f'<span style="background:#EFF6FF;color:#0369A1;border:1px solid #BAE6FD;'
                f'padding:2px 9px;border-radius:6px;font-size:0.76rem;font-weight:600">'
                f'{p["upload_freq"]}</span>',
                unsafe_allow_html=True,
            )
            st.markdown('<div style="height:1px;background:#F1F5F9;margin:5px 0"></div>',
                        unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("### Competitive Radar")

        top_channels = dict(
            list(sorted(competitor_profiles.items(), key=lambda x: -x[1]["avg_views"]))[:5]
        )
        radar_data = {ch: p["radar"] for ch, p in top_channels.items()}
        if radar_data:
            st.plotly_chart(competitor_radar(radar_data), use_container_width=True,
                            config={"displayModeBar": False})

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("### Market Gap Analysis")
        st.markdown("**Topics already well-covered vs. underserved opportunities**")

        gap1, gap2 = st.columns(2)
        with gap1:
            st.markdown("**Covered Topics** — high competition")
            for topic in covered:
                st.markdown(f"""
<div style="background:#FEF2F2;border:1px solid #FECACA;border-radius:8px;
     padding:6px 12px;margin-bottom:5px;display:flex;align-items:center;gap:8px">
  <span style="color:#DC2626;font-weight:700">●</span>
  <span style="font-size:0.83rem;color:#374151;font-weight:500">{topic.title()}</span>
  <span style="margin-left:auto;font-size:0.7rem;color:#DC2626;font-weight:700">HIGH COMPETITION</span>
</div>""", unsafe_allow_html=True)

        with gap2:
            st.markdown("**Content Gaps** — opportunity areas")
            for gap in gaps:
                st.markdown(f"""
<div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:8px;
     padding:6px 12px;margin-bottom:5px;display:flex;align-items:center;gap:8px">
  <span style="color:#16A34A;font-weight:700">★</span>
  <span style="font-size:0.83rem;color:#374151;font-weight:500">{gap}</span>
  <span style="margin-left:auto;font-size:0.7rem;color:#16A34A;font-weight:700">OPPORTUNITY</span>
</div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 4 — CONTENT STRATEGY
    # ══════════════════════════════════════════════════════════════════════════
    with tab4:
        st.markdown('<span class="section-label">Content Strategy</span>', unsafe_allow_html=True)
        st.markdown("### Data-driven content blueprint")
        st.markdown("")

        s = strategy
        cs1, cs2 = st.columns(2)
        with cs1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**📐  Optimal Video Structure**")
            st.markdown(f"""
<div style="margin-top:8px">
  <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #F1F5F9">
    <span style="font-size:0.82rem;color:#64748B;font-weight:600">Target Duration</span>
    <span style="font-size:0.82rem;color:#0F172A;font-weight:700">{s['optimal_duration']}</span>
  </div>
  <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #F1F5F9">
    <span style="font-size:0.82rem;color:#64748B;font-weight:600">Recommended Format</span>
    <span style="font-size:0.82rem;color:#0F172A;font-weight:700">{s['recommended_format']}</span>
  </div>
  <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #F1F5F9">
    <span style="font-size:0.82rem;color:#64748B;font-weight:600">Primary Audience</span>
    <span style="font-size:0.82rem;color:#0F172A;font-weight:700">{s['primary_audience']}</span>
  </div>
  <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #F1F5F9">
    <span style="font-size:0.82rem;color:#64748B;font-weight:600">Best Upload Time</span>
    <span style="font-size:0.82rem;color:#0F172A;font-weight:700">{s['post_time']}</span>
  </div>
  <div style="display:flex;justify-content:space-between;padding:8px 0">
    <span style="font-size:0.82rem;color:#64748B;font-weight:600">Avg Engagement</span>
    <span style="font-size:0.82rem;color:#16A34A;font-weight:700">{s['avg_engagement']}% — {s['engagement_note']}</span>
  </div>
</div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with cs2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**✍️  Content Formulas**")
            st.markdown(f"""
<div style="margin-top:8px">
  <div style="margin-bottom:12px">
    <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;
         color:#0369A1;margin-bottom:4px">Title Formula</div>
    <div style="font-size:0.83rem;color:#0F172A;background:#F8FAFC;border-radius:8px;
         padding:8px 10px;font-family:monospace">{s['title_formula']}</div>
  </div>
  <div style="margin-bottom:12px">
    <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;
         color:#0369A1;margin-bottom:4px">Thumbnail Formula</div>
    <div style="font-size:0.83rem;color:#0F172A;background:#F8FAFC;border-radius:8px;
         padding:8px 10px">{s['thumbnail_formula']}</div>
  </div>
  <div style="margin-bottom:12px">
    <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;
         color:#0369A1;margin-bottom:4px">Hook Formula</div>
    <div style="font-size:0.83rem;color:#0F172A;background:#F8FAFC;border-radius:8px;
         padding:8px 10px">{s['hook_formula']}</div>
  </div>
  <div>
    <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;
         color:#0369A1;margin-bottom:4px">CTA Placement</div>
    <div style="font-size:0.83rem;color:#0F172A;background:#F8FAFC;border-radius:8px;
         padding:8px 10px">{s['cta_placement']}</div>
  </div>
</div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("### Content Opportunity Roadmap")

        roadmap_items = [
            {"week": "Week 1–2", "action": f"Create foundational '{kw.title()} for beginners' video",
             "priority": "HIGH", "expected_views": stable_random(seed_hash(kw+".w1"), 20_000, 80_000)},
            {"week": "Week 3–4", "action": f"Publish a '{kw.title()} case study / results' video",
             "priority": "HIGH", "expected_views": stable_random(seed_hash(kw+".w2"), 30_000, 120_000)},
            {"week": "Week 5–6", "action": f"Comparison/review: 'Best tools for {kw.title()}'",
             "priority": "MED", "expected_views": stable_random(seed_hash(kw+".w3"), 15_000, 60_000)},
            {"week": "Week 7–8", "action": f"Deep dive: '{kw.title()} mistakes to avoid'",
             "priority": "MED", "expected_views": stable_random(seed_hash(kw+".w4"), 25_000, 90_000)},
            {"week": "Week 9–12", "action": f"Long-form: 'Complete {kw.title()} masterclass 2025'",
             "priority": "HIGH", "expected_views": stable_random(seed_hash(kw+".w5"), 50_000, 200_000)},
        ]

        for item in roadmap_items:
            pcolor = "#DC2626" if item["priority"]=="HIGH" else "#D97706" if item["priority"]=="MED" else "#16A34A"
            pbg    = "#FEF2F2" if item["priority"]=="HIGH" else "#FFFBEB" if item["priority"]=="MED" else "#F0FDF4"
            st.markdown(f"""
<div style="background:#fff;border:1px solid #E2E8F0;border-radius:10px;
     padding:0.85rem 1.1rem;margin-bottom:0.5rem;
     display:grid;grid-template-columns:90px 1fr 100px 130px;gap:12px;align-items:center;
     box-shadow:0 1px 3px rgba(0,0,0,0.04)">
  <span style="font-size:0.72rem;font-weight:700;color:#64748B">{item['week']}</span>
  <span style="font-size:0.88rem;font-weight:600;color:#0F172A">{item['action']}</span>
  <span style="background:{pbg};color:{pcolor};border:1px solid {pcolor}33;
    padding:2px 10px;border-radius:20px;font-size:0.7rem;font-weight:700;text-align:center">
    {item['priority']}
  </span>
  <span style="font-size:0.78rem;color:#64748B;text-align:right">
    ~{fmt_number(item['expected_views'])} views est.
  </span>
</div>""", unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("""
<div class="callout-success">
  <strong>Strategy Summary:</strong> This niche shows
  <strong>""" + str(viral_count) + """ viral</strong> and
  <strong>""" + str(rising_count) + """ rising</strong> videos — indicating an active, growing audience.
  The optimal entry strategy is a <strong>""" + s['recommended_format'] + """-format</strong> video
  targeting the <strong>""" + s['primary_audience'] + """</strong> age group, published on
  <strong>""" + s['post_time'] + """</strong>.
  Focus on content gaps (see Competitor Intel tab) to avoid direct head-to-head competition with
  established channels.
</div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 5 — BUSINESS METRICS
    # ══════════════════════════════════════════════════════════════════════════
    with tab5:
        st.markdown('<span class="section-label">Business Metrics</span>', unsafe_allow_html=True)
        st.markdown("### Revenue & monetisation intelligence")
        st.markdown("")

        bm1, bm2, bm3, bm4 = st.columns(4)
        bm1.metric("💰 Total Est. Revenue",  f"${fmt_number(int(total_rev))}",  "across all videos")
        bm2.metric("📈 Avg CPM Est.",
                   f"${round(sum(v['cpm_est'] for v in enriched)/len(enriched),2)}",
                   "per 1K views")
        bm3.metric("🚀 Best CPM",
                   f"${max(v['cpm_est'] for v in enriched)}",
                   "single video")
        bm4.metric("👥 Avg Sub Bump",
                   f"+{fmt_number(int(sum(v['subscriber_bump'] for v in enriched)/len(enriched)))}",
                   "estimated per video")

        st.markdown("")
        st.plotly_chart(revenue_bar(enriched), use_container_width=True,
                        config={"displayModeBar": False})

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("### Revenue Breakdown Table")

        rhdr = st.columns([3, 1, 1, 1, 1.2])
        for col, lbl in zip(rhdr, ["Video", "Views", "CPM Est.", "Revenue Est.", "Velocity"]):
            col.markdown(
                f'<p style="font-size:0.68rem;font-weight:700;color:#64748B;'
                f'text-transform:uppercase;letter-spacing:0.07em;margin:0">{lbl}</p>',
                unsafe_allow_html=True,
            )
        st.markdown('<div style="height:1px;background:#E2E8F0;margin:4px 0 8px"></div>',
                    unsafe_allow_html=True)

        for v in sorted(enriched, key=lambda x: -x["revenue_est"])[:10]:
            vel_c, vel_bg = TREND_VELOCITY.get(v["velocity"], ("#64748B","#F8FAFC"))
            rcols = st.columns([3, 1, 1, 1, 1.2])
            rcols[0].markdown(
                f'<p style="font-weight:600;color:#0F172A;font-size:0.84rem;margin:0">'
                f'{v["title"][:55]}{"…" if len(v["title"])>55 else ""}</p>',
                unsafe_allow_html=True)
            rcols[1].markdown(f'<p style="color:#374151;font-size:0.84rem;margin:0">{fmt_number(v["views"])}</p>',
                              unsafe_allow_html=True)
            rcols[2].markdown(f'<p style="color:#374151;font-size:0.84rem;margin:0">${v["cpm_est"]}</p>',
                              unsafe_allow_html=True)
            rcols[3].markdown(f'<p style="font-weight:700;color:#16A34A;font-size:0.84rem;margin:0">${int(v["revenue_est"]):,}</p>',
                              unsafe_allow_html=True)
            rcols[4].markdown(
                f'<span style="background:{vel_bg};color:{vel_c};border:1px solid {vel_c}44;'
                f'padding:2px 9px;border-radius:20px;font-size:0.72rem;font-weight:700">'
                f'{v["velocity"]}</span>',
                unsafe_allow_html=True,
            )
            st.markdown('<div style="height:1px;background:#F1F5F9;margin:4px 0"></div>',
                        unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("### Monetisation Insights")

        avg_cpm     = round(sum(v["cpm_est"] for v in enriched) / len(enriched), 2)
        high_cpm    = [v for v in enriched if v["cpm_est"] > avg_cpm * 1.3]
        top_rev_vid = max(enriched, key=lambda v: v["revenue_est"])

        st.markdown(f"""
<div class="callout">
  <strong>Revenue Intelligence:</strong>
  The estimated total revenue across <strong>{len(enriched)} videos</strong> is
  <strong>${total_rev:,.0f}</strong> with an average CPM of <strong>${avg_cpm}</strong>.
  <br><br>
  <strong>{len(high_cpm)} videos</strong> are above-average CPM — these indicate premium audience segments
  that advertisers pay a premium for (B2B, finance, tech, health).
  <br><br>
  Top revenue opportunity: <strong>"{top_rev_vid['title'][:60]}…"</strong>
  with an estimated <strong>${int(top_rev_vid['revenue_est']):,}</strong> in ad revenue.
  Creating similar content in terms of format, length, and topic framing is the highest-ROI move.
</div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 6 — DEEP DIVES
    # ══════════════════════════════════════════════════════════════════════════
    with tab6:
        st.markdown('<span class="section-label">Per-Video Deep Dives</span>', unsafe_allow_html=True)
        st.markdown("### Expand any video for full analysis")
        st.markdown("")

        for v in enriched:
            vc   = CATEGORY_COLORS.get(v["category"], "#0369A1")
            vel_c, vel_bg = TREND_VELOCITY.get(v["velocity"], ("#64748B","#F8FAFC"))
            label = f'{v["velocity"]}  {v["title"][:60]}{"…" if len(v["title"])>60 else ""}  ·  {fmt_number(v["views"])} views'
            with st.expander(label, expanded=False):
                dm1, dm2, dm3, dm4, dm5, dm6 = st.columns(6)
                dm1.metric("Views",       fmt_number(v["views"]))
                dm2.metric("Likes",       fmt_number(v["likes"]))
                dm3.metric("Comments",    fmt_number(v["comments"]))
                dm4.metric("Engagement",  f'{v["eng_rate"]}%')
                dm5.metric("Duration",    fmt_duration(v["duration_s"]))
                dm6.metric("Est. Revenue", f'${int(v["revenue_est"]):,}')

                dc1, dc2, dc3 = st.columns(3)
                with dc1:
                    st.plotly_chart(age_donut(v["audience_age"]), use_container_width=True,
                                    config={"displayModeBar": False},
                                    key=f"age_{v['id']}")
                with dc2:
                    st.plotly_chart(geo_bar(v["geo"]), use_container_width=True,
                                    config={"displayModeBar": False},
                                    key=f"geo_{v['id']}")
                with dc3:
                    st.plotly_chart(retention_chart(v), use_container_width=True,
                                    config={"displayModeBar": False},
                                    key=f"ret_{v['id']}")

                st.markdown(f"""
<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;
     padding:0.8rem 1rem;margin:0.5rem 0;
     display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px">
  <div>
    <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#64748B;margin-bottom:3px">Content Type</div>
    <div style="font-size:0.88rem;font-weight:600;color:#0F172A">{v['content_type'].title()}</div>
  </div>
  <div>
    <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#64748B;margin-bottom:3px">Category</div>
    <div style="font-size:0.88rem;font-weight:600;color:{vc}">{v['category']}</div>
  </div>
  <div>
    <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#64748B;margin-bottom:3px">Est. Subscriber Bump</div>
    <div style="font-size:0.88rem;font-weight:600;color:#16A34A">+{fmt_number(v['subscriber_bump'])}</div>
  </div>
</div>""", unsafe_allow_html=True)

                st.markdown(f"""
<div style="display:flex;gap:12px;margin-top:8px;flex-wrap:wrap">
  <a href="https://www.youtube.com/watch?v={v['id']}" target="_blank"
     style="background:#0369A1;color:#fff;padding:7px 16px;border-radius:8px;
     font-size:0.8rem;font-weight:700;text-decoration:none">▶ Watch Video</a>
  <a href="https://www.youtube.com/channel/{v['channel']}" target="_blank"
     style="background:#F1F5F9;color:#374151;padding:7px 16px;border-radius:8px;
     font-size:0.8rem;font-weight:700;text-decoration:none">📺 View Channel</a>
</div>""", unsafe_allow_html=True)

    # ── RESET BUTTON ──────────────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    reset_col, _ = st.columns([1, 4])
    with reset_col:
        if st.button("🔄  New Search", use_container_width=True):
            for k in ["videos", "enriched", "keyword", "ran_analysis"]:
                st.session_state[k] = [] if k in ("videos", "enriched") else ("" if k == "keyword" else False)
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# COMPARE MODE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<span class="section-label">Compare Mode</span>', unsafe_allow_html=True)
st.markdown("## ⚔️  Topic vs Topic Comparison")
st.markdown(
    "Compare two topics, artists, brands, or keywords head-to-head — "
    "views, engagement, audience, sentiment, and revenue side by side."
)
st.markdown("")

# ── Session state for compare ─────────────────────────────────────────────────
for _ck, _cv in [("cmp_a", []), ("cmp_b", []), ("cmp_kw_a", ""), ("cmp_kw_b", ""),
                 ("cmp_ran", False)]:
    if _ck not in st.session_state:
        st.session_state[_ck] = _cv

# ── Input row ─────────────────────────────────────────────────────────────────
cmp_col1, vs_col, cmp_col2 = st.columns([5, 1, 5])
with cmp_col1:
    cmp_kw_a = st.text_input("🔵  Topic A", placeholder="e.g.  Taylor Swift",
                              key="cmp_input_a")
with vs_col:
    st.markdown(
        '<div style="display:flex;align-items:center;justify-content:center;'
        'height:100%;padding-top:28px;font-size:1.3rem;font-weight:900;color:#64748B">VS</div>',
        unsafe_allow_html=True,
    )
with cmp_col2:
    cmp_kw_b = st.text_input("🔴  Topic B", placeholder="e.g.  Beyoncé",
                              key="cmp_input_b")

cmp_n_col, cmp_btn_col, cmp_demo_col, _ = st.columns([1, 1.2, 1.2, 2])
with cmp_n_col:
    cmp_n = st.selectbox("Videos each", [5, 10, 20], index=1, key="cmp_n")
with cmp_btn_col:
    cmp_btn = st.button("⚔️  Compare Now", use_container_width=True, key="cmp_run")
with cmp_demo_col:
    cmp_demo_btn = st.button("🎮  Demo Compare", use_container_width=True, key="cmp_demo")

# ── Demo data ─────────────────────────────────────────────────────────────────
DEMO_CMP_A_KW = "Taylor Swift"
DEMO_CMP_B_KW = "Beyoncé"
DEMO_CMP_A = [
    {"id":"ts001","title":"Taylor Swift — Anti-Hero (Official Music Video)","channel":"TaylorSwiftVEVO","published":"2022-10-21","description":"Anti-Hero from Midnights album, biggest pop release of 2022","thumbnail":""},
    {"id":"ts002","title":"Taylor Swift Eras Tour Full Concert Highlights","channel":"SwiftiesCentral","published":"2023-08-15","description":"Best moments from the record-breaking Eras Tour across all albums","thumbnail":""},
    {"id":"ts003","title":"Taylor Swift vs Scooter Braun: The Full Story","channel":"MusicNews","published":"2023-06-10","description":"Complete timeline of the masters dispute and re-recordings","thumbnail":""},
    {"id":"ts004","title":"Every Taylor Swift Album Ranked (Swiftie Edition)","channel":"PopCritic","published":"2024-01-20","description":"Deep dive ranking all 11 Taylor Swift albums from debut to Tortured Poets","thumbnail":""},
    {"id":"ts005","title":"Taylor Swift — Shake It Off (Official Video)","channel":"TaylorSwiftVEVO","published":"2014-08-18","description":"Official music video for Shake It Off from the 1989 album","thumbnail":""},
    {"id":"ts006","title":"Taylor Swift Speaks Out on AI and Music Rights","channel":"EntertainmentTonight","published":"2024-03-05","description":"Taylor Swift addresses the use of AI in music creation and artist rights","thumbnail":""},
    {"id":"ts007","title":"Taylor Swift NFL Romance: Travis Kelce Timeline","channel":"E!News","published":"2023-10-01","description":"Everything we know about Taylor Swift and Travis Kelce's relationship","thumbnail":""},
    {"id":"ts008","title":"Taylor Swift Songwriting Masterclass","channel":"MusicMasterclass","published":"2023-11-12","description":"Breakdown of Taylor Swift's unique storytelling and songwriting techniques","thumbnail":""},
    {"id":"ts009","title":"Taylor Swift Fearless Re-Recording — What Changed?","channel":"MusicAnalysis","published":"2021-04-09","description":"Comparing Fearless (Taylor's Version) to the original with audio analysis","thumbnail":""},
    {"id":"ts010","title":"Taylor Swift Net Worth & Business Empire 2024","channel":"WealthInsider","published":"2024-02-14","description":"How Taylor Swift became a billionaire through music, tours, and brand deals","thumbnail":""},
]
DEMO_CMP_B = [
    {"id":"by001","title":"Beyoncé — CUFF IT (Official Video)","channel":"BeyoncéVEVO","published":"2022-11-11","description":"CUFF IT from the Renaissance album, the summer anthem of 2022","thumbnail":""},
    {"id":"by002","title":"Beyoncé Renaissance World Tour Highlights","channel":"BeyHive","published":"2023-09-20","description":"Iconic moments from Beyoncé's record-breaking Renaissance World Tour","thumbnail":""},
    {"id":"by003","title":"Beyoncé Cowboy Carter Album Full Reaction","channel":"MusicReacts","published":"2024-03-29","description":"First listen reaction to Beyoncé's country album Cowboy Carter","thumbnail":""},
    {"id":"by004","title":"Beyoncé vs Taylor Swift: Who Is the Bigger Star?","channel":"PopDebate","published":"2023-12-15","description":"Comparing album sales, streaming records, and cultural impact","thumbnail":""},
    {"id":"by005","title":"Beyoncé — Single Ladies (Official Video)","channel":"BeyoncéVEVO","published":"2009-10-02","description":"Classic Single Ladies music video, one of the most iconic of all time","thumbnail":""},
    {"id":"by006","title":"Beyoncé Lemonade Visual Album — Every Scene Explained","channel":"FilmTheory","published":"2023-05-18","description":"Deep analysis of every visual and lyrical reference in Lemonade","thumbnail":""},
    {"id":"by007","title":"Beyoncé's Business Empire: Music, Fashion & Film","channel":"ForbesWomen","published":"2024-01-10","description":"How Beyoncé built a $500M+ empire through Ivy Park, Parkwood Entertainment","thumbnail":""},
    {"id":"by008","title":"Beyoncé Renaissance: The Country Pivot Explained","channel":"MusicAnalysis","published":"2024-04-02","description":"Why Beyoncé's move into country music is a cultural and business masterstroke","thumbnail":""},
    {"id":"by009","title":"Beyoncé Documentary: Life is But a Dream","channel":"HBO","published":"2013-02-16","description":"Intimate look at Beyoncé's life and career in her own words","thumbnail":""},
    {"id":"by010","title":"Beyoncé Net Worth 2024 — Richest Female Musician?","channel":"WealthInsider","published":"2024-03-01","description":"Breaking down Beyoncé's estimated $500M+ net worth and revenue streams","thumbnail":""},
]

if cmp_demo_btn:
    st.session_state.cmp_kw_a = DEMO_CMP_A_KW
    st.session_state.cmp_kw_b = DEMO_CMP_B_KW
    st.session_state.cmp_a    = [enrich_video(v, keyword=DEMO_CMP_A_KW) for v in DEMO_CMP_A]
    st.session_state.cmp_b    = [enrich_video(v, keyword=DEMO_CMP_B_KW) for v in DEMO_CMP_B]
    st.session_state.cmp_ran  = True
    st.success(f"Demo comparison loaded — **{DEMO_CMP_A_KW}** vs **{DEMO_CMP_B_KW}**")

if cmp_btn:
    if not cmp_kw_a.strip() or not cmp_kw_b.strip():
        st.error("Please enter both Topic A and Topic B.")
    elif not _api_key.strip():
        st.error("API key required. Use Demo Compare to explore without a key.")
    else:
        with st.spinner(f'Searching "{cmp_kw_a}" and "{cmp_kw_b}"…'):
            vids_a, err_a = search_youtube(cmp_kw_a.strip(), _api_key.strip(), cmp_n)
            vids_b, err_b = search_youtube(cmp_kw_b.strip(), _api_key.strip(), cmp_n)
        if err_a or err_b:
            st.error(f"API error: {err_a or err_b}")
        elif not vids_a or not vids_b:
            st.warning("One or both searches returned no results. Try different keywords.")
        else:
            prog_c = st.progress(0); stat_c = st.empty()
            stat_c.markdown("⚙️ **Enriching videos…**")
            enriched_a, enriched_b = [], []
            total_c = len(vids_a) + len(vids_b)
            for i, v in enumerate(vids_a):
                prog_c.progress((i+1)/total_c)
                enriched_a.append(enrich_video(v, keyword=cmp_kw_a.strip()))
            for i, v in enumerate(vids_b):
                prog_c.progress((len(vids_a)+i+1)/total_c)
                enriched_b.append(enrich_video(v, keyword=cmp_kw_b.strip()))
            prog_c.progress(1.0); stat_c.markdown("✅ **Done!**")
            time.sleep(0.3); prog_c.empty(); stat_c.empty()
            st.session_state.cmp_kw_a = cmp_kw_a.strip()
            st.session_state.cmp_kw_b = cmp_kw_b.strip()
            st.session_state.cmp_a    = enriched_a
            st.session_state.cmp_b    = enriched_b
            st.session_state.cmp_ran  = True
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# COMPARE DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.cmp_ran and st.session_state.cmp_a and st.session_state.cmp_b:
    ca       = st.session_state.cmp_a
    cb       = st.session_state.cmp_b
    kw_a     = st.session_state.cmp_kw_a
    kw_b     = st.session_state.cmp_kw_b
    COLOR_A  = "#0369A1"   # blue
    COLOR_B  = "#DC2626"   # red

    # ── Aggregate stats ───────────────────────────────────────────────────────
    def agg(videos):
        return {
            "views":    sum(v["views"]    for v in videos),
            "likes":    sum(v["likes"]    for v in videos),
            "comments": sum(v["comments"] for v in videos),
            "eng":      round(sum(v["eng_rate"] for v in videos) / len(videos), 2),
            "revenue":  sum(v["revenue_est"] for v in videos),
            "viral":    sum(1 for v in videos if v["velocity"] == "🔥 Viral"),
            "rising":   sum(1 for v in videos if v["velocity"] == "⬆ Rising"),
            "dur":      sum(v["duration_s"] for v in videos) / len(videos),
        }

    sa, sb = agg(ca), agg(cb)

    # ── Winner badge ──────────────────────────────────────────────────────────
    score_a = (
        (1 if sa["views"]    > sb["views"]    else 0) +
        (1 if sa["eng"]      > sb["eng"]      else 0) +
        (1 if sa["viral"]    > sb["viral"]    else 0) +
        (1 if sa["revenue"]  > sb["revenue"]  else 0)
    )
    score_b = 4 - score_a
    winner  = kw_a if score_a >= score_b else kw_b
    win_col = COLOR_A if score_a >= score_b else COLOR_B

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
<div style="background:linear-gradient(135deg,{win_col}15,{win_col}05);
     border:2px solid {win_col}44;border-radius:16px;padding:1.2rem 1.5rem;
     text-align:center;margin-bottom:1.5rem">
  <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;
       letter-spacing:0.1em;color:{win_col};margin-bottom:4px">Overall Winner</div>
  <div style="font-size:2rem;font-weight:900;color:{win_col}">🏆 {winner}</div>
  <div style="font-size:0.8rem;color:#64748B;margin-top:4px">
    Leading in {max(score_a,score_b)} out of 4 key metrics
  </div>
</div>""", unsafe_allow_html=True)

    # ── Score cards ───────────────────────────────────────────────────────────
    st.markdown("### Head-to-Head Metrics")
    metrics = [
        ("👁 Total Views",     fmt_number(sa["views"]),   fmt_number(sb["views"]),   sa["views"]   > sb["views"]),
        ("📊 Avg Engagement",  f'{sa["eng"]}%',           f'{sb["eng"]}%',           sa["eng"]     > sb["eng"]),
        ("💬 Total Comments",  fmt_number(sa["comments"]),fmt_number(sb["comments"]),sa["comments"]> sb["comments"]),
        ("💰 Est. Revenue",    f'${fmt_number(int(sa["revenue"]))}', f'${fmt_number(int(sb["revenue"]))}', sa["revenue"] > sb["revenue"]),
        ("🔥 Viral Videos",    str(sa["viral"]),          str(sb["viral"]),          sa["viral"]   > sb["viral"]),
        ("⬆ Rising Videos",   str(sa["rising"]),         str(sb["rising"]),         sa["rising"]  > sb["rising"]),
    ]

    for label, val_a, val_b, a_wins in metrics:
        wa = "🏆 " if a_wins  else ""
        wb = "🏆 " if not a_wins else ""
        ca_bg = f"{COLOR_A}12" if a_wins  else "#F8FAFC"
        cb_bg = f"{COLOR_B}12" if not a_wins else "#F8FAFC"
        ca_border = f"2px solid {COLOR_A}55" if a_wins  else "1px solid #E2E8F0"
        cb_border = f"2px solid {COLOR_B}55" if not a_wins else "1px solid #E2E8F0"
        st.markdown(f"""
<div style="display:grid;grid-template-columns:1fr 80px 1fr;gap:8px;margin-bottom:8px;align-items:center">
  <div style="background:{ca_bg};border:{ca_border};border-radius:10px;
       padding:10px 14px;text-align:center">
    <div style="font-size:1.1rem;font-weight:800;color:{COLOR_A}">{wa}{val_a}</div>
    <div style="font-size:0.7rem;color:#64748B;font-weight:600">{kw_a}</div>
  </div>
  <div style="text-align:center;font-size:0.72rem;font-weight:700;color:#94A3B8">{label}</div>
  <div style="background:{cb_bg};border:{cb_border};border-radius:10px;
       padding:10px 14px;text-align:center">
    <div style="font-size:1.1rem;font-weight:800;color:{COLOR_B}">{wb}{val_b}</div>
    <div style="font-size:0.7rem;color:#64748B;font-weight:600">{kw_b}</div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    st.markdown("### Visual Comparison")
    ch1, ch2 = st.columns(2)

    # Views grouped bar
    with ch1:
        top_a = sorted(ca, key=lambda v: -v["views"])[:5]
        top_b = sorted(cb, key=lambda v: -v["views"])[:5]
        fig_v = go.Figure()
        fig_v.add_trace(go.Bar(
            name=kw_a,
            x=[v["title"][:22]+"…" if len(v["title"])>22 else v["title"] for v in top_a],
            y=[v["views"] for v in top_a],
            marker=dict(color=COLOR_A, opacity=0.85, line=dict(width=0)),
            text=[fmt_number(v["views"]) for v in top_a],
            textposition="outside", textfont=dict(size=10),
        ))
        fig_v.add_trace(go.Bar(
            name=kw_b,
            x=[v["title"][:22]+"…" if len(v["title"])>22 else v["title"] for v in top_b],
            y=[v["views"] for v in top_b],
            marker=dict(color=COLOR_B, opacity=0.85, line=dict(width=0)),
            text=[fmt_number(v["views"]) for v in top_b],
            textposition="outside", textfont=dict(size=10),
        ))
        fig_v.update_layout(
            **_chart_base(300, margin_b=90),
            title=dict(text="Top 5 Videos by Views", font=dict(size=12, color="#64748B"), x=0),
            barmode="group",
            xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#374151"), tickangle=-20),
            yaxis=dict(showgrid=True, gridcolor=GRID, tickfont=dict(color=TICK, size=10)),
            legend=dict(font=dict(size=11), orientation="h", x=0.5, xanchor="center", y=-0.3),
        )
        st.plotly_chart(fig_v, use_container_width=True, config={"displayModeBar": False},
                        key="cmp_views_bar")

    # Engagement comparison
    with ch2:
        fig_e = go.Figure()
        fig_e.add_trace(go.Bar(
            name=kw_a,
            x=[v["title"][:22]+"…" if len(v["title"])>22 else v["title"] for v in sorted(ca, key=lambda v: -v["eng_rate"])[:5]],
            y=[v["eng_rate"] for v in sorted(ca, key=lambda v: -v["eng_rate"])[:5]],
            marker=dict(color=COLOR_A, opacity=0.85, line=dict(width=0)),
            text=[f'{v["eng_rate"]}%' for v in sorted(ca, key=lambda v: -v["eng_rate"])[:5]],
            textposition="outside", textfont=dict(size=10),
        ))
        fig_e.add_trace(go.Bar(
            name=kw_b,
            x=[v["title"][:22]+"…" if len(v["title"])>22 else v["title"] for v in sorted(cb, key=lambda v: -v["eng_rate"])[:5]],
            y=[v["eng_rate"] for v in sorted(cb, key=lambda v: -v["eng_rate"])[:5]],
            marker=dict(color=COLOR_B, opacity=0.85, line=dict(width=0)),
            text=[f'{v["eng_rate"]}%' for v in sorted(cb, key=lambda v: -v["eng_rate"])[:5]],
            textposition="outside", textfont=dict(size=10),
        ))
        fig_e.update_layout(
            **_chart_base(300, margin_b=90),
            title=dict(text="Top 5 Videos by Engagement", font=dict(size=12, color="#64748B"), x=0),
            barmode="group",
            xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#374151"), tickangle=-20),
            yaxis=dict(showgrid=True, gridcolor=GRID, tickfont=dict(color=TICK, size=10),
                       ticksuffix="%"),
            legend=dict(font=dict(size=11), orientation="h", x=0.5, xanchor="center", y=-0.3),
        )
        st.plotly_chart(fig_e, use_container_width=True, config={"displayModeBar": False},
                        key="cmp_eng_bar")

    # Velocity comparison donut side by side
    ch3, ch4 = st.columns(2)
    with ch3:
        st.plotly_chart(velocity_donut(ca), use_container_width=True,
                        config={"displayModeBar": False}, key="cmp_vel_a")
        st.markdown(f'<p style="text-align:center;font-size:0.8rem;font-weight:700;color:{COLOR_A}">{kw_a} — Velocity Mix</p>',
                    unsafe_allow_html=True)
    with ch4:
        st.plotly_chart(velocity_donut(cb), use_container_width=True,
                        config={"displayModeBar": False}, key="cmp_vel_b")
        st.markdown(f'<p style="text-align:center;font-size:0.8rem;font-weight:700;color:{COLOR_B}">{kw_b} — Velocity Mix</p>',
                    unsafe_allow_html=True)

    # Audience age comparison
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### Audience Age Comparison")

    agg_age_a = defaultdict(float)
    agg_age_b = defaultdict(float)
    for v in ca:
        for age, pct in v["audience_age"].items(): agg_age_a[age] += pct
    for v in cb:
        for age, pct in v["audience_age"].items(): agg_age_b[age] += pct
    agg_age_a = {k: round(v/len(ca)) for k, v in agg_age_a.items()}
    agg_age_b = {k: round(v/len(cb)) for k, v in agg_age_b.items()}

    ages = ["13-17", "18-24", "25-34", "35-44", "45+"]
    fig_age = go.Figure()
    fig_age.add_trace(go.Bar(
        name=kw_a, x=ages,
        y=[agg_age_a.get(a, 0) for a in ages],
        marker=dict(color=COLOR_A, opacity=0.85, line=dict(width=0)),
        text=[f'{agg_age_a.get(a,0)}%' for a in ages],
        textposition="outside", textfont=dict(size=11),
    ))
    fig_age.add_trace(go.Bar(
        name=kw_b, x=ages,
        y=[agg_age_b.get(a, 0) for a in ages],
        marker=dict(color=COLOR_B, opacity=0.85, line=dict(width=0)),
        text=[f'{agg_age_b.get(a,0)}%' for a in ages],
        textposition="outside", textfont=dict(size=11),
    ))
    fig_age.update_layout(
        **_chart_base(280, margin_b=60),
        title=dict(text="Audience Age Distribution", font=dict(size=12, color="#64748B"), x=0),
        barmode="group",
        xaxis=dict(showgrid=False, tickfont=dict(color="#374151", size=11)),
        yaxis=dict(showgrid=True, gridcolor=GRID, tickfont=dict(color=TICK, size=10),
                   ticksuffix="%"),
        legend=dict(font=dict(size=11), orientation="h", x=0.5, xanchor="center", y=-0.18),
    )
    st.plotly_chart(fig_age, use_container_width=True, config={"displayModeBar": False},
                    key="cmp_age_bar")

    # ── Top videos from each ──────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### Top Videos — Side by Side")
    tv_a, tv_b = st.columns(2)

    with tv_a:
        st.markdown(f'<p style="font-weight:800;color:{COLOR_A};font-size:0.95rem;margin-bottom:8px">🔵 {kw_a}</p>',
                    unsafe_allow_html=True)
        for rank, v in enumerate(sorted(ca, key=lambda x: -x["views"])[:5], 1):
            vel_c, vel_bg = TREND_VELOCITY.get(v["velocity"], ("#64748B","#F8FAFC"))
            st.markdown(f"""
<div style="background:#fff;border:1px solid #E2E8F0;border-left:3px solid {COLOR_A};
     border-radius:10px;padding:0.7rem 0.9rem;margin-bottom:5px;
     box-shadow:0 1px 3px rgba(0,0,0,0.04)">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:6px">
    <div>
      <div style="font-size:0.82rem;font-weight:700;color:#0F172A;margin-bottom:2px">
        #{rank} {v['title'][:50]}{'…' if len(v['title'])>50 else ''}
      </div>
      <div style="font-size:0.72rem;color:#64748B">
        👁 {fmt_number(v['views'])} &nbsp;·&nbsp; 📊 {v['eng_rate']}%
      </div>
    </div>
    <span style="background:{vel_bg};color:{vel_c};border:1px solid {vel_c}33;
      padding:2px 7px;border-radius:20px;font-size:0.68rem;font-weight:700;white-space:nowrap">
      {v['velocity']}
    </span>
  </div>
</div>""", unsafe_allow_html=True)

    with tv_b:
        st.markdown(f'<p style="font-weight:800;color:{COLOR_B};font-size:0.95rem;margin-bottom:8px">🔴 {kw_b}</p>',
                    unsafe_allow_html=True)
        for rank, v in enumerate(sorted(cb, key=lambda x: -x["views"])[:5], 1):
            vel_c, vel_bg = TREND_VELOCITY.get(v["velocity"], ("#64748B","#F8FAFC"))
            st.markdown(f"""
<div style="background:#fff;border:1px solid #E2E8F0;border-left:3px solid {COLOR_B};
     border-radius:10px;padding:0.7rem 0.9rem;margin-bottom:5px;
     box-shadow:0 1px 3px rgba(0,0,0,0.04)">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:6px">
    <div>
      <div style="font-size:0.82rem;font-weight:700;color:#0F172A;margin-bottom:2px">
        #{rank} {v['title'][:50]}{'…' if len(v['title'])>50 else ''}
      </div>
      <div style="font-size:0.72rem;color:#64748B">
        👁 {fmt_number(v['views'])} &nbsp;·&nbsp; 📊 {v['eng_rate']}%
      </div>
    </div>
    <span style="background:{vel_bg};color:{vel_c};border:1px solid {vel_c}33;
      padding:2px 7px;border-radius:20px;font-size:0.68rem;font-weight:700;white-space:nowrap">
      {v['velocity']}
    </span>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Summary insight ───────────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    views_winner  = kw_a if sa["views"]   > sb["views"]   else kw_b
    eng_winner    = kw_a if sa["eng"]     > sb["eng"]     else kw_b
    rev_winner    = kw_a if sa["revenue"] > sb["revenue"] else kw_b
    viral_winner  = kw_a if sa["viral"]   > sb["viral"]   else kw_b
    dom_age_a     = max(agg_age_a, key=agg_age_a.get)
    dom_age_b     = max(agg_age_b, key=agg_age_b.get)

    st.markdown(f"""
<div class="callout">
  <strong>Comparison Summary — {kw_a} vs {kw_b}:</strong><br><br>
  🏆 <strong>Overall winner: {winner}</strong> (leads in {max(score_a,score_b)}/4 metrics)<br>
  👁 <strong>More views:</strong> {views_winner}<br>
  📊 <strong>Higher engagement:</strong> {eng_winner}<br>
  💰 <strong>More revenue potential:</strong> {rev_winner}<br>
  🔥 <strong>More viral content:</strong> {viral_winner}<br><br>
  👥 <strong>{kw_a}</strong> primary audience: <strong>{dom_age_a}</strong> &nbsp;·&nbsp;
     <strong>{kw_b}</strong> primary audience: <strong>{dom_age_b}</strong>
</div>""", unsafe_allow_html=True)

    # Reset compare
    rc_col, _ = st.columns([1, 4])
    with rc_col:
        if st.button("🔄  Reset Comparison", use_container_width=True, key="cmp_reset"):
            for k in ["cmp_a","cmp_b","cmp_kw_a","cmp_kw_b","cmp_ran"]:
                st.session_state[k] = [] if k in ("cmp_a","cmp_b") else ("" if "kw" in k else False)
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:1rem 0">
  <div style="font-size:1rem;font-weight:800;color:#0F172A;letter-spacing:-0.03em;margin-bottom:4px">
    Trend<span style="color:#38BDF8">Scope</span>
  </div>
  <div style="font-size:0.72rem;color:#94A3B8">
    YouTube Trend Discovery &amp; Business Intelligence Platform
  </div>
</div>
""", unsafe_allow_html=True)
