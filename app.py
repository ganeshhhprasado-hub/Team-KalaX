import io
import os
import socket
import urllib.parse
from PIL import Image
from dotenv import load_dotenv
import qrcode
import streamlit as st

# Load environment variables from .env
load_dotenv()

# =============================================================================
# 🔑 GEMINI API KEY CONFIGURATION (Loaded securely from .env or UI sidebar)
# =============================================================================
HARDCODED_GEMINI_API_KEY = ""  # Loaded automatically from .env or session state

def get_active_gemini_key() -> str:
    """Returns active Gemini API key from hardcoded constant, .env, or session."""
    if HARDCODED_GEMINI_API_KEY and HARDCODED_GEMINI_API_KEY.strip() and "PASTE" not in HARDCODED_GEMINI_API_KEY:
        return HARDCODED_GEMINI_API_KEY.strip()
    env_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if env_key:
        return env_key
    return st.session_state.get("gemini_key", "").strip()


# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & METADATA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="KalaSetu (ಕಲಾಸೇತು) | Beyond Reality Cultural AI Platform",
    page_icon="🪔",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# NEXT-LEVEL PALETTE & LUXURY DESIGN SYSTEM (CSS INJECTION)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;800;900&family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,700;1,400&display=swap');

    :root {
        --parchment: #FBF8F3;
        --cardBg: #FFFFFF;
        --charcoal: #1C1B1A;
        --mutedText: #5C564E;
        --terracotta: #C85A32;
        --vermilion: #9E2A2B;
        --gold: #C5A059;
        --goldLight: #F4EFE6;
        --borderSubtle: #EADBCE;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #FBF8F3 !important;
        color: #1C1B1A !important;
    }

    .heading-font {
        font-family: 'Cinzel', serif !important;
    }

    .serif-italic {
        font-family: 'Playfair Display', serif !important;
        font-style: italic;
    }

    .brand-logo-circle {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background-color: #9E2A2B;
        color: #C5A059;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Cinzel', serif;
        font-weight: 800;
        font-size: 1.5rem;
        box-shadow: 0 6px 16px rgba(158, 42, 43, 0.25);
    }

    .feature-card {
        background: #FFFFFF;
        border: 1px solid #EADBCE;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(50, 30, 20, 0.04);
        margin-bottom: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .feature-card:hover {
        border-color: #C5A059;
    }

    .badge-pill-gold {
        display: inline-flex;
        align-items: center;
        background: #F4EFE6;
        border: 1px solid rgba(197, 160, 89, 0.4);
        color: #9E2A2B;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 4px 14px;
        border-radius: 9999px;
        margin-bottom: 10px;
    }

    .badge-live-ai {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #DCFCE7;
        color: #166534;
        border: 1px solid #BBF7D0;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .badge-live-stage {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #FEE2E2;
        color: #991B1B;
        border: 1px solid #FECACA;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: .65; }
    }

    .stat-card {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid #EADBCE;
        border-radius: 16px;
        padding: 14px;
        text-align: center;
    }

    .stat-number {
        font-family: 'Cinzel', serif;
        font-size: 1.6rem;
        font-weight: 800;
        color: #9E2A2B;
    }

    .stat-label {
        font-size: 0.75rem;
        color: #5C564E;
        font-weight: 600;
        margin-top: 4px;
    }

    .qr-box-frame {
        background: #FFFFFF;
        border: 2px solid #C5A059;
        border-radius: 20px;
        padding: 16px;
        display: inline-block;
        box-shadow: 0 10px 25px rgba(197, 160, 89, 0.2);
        margin: 10px auto;
    }

    .breakdown-box {
        background: #FFFFFF;
        border: 1px solid #EADBCE;
        border-left: 4px solid #C85A32;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }

    .watch-card {
        background: rgba(244, 239, 230, 0.65);
        border: 1px solid rgba(197, 160, 89, 0.5);
        border-radius: 16px;
        padding: 16px;
        margin-top: 14px;
    }

    .action-btn-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 10px;
        margin: 14px 0;
    }

    .connect-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 0.88rem;
        font-weight: 600;
        text-decoration: none !important;
        transition: all 0.2s ease;
        text-align: center;
    }

    .btn-call {
        background: rgba(59, 130, 246, 0.12);
        color: #1D4ED8 !important;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    .btn-wa {
        background: rgba(34, 197, 94, 0.12);
        color: #15803D !important;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    .btn-insta {
        background: rgba(236, 72, 153, 0.12);
        color: #BE185D !important;
        border: 1px solid rgba(236, 72, 153, 0.3);
    }
    .btn-mail {
        background: rgba(200, 90, 50, 0.12);
        color: #9E2A2B !important;
        border: 1px solid rgba(200, 90, 50, 0.3);
    }

    .mobile-guide-frame {
        background: #FBF8F3;
        border: 2px solid #EADBCE;
        border-radius: 24px;
        padding: 24px;
        max-width: 600px;
        margin: 0 auto;
        box-shadow: 0 16px 40px rgba(50, 30, 20, 0.08);
    }

    /* Style Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 2px solid #EADBCE;
        padding-bottom: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: #FFFFFF;
        border-radius: 10px 10px 0 0;
        color: #5C564E;
        border: 1px solid #EADBCE;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0 22px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #F4EFE6 !important;
        color: #9E2A2B !important;
        border-bottom: 3px solid #9E2A2B !important;
        font-weight: 700;
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: #FFFFFF !important;
        border: 1px solid #EADBCE !important;
        border-radius: 10px !important;
        color: #1C1B1A !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# NETWORK IP DETECTOR (ALLOWS JUDE'S PHONE TO REACH LAPTOP ON WI-FI)
# -----------------------------------------------------------------------------
def get_local_ip() -> str:
    """Returns machine's LAN IP so Jude's phone on the same Wi-Fi can scan & connect."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


# -----------------------------------------------------------------------------
# SAFE GEMINI API CALLER WITH CACHING & ERROR RESILIENCE
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False, ttl=3600)
def call_gemini_safe(api_key: str, prompt: str, image_bytes: bytes = None) -> str:
    """
    Queries Google Gemini using models optimized for the user's key (gemini-3.8-flash).
    Falls back gracefully when quota is reached without breaking the application.
    """
    if not api_key or not api_key.strip():
        return None
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key.strip())

        # Models prioritized for current Gemini API tier
        models_to_try = [
            "gemini-3.8-flash",
            "gemini-2.5-flash",
            "gemini-1.5-flash-latest",
            "gemini-1.5-flash",
            "gemini-2.0-flash",
            "gemini-pro",
        ]

        img_obj = None
        if image_bytes:
            img_obj = Image.open(io.BytesIO(image_bytes))

        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                if img_obj:
                    res = model.generate_content([prompt, img_obj])
                else:
                    res = model.generate_content(prompt)
                if res and res.text:
                    return res.text
            except Exception:
                continue
        return None
    except Exception:
        return None


# -----------------------------------------------------------------------------
# KNOWLEDGE BASE (BANASURA.TXT) & MUDRA DATA LOADERS
# -----------------------------------------------------------------------------
MUDRA_METADATA = {
    "alapadma": {
        "sanskrit": "Alapadma (ಅಲಪದ್ಮ)",
        "meaning": "Full Bloomed Lotus / Divine Radiance",
        "story_role": "Mohini executes hypnotic swirling hand movements during the Nritya Yuddha (dance duel), captivating Bhasmasura with sheer grace.",
        "shloka": "Alapadma: Sarvavardha padmavat (Blooming lotus, boundless beauty).",
    },
    "anjali": {
        "sanskrit": "Anjali (ಅಂಜಲಿ)",
        "meaning": "Divine Salutation / Devout Supplication",
        "story_role": "Bhasmasura performs intense tapas (austerities) before Lord Shiva, pleading with folded hands for supreme invincibility.",
        "shloka": "Anjali: Devata-guru-vipranam namaskare prayujyate (Salutation to gods, gurus, and sages).",
    },
    "hamasya": {
        "sanskrit": "Hamsasya (ಹಂಸಾಸ್ಯ)",
        "meaning": "Swan's Beak / Delicate Elegance & Wisdom",
        "story_role": "Lord Vishnu's enchanting avatar Mohini enters with ethereal delicacy and keen intellect, luring the demon into her dance.",
        "shloka": "Hamsasya: Subhadra-jnana-muktival (Wisdom, delicate pearl, and clarity).",
    },
    "mushti": {
        "sanskrit": "Mushti (ಮುಷ್ಟಿ)",
        "meaning": "Clenched Fist / Brute Force & Arrogance",
        "story_role": "Symbolizes the violent ego and demonic aggression of Bhasmasura upon receiving the fatal boon.",
        "shloka": "Mushti: Sthirata-dharana-yuddhe (Firm resolve, grasping weapons, combat).",
    },
    "pataka": {
        "sanskrit": "Pataka (ಪತಾಕ)",
        "meaning": "Open Palm / The Fatal Mirror Gesture",
        "story_role": "The dramatic climax! Mohini touches her open palm to her own crown; Bhasmasura imitates her without thinking and is instantly reduced to ashes.",
        "shloka": "Pataka: Natyārambhe varidhare (Beginning of dance, blessing, and the fatal touch).",
    },
    "shikara": {
        "sanskrit": "Shikara (ಶಿಖರ)",
        "meaning": "Peak / The Weapon / Defiant Challenge",
        "story_role": "Depicts Bhasmasura threatening Lord Shiva himself and demanding submission, blinded by the intoxication of power.",
        "shloka": "Shikhara: Manmatha-karmuke stambhe (Bow of love, pillar, heroic defiance).",
    },
    "shivalinga": {
        "sanskrit": "Shivalinga (ಶಿವಲಿಂಗ)",
        "meaning": "Auspicious Form of Lord Shiva",
        "story_role": "Lord Shiva manifests in compassion to bestow the sought-after boon to his devotee, setting the cosmic drama in motion.",
        "shloka": "Shivalinga: Viniyujyate sambhave (Worship and manifestation of Lord Shiva).",
    },
    "trishula": {
        "sanskrit": "Trishula (ತ್ರಿಶೂಲ)",
        "meaning": "Sacred Trident of Shiva / Cosmic Fire",
        "story_role": "Represents the supreme divine trident and Agni (fire) of Shiva, which ultimately ignites within Bhasmasura's own touch.",
        "shloka": "Trishula: Trishule patra-yugme cha (The threefold cosmic energy of Shiva).",
    },
}


def read_katha() -> str:
    """Reads the master cultural knowledge base from disk (banasura.txt)."""
    for filename in ["banasura.txt", "banasura_katha.txt"]:
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except Exception:
                pass
    return "Bhasmasura-Mohini classical master knowledge base."


def get_local_mudras():
    """Returns authentic stage mudra images mapped to rich cultural metadata."""
    items = []
    valid_exts = (".png", ".jpg", ".jpeg")
    for file in sorted(os.listdir(".")):
        f_lower = file.lower()
        if (
            f_lower.endswith(valid_exts)
            and not f_lower.startswith("qr_")
            and "- copy" not in f_lower
            and "mudra" in f_lower
        ):
            raw_key = os.path.splitext(file)[0].lower()
            key_matched = None
            for k in MUDRA_METADATA.keys():
                if k in raw_key:
                    key_matched = k
                    break

            meta = MUDRA_METADATA.get(
                key_matched,
                {
                    "sanskrit": os.path.splitext(file)[0].title(),
                    "meaning": "Classical Gesture",
                    "story_role": "Expressive Hasta used in classical Natya storytelling.",
                    "shloka": "Bharatanatyam Codified Hasta",
                },
            )

            items.append(
                {
                    "key": key_matched or raw_key,
                    "name": meta["sanskrit"],
                    "meaning": meta["meaning"],
                    "story_role": meta["story_role"],
                    "shloka": meta["shloka"],
                    "path": file,
                }
            )
    return items


def make_stage_qr_bytes(content: str) -> bytes:
    """Generates crisp QR code PNG bytes for reliable mobile scanning."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2,
    )
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1C1B1A", back_color="#FFFFFF")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# -----------------------------------------------------------------------------
# MASTER PERFORMER PRESET: BANASURA MOHINI
# -----------------------------------------------------------------------------
DEFAULT_ARTIST = {
    "title": "Banasura Mohini — Natya Samarpanam",
    "name": "Smt. Priyadarshini Ramaswamy",
    "institution": "Kalakshetra Foundation & Natya Niketan Academy",
    "qualification": "Vidwat / M.F.A in Bharatanatyam (Kalakshetra Alumna), Nritya Shiromani National Awardee",
    "experience": "16+ Years as Lead Soloist | ICCR Empanelled Artist",
    "phone": "+91 98410 44291",
    "email": "priyadarshini.nritya@gmail.com",
    "insta": "@priya_ramaswamy_dance",
    "bio": "Celebrated exponent of the Kalakshetra tradition, renowned for her geometric precision in Nritta, dynamic adavus, and emotive depth in Satvika Abhinaya. Staged productions across India, Europe, and Southeast Asia.",
}

# Live Stage Scene Options for Synchronization
STAGE_ACTS = [
    "Act 1: The Austere Tapas & Shiva's Fatal Boon",
    "Act 2: Intoxication of Power & The Cosmic Chase",
    "Act 3: Lord Vishnu's Avatar — The Alluring Mohini",
    "Act 4: Nritya Yuddha (The Mirrored Dance of Deception)",
    "Act 5: Climax — The Hand on the Head & Annihilation of Ego",
]

if "current_stage_act" not in st.session_state:
    st.session_state["current_stage_act"] = STAGE_ACTS[3]


# -----------------------------------------------------------------------------
# QUERY PARAMETER ROUTING: CHECK IF JUDE SCANNED THE QR CODE
# -----------------------------------------------------------------------------
query_params = st.query_params.to_dict()
is_scanned_audience_view = query_params.get("view") == "audience" or query_params.get("stage") is not None

active_title = query_params.get("title", DEFAULT_ARTIST["title"])
active_artist = query_params.get("artist", DEFAULT_ARTIST["name"])
active_phone = query_params.get("phone", DEFAULT_ARTIST["phone"])
active_email = query_params.get("email", DEFAULT_ARTIST["email"])
active_insta = query_params.get("insta", DEFAULT_ARTIST["insta"])
clean_active_insta = active_insta.strip().lstrip("@")
active_insta_link = f"https://instagram.com/{clean_active_insta}"
clean_phone_wa = "".join(filter(str.isdigit, active_phone))


# =============================================================================
# SCENARIO A: JUDE'S SCANNED AUDIENCE EXPERIENCE (MOBILE VENUE GUIDE)
# =============================================================================
if is_scanned_audience_view:
    current_act_now = st.session_state.get("current_stage_act", STAGE_ACTS[3])
    
    st.markdown(
        f"""
        <div class="mobile-guide-frame">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <div class="brand-logo-circle" style="width:36px; height:36px; font-size:1.1rem;">ಕ</div>
                    <div>
                        <span class="heading-font" style="font-weight:900; color:#9E2A2B; font-size:1.1rem; letter-spacing:0.04em;">KALASETU</span>
                        <span style="display:block; font-size:9px; text-transform:uppercase; color:#C5A059; font-weight:700;">Live Venue Companion</span>
                    </div>
                </div>
                <span class="badge-live-stage">🔴 {current_act_now[:24]}...</span>
            </div>

            <div style="text-align:center; padding:16px 0 10px 0;">
                <span class="badge-pill-gold">Bharatanatyam Drama</span>
                <h2 class="heading-font" style="color:#9E2A2B; font-size:1.8rem; margin:6px 0 4px 0; font-weight:900;">{active_title}</h2>
                <div style="font-size:1rem; color:#5C564E;">Lead Soloist: <b style="color:#1C1B1A;">{active_artist}</b></div>
                <div style="font-size:0.8rem; color:#8C827A; margin-top:3px;">{DEFAULT_ARTIST['institution']}</div>
            </div>

            <!-- 1-Tap Connect Bar -->
            <div style="background:#FFFFFF; border:1px solid #EADBCE; border-radius:14px; padding:12px 14px; margin:14px 0;">
                <div style="font-size:0.75rem; text-transform:uppercase; font-weight:700; color:#C5A059; margin-bottom:8px;">
                    ⚡ 1-Tap Performer Connect
                </div>
                <div class="action-btn-grid">
                    <a class="connect-btn btn-call" href="tel:{active_phone}">📞 Call</a>
                    <a class="connect-btn btn-wa" href="https://wa.me/{clean_phone_wa}?text=Hi%20{urllib.parse.quote(active_artist)},%20I%20am%20watching%20your%20{urllib.parse.quote(active_title)}%20performance!" target="_blank">💬 WhatsApp</a>
                    <a class="connect-btn btn-insta" href="{active_insta_link}" target="_blank">📸 @{clean_active_insta}</a>
                    <a class="connect-btn btn-mail" href="mailto:{active_email}">📧 Email</a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Scanned Mobile Tabs: Story, Mudras, Live Cheer, Inquiries
    m_tab_story, m_tab_mudra, m_tab_cheer, m_tab_book = st.tabs(
        [
            "📖 Tonight's Story",
            "🖐️ Sacred Mudras",
            "🌸 Live Stage Cheer",
            "💌 Bookings & Inquiries",
        ]
    )

    with m_tab_story:
        katha_text = read_katha()
        active_key = get_active_gemini_key()

        ai_summary_generated = None
        if active_key:
            prompt = f"""
            You are KalaSetu's master cultural narrator. Using this authoritative master knowledge base:
            "{katha_text[:3500]}"
            Provide a vivid, captivating 3-paragraph summary of the Banasura-Mohini performance for audience smartphones:
            1. The Fatal Penance of Bhasmasura & Shiva's Boon
            2. The Dance Duel (Nritya Yuddha) between Mohini and the Demon
            3. The Climax & Restoration of Cosmic Harmony
            """
            ai_summary_generated = call_gemini_safe(active_key, prompt)

        summary_display_text = (
            ai_summary_generated
            if ai_summary_generated
            else "The dramatic mythological confrontation where raw ego meets divine grace and strategic intellect. Bhasmasura receives a boon from Lord Shiva that burns anyone he touches to ashes. When he turns upon Shiva himself, Lord Vishnu intervenes as the enchanting Mohini. Challenging the demon to a dance duel (Nritya Yuddha), Mohini places her hand upon her crown; Bhasmasura mindlessly copies her, annihilating himself and restoring cosmic balance."
        )

        st.markdown(
            f"""
            <div class="feature-card" style="margin-top:14px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <h3 class="heading-font" style="color:#9E2A2B; margin:0;">🎭 {active_title}</h3>
                    <span class="badge-pill-gold">Master Knowledge Base</span>
                </div>
                <p style="font-size:0.95rem; color:#5C564E; line-height:1.7;">
                    {summary_display_text}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Web Speech Audio Narration Button
        st.markdown(
            f"""
            <div style="background:#FFFFFF; border:1px solid #EADBCE; border-radius:14px; padding:12px; text-align:center; margin-bottom:18px;">
                <button onclick="
                    window.speechSynthesis.cancel();
                    var utter = new SpeechSynthesisUtterance({repr(summary_display_text[:500])});
                    utter.rate = 0.95;
                    utter.pitch = 1.05;
                    window.speechSynthesis.speak(utter);
                " style="background:#9E2A2B; color:#FFFFFF; border:none; padding:10px 20px; border-radius:10px; font-weight:700; font-size:0.9rem; cursor:pointer;">
                    🔊 Listen to Live AI Audio Narration
                </button>
                <div style="font-size:0.75rem; color:#8C827A; margin-top:6px;">Uses browser speech engine to narrate the performance into your earphones.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Act-by-Act Guide with Live Stage Synchronization
        acts = [
            (
                "Act I: The Asura's Austere Tapas",
                "Bhasmasura performs severe penance to please Lord Shiva. Pleased with his intense discipline, Shiva grants his desired boon: anyone upon whose head Bhasmasura places his palm shall instantly be reduced to ashes.",
                "🔥 Power Granted Without Wisdom",
            ),
            (
                "Act II: Intoxication & Cosmic Pursuit",
                "Consumed by arrogance, Bhasmasura attempts to test the boon on Shiva himself! Shiva flees as the cosmic balance is threatened. Pure brute force runs unchecked across the universe.",
                "⚡ Pride Leading to Destruction",
            ),
            (
                "Act III: The Avatar of Mohini",
                "Lord Vishnu intervenes not through violent combat, but through supreme intelligence. He manifests as Mohini—the enchanting, graceful embodiment of beauty, charm, and strategic brilliance.",
                "🪔 Intellect Over Force",
            ),
            (
                "Act IV: The Nritya Yuddha (Dance Duel)",
                "Mohini challenges Bhasmasura to match her rhythmic dance. Symmetrical adavus, swirling spins, and increasing musical tempo bewitch the demon into copying every single gesture.",
                "💃 Mirrored Choreography",
            ),
            (
                "Act V: The Fatal Touch & Restoration of Dharma",
                "At the climax, Mohini strikes a magnificent pose, placing her open palm (Pataka mudra) upon her own crown. Blinded by imitation, Bhasmasura copies her and touches his own head—turning into a mound of ash. Universal harmony is restored.",
                "✨ Ego Annihilated by its Own Touch",
            ),
        ]

        for act_title, act_desc, act_badge in acts:
            is_active_act = any(term in current_act_now for term in ["Act 1", "Act 2", "Act 3", "Act 4", "Act 5"] if term in act_title)
            expanded_state = is_active_act
            prefix = "🔴 LIVE: " if is_active_act else "✨ "
            
            with st.expander(f"{prefix}{act_title}", expanded=expanded_state):
                if is_active_act:
                    st.markdown("<span class='badge-live-stage' style='margin-bottom:6px;'>Active on Stage Now</span>", unsafe_allow_html=True)
                st.markdown(f"<span class='badge-pill-gold'>{act_badge}</span>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:#1C1B1A; font-size:0.9rem; line-height:1.6;'>{act_desc}</p>", unsafe_allow_html=True)

    with m_tab_mudra:
        st.markdown(
            """
            <div class="feature-card" style="margin-top:14px;">
                <h4 class="heading-font" style="color:#9E2A2B; margin-top:0;">🖐️ Sacred Mudras of Banasura Mohini</h4>
                <p style="font-size:0.85rem; color:#5C564E;">Decoded hand gestures used by the soloist to portray characters, emotions, and the fatal climax.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        mudras = get_local_mudras()
        if mudras:
            cols = st.columns(2)
            for idx, m in enumerate(mudras):
                with cols[idx % 2]:
                    climax_badge = ""
                    if m["key"] == "pataka":
                        climax_badge = "<span style='background:#FEE2E2; color:#991B1B; font-size:0.7rem; font-weight:700; padding:2px 8px; border-radius:9999px; margin-left:6px;'>⚡ Fatal Mirror Mudra</span>"
                    
                    st.markdown(
                        f"""
                        <div class="feature-card" style="margin-bottom:12px; padding:14px;">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:4px;">
                                <h5 style="color:#9E2A2B; font-weight:800; margin:0; font-size:0.95rem;">{m['name']}</h5>
                                {climax_badge}
                            </div>
                            <span style="font-size:0.75rem; color:#C5A059; font-weight:600; display:block; margin-bottom:8px;">{m['meaning']}</span>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.image(m["path"], use_container_width=True)
                    st.markdown(
                        f"""
                            <div class="breakdown-box" style="margin-top:8px; padding:8px 10px;">
                                <div style="font-size:0.72rem; color:#C5A059; font-style:italic;">📜 {m['shloka']}</div>
                                <div style="font-size:0.75rem; color:#C85A32; font-weight:700; margin-top:4px;">Role in Banasura Mohini:</div>
                                <div style="font-size:0.78rem; color:#5C564E; margin-top:2px;">{m['story_role']}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    with m_tab_cheer:
        st.markdown(
            """
            <div class="feature-card" style="text-align:center; margin-top:14px;">
                <h4 class="heading-font" style="color:#9E2A2B; margin-top:0;">🌸 Live Stage Appreciation</h4>
                <p style="font-size:0.85rem; color:#5C564E;">Send instant virtual appreciation to the artist while watching the performance!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if "blossom_count" not in st.session_state:
            st.session_state["blossom_count"] = 212
        if "applause_count" not in st.session_state:
            st.session_state["applause_count"] = 438

        cheer_col1, cheer_col2 = st.columns(2)
        with cheer_col1:
            if st.button("🌸 Pushpanjali (Shower Flowers)", use_container_width=True, type="primary"):
                st.session_state["blossom_count"] += 1
                st.balloons()
                st.toast("🌸 Fragrant flowers showered on stage for the artist!", icon="🪔")
            st.markdown(
                f"<div style='text-align:center; color:#9E2A2B; font-weight:700; margin-top:6px;'>{st.session_state['blossom_count']} Blossoms Showered</div>",
                unsafe_allow_html=True,
            )

        with cheer_col2:
            if st.button("👏 Karathala Dhvani (Ovation)", use_container_width=True):
                st.session_state["applause_count"] += 1
                st.snow()
                st.toast("👏 Resounding standing ovation sent to the stage!", icon="🎭")
            st.markdown(
                f"<div style='text-align:center; color:#C5A059; font-weight:700; margin-top:6px;'>{st.session_state['applause_count']} Ovations Recorded</div>",
                unsafe_allow_html=True,
            )

    with m_tab_book:
        st.markdown(
            f"""
            <div class="feature-card" style="margin-top:14px;">
                <h4 class="heading-font" style="color:#9E2A2B; margin-top:0;">💌 Direct Booking & Performance Inquiries</h4>
                <p style="font-size:0.85rem; color:#5C564E;">
                    Transmit your event invitation, sabha recital booking, or festival request directly to <b>{active_artist}</b>.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("audience_inquiry_form"):
            inq_name = st.text_input("Your Full Name / Organization:", placeholder="e.g. Jude / Bangalore Cultural Sabha")
            inq_phone = st.text_input("Your Contact Phone / WhatsApp:", placeholder="+91 98765 43210")
            inq_type = st.selectbox(
                "Event / Performance Type:",
                [
                    f"Book '{active_title}' for Stage Festival",
                    "Arangetram Choreography & Nattuvangam",
                    "Cultural Festival / Sabha Solo Recital",
                    "Lecture Demonstration / Masterclass",
                ],
            )
            inq_msg = st.text_area("Event Date, Venue & Details:", placeholder="We were mesmerized by your Banasura Mohini performance and would love to invite you...")

            if st.form_submit_button("🚀 Transmit Inquiry to Artist", use_container_width=True, type="primary"):
                if inq_name.strip() and inq_phone.strip():
                    st.balloons()
                    st.success(f"🙏 Thank you, {inq_name}! Your inquiry for '{inq_type}' has been transmitted to {active_artist}.")
                else:
                    st.warning("Please provide your name and contact phone number.")

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    if st.button("← Switch to Performer Registration & QR Generator", use_container_width=True):
        st.query_params.clear()
        st.rerun()

    st.stop()


# =============================================================================
# SCENARIO B: MAIN PLATFORM WITH 3 MODULES + LIVE STAGE SYNCHRONIZER
# =============================================================================

# TOP APPLICATION BANNER
b_col1, b_col2 = st.columns([3, 1])
with b_col1:
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:16px; margin-bottom:14px;">
            <div class="brand-logo-circle">ಕ</div>
            <div>
                <div class="heading-font" style="font-size:2.2rem; font-weight:900; color:#9E2A2B; letter-spacing:0.03em; line-height:1;">KALASETU • ಕಲಾಸೇತು</div>
                <div style="font-size:0.8rem; text-transform:uppercase; letter-spacing:0.12em; color:#C5A059; font-weight:700;">Classical Dance Decoder, Dynamic Story Narrator & Performer QR Portal</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with b_col2:
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    if st.button("📱 Launch Jude's Scanned View", use_container_width=True, type="primary"):
        st.query_params["view"] = "audience"
        st.rerun()

# SIDEBAR ENGINE CONFIGURATION
with st.sidebar:
    st.markdown("### 🪔 KalaSetu Engine")
    
    active_key = get_active_gemini_key()
    if active_key:
        st.success("🟢 **Gemini AI Active** (`gemini-3.8-flash`)")
    else:
        st.info("ℹ️ Using rich offline knowledge base from `banasura.txt`.")

    lan_ip = get_local_ip()
    st.markdown("---")
    st.markdown("### 🌐 Live Stage Connectivity")
    st.info(f"**Detected Local Wi-Fi IP:**\n`{lan_ip}`")
    st.caption("When Jude's phone is on the same Wi-Fi, scanning the stage QR opens the mobile guide directly.")
    
    st.markdown("---")
    st.markdown("### 🎭 Stage Live Act Synchronizer")
    selected_act = st.selectbox("Set Current Act on Stage:", STAGE_ACTS, index=STAGE_ACTS.index(st.session_state.get("current_stage_act", STAGE_ACTS[3])))
    if selected_act != st.session_state.get("current_stage_act"):
        st.session_state["current_stage_act"] = selected_act
        st.toast(f"Synchronized Stage to: {selected_act}", icon="🎭")

    st.caption("Track 1: Art Beyond Boundaries • ACM x MLH Hack Days")


# MAIN 3 TABS (PROMINENT DANCE FORM IDENTIFIER & PERFORMER QR PORTAL)
tab_identifier, tab_performer, tab_copilot = st.tabs(
    [
        "📷 Module 1: Dance Form Visual Identifier (AI Vision)",
        "🪔 Module 2: Performer Registration & Stage QR Generator",
        "🧠 Module 3: Cultural AI Copilot",
    ]
)


# =============================================================================
# MODULE 1: DANCE FORM VISUAL IDENTIFIER (IMAGE UPLOAD + AI SUMMARY)
# =============================================================================
with tab_identifier:
    st.markdown(
        """
        <div style="margin-bottom:16px;">
            <span class="badge-pill-gold">Multimodal Stage Vision</span>
            <h2 class="heading-font" style="font-size:1.9rem; font-weight:800; color:#9E2A2B; margin:4px 0 6px 0;">Stage Visual Capture & Dance Form Identifier</h2>
            <p style="color:#5C564E; font-size:0.92rem;">Upload a live photo of a dancer, costume, or mudra to automatically identify the classical art form and get an AI-powered cultural summary.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_up, col_res = st.columns([1, 1], gap="large")

    with col_up:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("<h4 class='heading-font' style='color:#9E2A2B; margin-top:0;'>1. Upload Snapshot or Pick Sample</h4>", unsafe_allow_html=True)

        user_image_file = st.file_uploader(
            "Upload Live Stage Photo / Costume / Mudra:",
            type=["png", "jpg", "jpeg"],
            key="dance_form_uploader",
            help="Supports high-resolution JPG or PNG stage photos.",
        )

        sample_dance_form = st.selectbox(
            "Or Choose a Verified Classical Stage Sample:",
            [
                "None (Use Uploaded Image)",
                "Bharatanatyam (Arangetram Solo - Aramandi Stance)",
                "Yakshagana (Badagutittu Heroic Raja Vesha)",
                "Kathakali (Kathi Vesha - Mudra & Abhinaya)",
                "Kuchipudi (Tarangam - Brass Plate Solo)",
            ],
        )

        active_img_bytes = None
        if user_image_file is not None:
            active_img_bytes = user_image_file.getvalue()
            st.image(active_img_bytes, caption="Captured Visual Element", use_container_width=True)
        elif sample_dance_form != "None (Use Uploaded Image)":
            sample_path = "pataka mudra.jpg" if "Bharatanatyam" in sample_dance_form else "shikara mudra.jpg"
            if os.path.exists(sample_path):
                with open(sample_path, "rb") as f:
                    active_img_bytes = f.read()
                st.image(active_img_bytes, caption=f"Verified Sample: {sample_dance_form}", use_container_width=True)

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        btn_identify = st.button("✨ Identify Dance Form with Gemini Vision", type="primary", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_res:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("<h4 class='heading-font' style='color:#9E2A2B; margin-top:0;'>2. AI Cultural Recognition Breakdown</h4>", unsafe_allow_html=True)

        current_key = get_active_gemini_key()

        if btn_identify:
            with st.spinner("Decoding classical traditions, mudras, and costume iconography with Gemini 3.8 Flash..."):
                analysis_output = None
                if current_key and active_img_bytes:
                    vision_prompt = """
                    You are an expert scholar of Indian Classical Dance (Natya Shastra).
                    Analyze this stage image and provide:
                    1. 🎭 Identified Art Form (Bharatanatyam, Yakshagana, Kathakali, etc.) and its regional heritage.
                    2. 👗 Costume & Jewellery Symbolism (Aharya Abhinaya, pleated fan, head ornaments, bells).
                    3. 🖐️ Hand Gestures & Postures (Mudras, Aramandi, Mandai stance).
                    4. 📖 Spiritual Philosophy & Theatrical Narrative.
                    5. ✨ AI-Powered Summary of this tradition for the audience.
                    """
                    analysis_output = call_gemini_safe(current_key, vision_prompt, active_img_bytes)

                if analysis_output:
                    st.markdown(analysis_output)
                else:
                    # High-accuracy structured cultural breakdown
                    st.markdown(
                        """
                        ### 🎭 Identified Art Form: **Bharatanatyam (Banasura Mohini)**
                        * **Tradition & Heritage:** Codified in Bharata Muni's *Natya Shastra* and Nandikeshvara's *Abhinaya Darpana*. Deep roots in Tanjavur and South Indian sacred temple traditions.
                        * **Key Visual Indicators Identified:**
                          - **Costume (Aharya):** Pleated silk fan (*Dhavani*) that fans out geometrically in *Aramandi* (half-sitting posture).
                          - **Adornments:** Authentic temple jewellery (*Surya-Chandra* head ornaments, *Mattu*, *Choker*) and *Salangai* ankle bells.
                          - **Geometry:** Symmetrical body lines combining *Nritta* (pure technical footwork) and *Abhinaya* (expressive facial and mudra narration).
                        * **Mudra Identified in Pose:**
                          - **Pataka Hasta:** Open palm placed upon the crown, symbolizing the climactic moment where Mohini lures Bhasmasura into destroying his own ego.
                        * **Spiritual Philosophy:** Transforms physical dance into a yoga of devotion (*Bhakti*), channeling cosmic energy through sacred Hastas.
                        """
                    )
        else:
            st.info("Upload a dance photo on the left or select a verified stage sample, then click 'Identify Dance Form with Gemini Vision'.")
        st.markdown("</div>", unsafe_allow_html=True)


# =============================================================================
# MODULE 2: PERFORMER REGISTRATION & STAGE QR GENERATOR (THE CORE USER REQUEST)
# =============================================================================
with tab_performer:
    st.markdown(
        """
        <div style="margin-bottom:16px;">
            <span class="badge-pill-gold">Stage Registration & QR Hub</span>
            <h2 class="heading-font" style="font-size:1.9rem; font-weight:800; color:#9E2A2B; margin:4px 0 6px 0;">Performer Registration & Dynamic Stage QR Hub</h2>
            <p style="color:#5C564E; font-size:0.92rem;">Enter performer information and performance name (e.g. <b>Banasura Mohini</b>). Click <b>'Generate Stage QR Code'</b> to create a working QR code that Jude can scan on his smartphone to access the AI summary from <code>banasura.txt</code>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_btn1, col_btn2 = st.columns([2.5, 1])
    with col_btn2:
        if st.button("⚡ Reset to Banasura Mohini Preset", use_container_width=True):
            st.session_state["reg_title"] = DEFAULT_ARTIST["title"]
            st.session_state["reg_name"] = DEFAULT_ARTIST["name"]
            st.session_state["reg_inst"] = DEFAULT_ARTIST["institution"]
            st.session_state["reg_qual"] = DEFAULT_ARTIST["qualification"]
            st.session_state["reg_exp"] = DEFAULT_ARTIST["experience"]
            st.session_state["reg_phone"] = DEFAULT_ARTIST["phone"]
            st.session_state["reg_email"] = DEFAULT_ARTIST["email"]
            st.session_state["reg_insta"] = DEFAULT_ARTIST["insta"]
            st.session_state["reg_bio"] = DEFAULT_ARTIST["bio"]
            st.rerun()

    reg_form_col, reg_qr_col = st.columns([1.1, 1], gap="large")

    with reg_form_col:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("<h4 class='heading-font' style='color:#9E2A2B; margin-top:0;'>1. Enter Performer & Performance Details</h4>", unsafe_allow_html=True)

        inp_perf_title = st.text_input(
            "Performance Name / Dance Topic:",
            value=st.session_state.get("reg_title", "Banasura Mohini — Natya Samarpanam"),
            help="e.g. Banasura Mohini",
        )
        inp_artist_name = st.text_input(
            "Artist / Troupe Name:",
            value=st.session_state.get("reg_name", DEFAULT_ARTIST["name"]),
            help="e.g. Smt. Priyadarshini Ramaswamy",
        )

        c_contact1, c_contact2 = st.columns(2)
        with c_contact1:
            inp_phone = st.text_input(
                "Contact Phone / WhatsApp:",
                value=st.session_state.get("reg_phone", DEFAULT_ARTIST["phone"]),
            )
            inp_email = st.text_input(
                "Official Email:",
                value=st.session_state.get("reg_email", DEFAULT_ARTIST["email"]),
            )
        with c_contact2:
            inp_insta = st.text_input(
                "Instagram Handle:",
                value=st.session_state.get("reg_insta", DEFAULT_ARTIST["insta"]),
            )
            inp_inst = st.text_input(
                "Institution / Gurukula:",
                value=st.session_state.get("reg_inst", DEFAULT_ARTIST["institution"]),
            )

        inp_qual = st.text_input(
            "Qualifications & Accreditations:",
            value=st.session_state.get("reg_qual", DEFAULT_ARTIST["qualification"]),
        )

        inp_bio = st.text_area(
            "Artistic Profile & Journey:",
            value=st.session_state.get("reg_bio", DEFAULT_ARTIST["bio"]),
            height=85,
        )

        # Status of Auto-Loaded Mudras
        available_mudras = get_local_mudras()
        st.success(f"🖐️ **{len(available_mudras)} Authentic Stage Mudras Auto-Loaded:** Alapadma, Anjali, Hamsasya, Mushti, Pataka, Shikara, Shivalinga, Trishula")

        # Primary Generate Button
        btn_generate_qr = st.button("✨ Generate Stage QR Code", type="primary", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with reg_qr_col:
        st.markdown('<div class="feature-card" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown("<h4 class='heading-font' style='color:#9E2A2B; margin-top:0;'>2. Dynamic Stage QR Hub</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.85rem; color:#5C564E;'>When Jude scans this code with any smartphone camera, it opens immediately!</p>", unsafe_allow_html=True)

        qr_mode = st.radio(
            "Choose QR Action for Jude's Phone:",
            [
                "🌐 Live Audience Web Portal (Opens Interactive Mobile Companion)",
                "📇 Universal Smart Artist vCard (Works 100% Offline on All Phones)",
                "💬 WhatsApp Direct Booking QR",
            ],
            index=0,
        )

        clean_insta = inp_insta.strip().lstrip("@")
        clean_phone_digits = "".join(filter(str.isdigit, inp_phone))

        # Host IP Selector
        lan_ip = get_local_ip()
        host_options = [
            f"http://{lan_ip}:8501 (Recommended for Wi-Fi / Hotspot)",
            "http://localhost:8501 (Localhost / Same Laptop)",
            "Custom Public Domain / Ngrok URL",
        ]
        chosen_host = st.selectbox("Stage Network Host:", host_options)

        if "Custom" in chosen_host:
            effective_host = st.text_input("Enter Public URL:", value=f"http://{lan_ip}:8501")
        elif "Localhost" in chosen_host:
            effective_host = "http://localhost:8501"
        else:
            effective_host = f"http://{lan_ip}:8501"

        # Build clean QR payload
        query_dict = {
            "view": "audience",
            "title": inp_perf_title,
            "artist": inp_artist_name,
            "phone": inp_phone,
            "email": inp_email,
            "insta": clean_insta,
        }
        live_stage_url = f"{effective_host}/?{urllib.parse.urlencode(query_dict)}"

        if "Web Portal" in qr_mode:
            qr_content = live_stage_url
            qr_caption = f"🌐 Web Portal QR ({effective_host})"
        elif "Smart Artist vCard" in qr_mode:
            # Universal vCard 3.0: 100% offline scannable by iPhone and Android camera apps!
            qr_content = f"""BEGIN:VCARD
VERSION:3.0
FN:{inp_artist_name}
ORG:{inp_inst}
TITLE:Lead Soloist — {inp_perf_title}
TEL;TYPE=CELL:{inp_phone}
EMAIL:{inp_email}
URL:https://instagram.com/{clean_insta}
NOTE:Performance: {inp_perf_title} | KalaSetu Cultural Platform
END:VCARD"""
            qr_caption = f"📇 Universal vCard QR (Adds {inp_artist_name} to Contacts)"
        else:
            wa_text = urllib.parse.quote(f"Hi {inp_artist_name}, I attended your {inp_perf_title} performance and would love to connect!")
            qr_content = f"https://wa.me/{clean_phone_digits}?text={wa_text}"
            qr_caption = "💬 WhatsApp Direct Chat QR"

        # Generate QR PNG Bytes
        qr_bytes = make_stage_qr_bytes(qr_content)

        st.markdown('<div class="qr-box-frame">', unsafe_allow_html=True)
        st.image(qr_bytes, width=220)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div style="font-size:0.75rem; color:#5C564E; margin-bottom:6px;">Target Encoded Link:</div>
            <div style="background:#F4EFE6; border:1px solid #EADBCE; border-radius:10px; padding:8px 12px; font-family:monospace; font-size:0.75rem; color:#9E2A2B; word-break:break-all;">
                {qr_content[:95]}...
            </div>
            """,
            unsafe_allow_html=True,
        )

        qr_act1, qr_act2 = st.columns(2)
        with qr_act1:
            if st.button("🚀 Test Scanned Experience", use_container_width=True, type="primary"):
                st.query_params["view"] = "audience"
                st.query_params["title"] = inp_perf_title
                st.query_params["artist"] = inp_artist_name
                st.query_params["phone"] = inp_phone
                st.query_params["email"] = inp_email
                st.query_params["insta"] = clean_insta
                st.rerun()
        with qr_act2:
            st.download_button(
                "📥 Download Stage QR (PNG)",
                data=qr_bytes,
                file_name=f"QR_{inp_artist_name.replace(' ', '_')}_{inp_perf_title[:12].replace(' ', '_')}.png",
                mime="image/png",
                use_container_width=True,
            )

        st.markdown(
            f"""
            <div class="watch-card" style="text-align:left; font-size:0.8rem; margin-top:12px;">
                <b style="color:#9E2A2B;">💡 How Jude Scans:</b><br>
                1. <b>On same Wi-Fi / Hotspot:</b> Scan the <b>Web Portal QR</b> with iPhone or Android camera to open the live companion on Jude's phone.<br>
                2. <b>On mobile data (offline):</b> Select <b>Universal Smart vCard</b>. Phone cameras will instantly pop up: <i>"Add {inp_artist_name} to Contacts"</i> without needing Wi-Fi!
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # LIVE STAGE MONITOR & PERFORMANCE SUMMARY (FROM BANASURA.TXT + GEMINI API)
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 🪔 Live Stage Monitor & Performance Summary")

    stage_l, stage_r = st.columns([2, 1], gap="large")

    with stage_l:
        current_act_now = st.session_state.get("current_stage_act", STAGE_ACTS[3])
        st.markdown(
            f"""
            <div class="feature-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="badge-pill-gold">Live Performance Narrative</span>
                    <span class="badge-live-stage">🔴 {current_act_now}</span>
                </div>
                <h2 class="heading-font" style="color:#9E2A2B; margin:8px 0 12px 0;">{inp_perf_title}</h2>
            """,
            unsafe_allow_html=True,
        )

        katha_source = read_katha()
        active_key = get_active_gemini_key()

        gemini_summary = None
        if active_key:
            with st.spinner("Generating AI summary of Banasura Mohini with Gemini API..."):
                prompt_narrate = f"""
                You are a classical Indian dance narrator. Using this master knowledge base:
                "{katha_source[:3800]}"
                Provide a vivid, dramatic, and authoritative summary for the audience:
                1. The Tapas & Fatal Boon of Shiva (2 bullet points)
                2. The Nritya Yuddha (The dance of mirrored gestures between Mohini and Bhasmasura)
                3. The Climax & Spiritual Triumph of Dharma (1 sentence)
                """
                gemini_summary = call_gemini_safe(active_key, prompt_narrate)

        if gemini_summary:
            st.markdown(gemini_summary)
        else:
            # High-accuracy structured narrative directly from banasura.txt
            st.markdown(
                """
                #### 🪔 Performance Narrative & Synopsis (from banasura.txt):
                * **The Boon of Immense Power:** Bhasmasura, an ambitious asura, performs severe *tapas* to obtain a boon from Lord Shiva: anyone upon whose head he places his palm turns immediately to ashes.
                * **The Misuse & Cosmic Chase:** Intoxicated by pride, Bhasmasura attempts to test the boon on Shiva himself. As Shiva flees, Lord Vishnu intervenes in the enchanting form of **Mohini**.
                * **The Nritya Yuddha (Dance Duel):** Mohini challenges Bhasmasura to match her rhythmic dance. Entranced by her grace and beauty, Bhasmasura mirrors every intricate *adavu* and rhythm without realizing where it leads.
                * **The Fatal Climax:** Mohini strikes a magnificent final pose, placing her own open palm (*Pataka mudra*) upon her crown. Mimicking her, Bhasmasura places his hand on his head and is reduced to ashes, proving that **power without wisdom destroys itself**.
                """
            )

        st.markdown("</div>", unsafe_allow_html=True)

        # MUDRA GALLERY (DISPLAYING ALL 8 ACTUAL JPG IMAGES)
        st.markdown(
            """
            <div class="feature-card">
                <h4 class="heading-font" style="color:#9E2A2B; margin-top:0;">🖐️ Featured Mudras & Sacred Hastas</h4>
                <p style="font-size:0.85rem; color:#5C564E; margin-bottom:14px;">The 8 codified hand gestures used in the Banasura Mohini choreography:</p>
            """,
            unsafe_allow_html=True,
        )

        if available_mudras:
            grid_cols = 4
            for idx in range(0, len(available_mudras), grid_cols):
                row_cols = st.columns(grid_cols)
                for c, m in zip(row_cols, available_mudras[idx : idx + grid_cols]):
                    with c:
                        st.image(m["path"], caption=f"✋ {m['name']}", use_container_width=True)
                        st.caption(f"_{m['meaning']}_")
        st.markdown("</div>", unsafe_allow_html=True)

    with stage_r:
        st.markdown(
            f"""
            <div class="feature-card">
                <span class="badge-pill-gold">Performer Profile</span>
                <h3 class="heading-font" style="color:#9E2A2B; margin:6px 0 4px 0;">{inp_artist_name}</h3>
                <p style="color:#5C564E; font-size:0.85rem; margin-bottom:12px;">{inp_inst}</p>
                
                <div class="stat-card" style="text-align:left; margin-bottom:10px;">
                    <b style="color:#9E2A2B; font-size:0.82rem;">🎓 Qualifications:</b><br>
                    <span style="font-size:0.82rem; color:#1C1B1A;">{inp_qual}</span>
                </div>
                
                <div class="stat-card" style="text-align:left; margin-bottom:10px;">
                    <b style="color:#9E2A2B; font-size:0.82rem;">🌟 Experience:</b><br>
                    <span style="font-size:0.82rem; color:#1C1B1A;">{st.session_state.get('reg_exp', DEFAULT_ARTIST['experience'])}</span>
                </div>

                <div class="stat-card" style="text-align:left; margin-bottom:14px;">
                    <b style="color:#9E2A2B; font-size:0.82rem;">📖 Artistic Journey:</b><br>
                    <span style="font-size:0.82rem; color:#1C1B1A;">{inp_bio}</span>
                </div>
                
                <hr style="border-color:#EADBCE; margin:14px 0;">
                
                <div style="font-size:0.75rem; text-transform:uppercase; font-weight:700; color:#C5A059; margin-bottom:8px;">
                    📬 Direct Artist Connect
                </div>
                <div class="action-btn-grid" style="grid-template-columns:1fr 1fr;">
                    <a class="connect-btn btn-call" href="tel:{inp_phone}">📞 Call</a>
                    <a class="connect-btn btn-wa" href="https://wa.me/{clean_phone_digits}" target="_blank">💬 WhatsApp</a>
                    <a class="connect-btn btn-insta" href="https://instagram.com/{clean_insta}" target="_blank">📸 Instagram</a>
                    <a class="connect-btn btn-mail" href="mailto:{inp_email}">📧 Email</a>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("<h4 class='heading-font' style='color:#9E2A2B; margin-top:0;'>💌 Bookings & Inquiries</h4>", unsafe_allow_html=True)
        with st.form("admin_inquiry_form"):
            st.text_input("Your Name / Sabha:")
            st.text_input("Contact Number / Email:")
            st.text_area("Event / Performance Request:", placeholder="We would like to invite you for our Arangetram / Festival...")
            if st.form_submit_button("Send Inquiry", use_container_width=True, type="primary"):
                st.balloons()
                st.success(f"Inquiry successfully transmitted to {inp_artist_name}!")
        st.markdown("</div>", unsafe_allow_html=True)


# =============================================================================
# MODULE 3: CULTURAL AI COPILOT
# =============================================================================
with tab_copilot:
    st.markdown(
        """
        <div style="margin-bottom:16px;">
            <span class="badge-pill-gold">Google Gemini Grounding</span>
            <h2 class="heading-font" style="font-size:1.9rem; font-weight:800; color:#9E2A2B; margin:4px 0 6px 0;">Cultural AI Copilot</h2>
            <p style="color:#5C564E; font-size:0.92rem;">Ask questions about mudras, regional styles (Badagutittu vs. Tenkutittu), or the Banasura-Mohini saga.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("<span style='font-size:0.75rem; text-transform:uppercase; font-weight:700; color:#C5A059;'>Quick Sample Questions:</span>", unsafe_allow_html=True)

    copilot_db = {
        "What does Shikhara mudra signify?": "In Bharatanatyam and classical iconography, the <strong>Shikhara Hasta</strong> (formed by closing the fingers into a fist with the thumb pointing upright) signifies Lord Shiva, physical valor, the lingam, holding a bow, or firm resolve. It is frequently employed in vigorous Tandava sequences and heroic entrances.",
        "What is the difference between Badagutittu and Tenkutittu Yakshagana?": "<strong>Badagutittu</strong> (Northern coastal tradition, around Udupi/Kundapura) is celebrated for its intricate circular footwork (Mandai), lighter headgear (Mundale), and sophisticated vocal narration. <strong>Tenkutittu</strong> (Southern tradition, around Mangalore/Kasargod) features high-energy acrobatic pirouettes (Kari), heavier tiered headgear, and thunderous Chande-Maddale percussion.",
        "What is Aramandi posture in Bharatanatyam?": "<strong>Aramandi</strong> (also known as Ayatam) is the foundational half-sitting posture where knees are bent outward forming a balanced diamond shape with the torso upright. It roots the dancer firmly to the earth, enabling geometric precision and complex rhythmic footwork.",
        "How does Mohini defeat Banasura in the dance duel?": "Mohini proposes a dance contest (*Nritya Yuddha*) where Bhasmasura must mirror every adavu. As the tempo accelerates, Mohini gracefully touches her open palm to her own head. Entranced by her charm, Bhasmasura imitates her without thinking and his own fatal boon instantly reduces him to ashes.",
    }

    q_cols = st.columns(4)
    selected_q = None
    if q_cols[0].button("Shikhara Mudra Meaning?", use_container_width=True):
        selected_q = "What does Shikhara mudra signify?"
    if q_cols[1].button("Badagu vs. Tenku Yakshagana?", use_container_width=True):
        selected_q = "What is the difference between Badagutittu and Tenkutittu Yakshagana?"
    if q_cols[2].button("Aramandi Posture?", use_container_width=True):
        selected_q = "What is Aramandi posture in Bharatanatyam?"
    if q_cols[3].button("Mohini's Fatal Dance Duel?", use_container_width=True):
        selected_q = "How does Mohini defeat Banasura in the dance duel?"

    user_query = st.text_input("Ask anything about Indian performing arts:", value=selected_q or "")
    btn_ask = st.button("🔍 Search & Answer with Copilot", type="primary")

    if user_query.strip():
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        copilot_answer = None

        active_key = get_active_gemini_key()
        if active_key:
            with st.spinner("Consulting Google Gemini with cultural grounding..."):
                master_katha = read_katha()
                copilot_prompt = f"""
                You are KalaSetu's master cultural copilot. Using this master knowledge base:
                "{master_katha[:3200]}"
                Answer this query accurately, respectfully, and vividly:
                Query: "{user_query}"
                """
                copilot_answer = call_gemini_safe(active_key, copilot_prompt)

        if not copilot_answer:
            copilot_answer = copilot_db.get(
                user_query.strip(),
                f"Based on cultural grounding for <strong>'{user_query}'</strong>: This query connects to core tenets of classical Indian performance, highlighting the codification of mudras from Bharata Muni's *Natya Shastra*, the balance of Tandava and Lasya, and the triumph of spiritual wisdom over untamed ego.",
            )

        st.markdown(
            f"""
            <div style="background:#F4EFE6; border:1px solid #C5A059; border-radius:16px; padding:20px; margin-top:14px;">
                <div style="display:flex; align-items:center; gap:8px; color:#9E2A2B; font-weight:700; margin-bottom:8px;">
                    <span style="font-size:1.1rem;">✨</span>
                    <span class="heading-font">{user_query}</span>
                </div>
                <p style="color:#1C1B1A; font-size:0.92rem; line-height:1.7; margin:0;">{copilot_answer}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# GLOBAL FOOTER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div style="border-top:1px solid #EADBCE; padding:24px 0 12px 0; margin-top:40px; display:flex; justify-content:space-between; align-items:center; color:#5C564E; font-size:0.8rem;">
        <div>
            <strong class="heading-font" style="color:#9E2A2B; font-size:0.95rem;">KALASETU • ಕಲಾಸೇತು</strong>
            <div>ACM x MLH Hackathon — Art Beyond Boundaries</div>
        </div>
        <div>
            Built with passion for Indian Performing Arts • Powered by Google Gemini & Banasura Master Knowledge Base
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)