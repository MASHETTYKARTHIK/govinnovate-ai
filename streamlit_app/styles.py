"""Shared futuristic dark theme for the Streamlit interface."""

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
  background:
    radial-gradient(circle at 15% 5%, rgba(0, 194, 255, .16), transparent 28%),
    radial-gradient(circle at 85% 0%, rgba(112, 74, 255, .18), transparent 30%),
    #070b17;
  color: #e7edf8;
}
[data-testid="stSidebar"] {
  background: rgba(8, 14, 29, .92);
  border-right: 1px solid rgba(111, 207, 255, .16);
}
[data-testid="stMetric"] {
  background: linear-gradient(145deg, rgba(20, 31, 57, .82), rgba(10, 18, 36, .72));
  border: 1px solid rgba(111, 207, 255, .2);
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 12px 40px rgba(0,0,0,.22);
}
.glass-card {
  background: linear-gradient(145deg, rgba(20, 31, 57, .8), rgba(10, 18, 36, .66));
  border: 1px solid rgba(111, 207, 255, .2);
  border-radius: 18px;
  padding: 20px;
  margin: 8px 0 18px;
  box-shadow: 0 14px 44px rgba(0,0,0,.24);
  backdrop-filter: blur(16px);
}
.eyebrow { color: #61dafb; font-size: .78rem; font-weight: 700; letter-spacing: .14em; }
.hero-title {
  font-size: clamp(2.1rem, 5vw, 4.2rem);
  line-height: 1.04;
  font-weight: 700;
  background: linear-gradient(90deg, #f5fbff, #61dafb 48%, #ad91ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 8px 0 12px;
}
.muted { color: #99a8bf; }
.badge {
  display: inline-block; padding: 5px 10px; margin: 2px 4px 2px 0;
  border-radius: 999px; background: rgba(97,218,251,.1);
  border: 1px solid rgba(97,218,251,.24); color: #9beaff; font-size: .78rem;
}
.score { color: #62e5b5; font-size: 1.8rem; font-weight: 700; }
.stButton > button, .stDownloadButton > button {
  border: 1px solid rgba(97,218,251,.4);
  border-radius: 10px;
  background: linear-gradient(90deg, #0a79b7, #6249c7);
  color: white; font-weight: 600;
}
</style>
"""
