# file: app.py
import streamlit as st
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is required in environment")

client = OpenAI(api_key=OPENAI_API_KEY)
MODEL = "gpt-4o-mini"  # change if needed

# ------------------ Dummy DB (fed to the model only) ------------------
DUMMY_DB = {
  "meta": {
    "generated_on": "2025-11-11",
    "description": "Dummy MR dataset for POC. Use only this data to answer MR queries."
  },
  "sku_data": {
    "PARA500-TAB-10": {
      "sku_id": "PARA500-TAB-10",
      "brand": "Paracetamol 500",
      "pack_size": "10 tablets",
      "dosage_form": "Tablet",
      "strength": "500 mg",
      "mrp": 18.00
    },
    "PARA500-TAB-20": {
      "sku_id": "PARA500-TAB-20",
      "brand": "Paracetamol 500",
      "pack_size": "20 tablets",
      "dosage_form": "Tablet",
      "strength": "500 mg",
      "mrp": 32.00
    },
    "DOLO650-TAB-10": {
      "sku_id": "DOLO650-TAB-10",
      "brand": "Dolo 650",
      "pack_size": "10 tablets",
      "dosage_form": "Tablet",
      "strength": "650 mg",
      "mrp": 42.00
    },
    "DOLO650-TAB-20": {
      "sku_id": "DOLO650-TAB-20",
      "brand": "Dolo 650",
      "pack_size": "20 tablets",
      "dosage_form": "Tablet",
      "strength": "650 mg",
      "mrp": 80.00
    },
    "CARDIOGUARD-50MG-TAB-30": {
      "sku_id": "CARDIOGUARD-50MG-TAB-30",
      "brand": "CardioGuard®",
      "pack_size": "30 tablets",
      "dosage_form": "Tablet",
      "strength": "50 mg",
      "mrp": 150.00
    },
    "DIABETEX-500MG-TAB-30": {
      "sku_id": "DIABETEX-500MG-TAB-30",
      "brand": "Diabetex®",
      "pack_size": "30 tablets",
      "dosage_form": "Tablet",
      "strength": "500 mg",
      "mrp": 120.00
    },
    "NEURORELIEF-10MG-CAP-10": {
      "sku_id": "NEURORELIEF-10MG-CAP-10",
      "brand": "NeuroRelief®",
      "pack_size": "10 capsules",
      "dosage_form": "Capsule",
      "strength": "10 mg",
      "mrp": 95.00
    },
    "ALLERGYFREE-10MG-TAB-30": {
      "sku_id": "ALLERGYFREE-10MG-TAB-30",
      "brand": "AllergyFree®",
      "pack_size": "30 tablets",
      "dosage_form": "Tablet",
      "strength": "10 mg",
      "mrp": 60.00
    },
    "RESPIRACLEAR-100MG-TAB-10": {
      "sku_id": "RESPIRACLEAR-100MG-TAB-10",
      "brand": "RespiraClear®",
      "pack_size": "10 tablets",
      "dosage_form": "Tablet",
      "strength": "100 mg",
      "mrp": 85.00
    },
    "VITALVIT-S-TAB-30": {
      "sku_id": "VITALVIT-S-TAB-30",
      "brand": "VitalVit-S®",
      "pack_size": "30 tablets",
      "dosage_form": "Tablet",
      "strength": "Multivitamin",
      "mrp": 45.00
    }
  },
  "sales": {
    "mr_anna_kim": [
      {"date": "2025-11-01", "value": 50_000, "sku_count": 5, "skus": ["PARA500-TAB-10","DOLO650-TAB-10","NEURORELIEF-10MG-CAP-10","ALLERGYFREE-10MG-TAB-30","VITALVIT-S-TAB-30"]},
      {"date": "2025-11-06", "value": 76_000, "sku_count": 7, "skus": ["DOLO650-TAB-20","CARDIOGUARD-50MG-TAB-30","DIABETEX-500MG-TAB-30","NEURORELIEF-10MG-CAP-10","PARA500-TAB-20","VITALVIT-S-TAB-30","RESPIRACLEAR-100MG-TAB-10"]},
      {"date": "2025-10-05", "value": 45_000, "sku_count": 6, "skus": ["PARA500-TAB-10","ALLERGYFREE-10MG-TAB-30","RESPIRACLEAR-100MG-TAB-10","VITALVIT-S-TAB-30","DIABETEX-500MG-TAB-30","NEURORELIEF-10MG-CAP-10"]},
      {"date": "2025-09-02", "value": 42_000, "sku_count": 5, "skus": ["PARA500-TAB-20","DOLO650-TAB-10","ALLERGYFREE-10MG-TAB-30","VITALVIT-S-TAB-30","PARA500-TAB-10"]}
    ],
    "mr_john_smith": [
      {"date": "2025-11-02", "value": 38_000, "sku_count": 4, "skus": ["PARA500-TAB-10","PARA500-TAB-20","VITALVIT-S-TAB-30","RESPIRACLEAR-100MG-TAB-10"]},
      {"date": "2025-11-07", "value": 65_000, "sku_count": 6, "skus": ["DOLO650-TAB-10","DOLO650-TAB-20","CARDIOGUARD-50MG-TAB-30","PARA500-TAB-10","PARA500-TAB-20","ALLERGYFREE-10MG-TAB-30"]},
      {"date": "2025-10-10", "value": 52_000, "sku_count": 5, "skus": ["DIABETEX-500MG-TAB-30","NEURORELIEF-10MG-CAP-10","PARA500-TAB-10","VITALVIT-S-TAB-30","PARA500-TAB-20"]},
      {"date": "2025-09-12", "value": 48_000, "sku_count": 5, "skus": ["PARA500-TAB-20","ALLERGYFREE-10MG-TAB-30","RESPIRACLEAR-100MG-TAB-10","PARA500-TAB-10","NEURORELIEF-10MG-CAP-10"]}
    ],
    "mr_sophia_lopez": [
      {"date": "2025-11-03", "value": 90_000, "sku_count": 8, "skus": ["DOLO650-TAB-10","DOLO650-TAB-20","CARDIOGUARD-50MG-TAB-30","DIABETEX-500MG-TAB-30","NEURORELIEF-10MG-CAP-10","ALLERGYFREE-10MG-TAB-30","VITALVIT-S-TAB-30","RESPIRACLEAR-100MG-TAB-10"]},
      {"date": "2025-11-08", "value": 82_000, "sku_count": 7, "skus": ["DOLO650-TAB-20","CARDIOGUARD-50MG-TAB-30","DIABETEX-500MG-TAB-30","PARA500-TAB-20","RESPIRACLEAR-100MG-TAB-10","VITALVIT-S-TAB-30","NEURORELIEF-10MG-CAP-10"]},
      {"date": "2025-10-15", "value": 68_000, "sku_count": 6, "skus": ["PARA500-TAB-10","PARA500-TAB-20","DOLO650-TAB-10","ALLERGYFREE-10MG-TAB-30","NEURORELIEF-10MG-CAP-10","RESPIRACLEAR-100MG-TAB-10"]},
      {"date": "2025-09-20", "value": 60_000, "sku_count": 5, "skus": ["PARA500-TAB-10","DOLO650-TAB-10","VITALVIT-S-TAB-30","ALLERGYFREE-10MG-TAB-30","PARA500-TAB-20"]}
    ]
  },
  "rcpa": {
    "dr_tejas_m_patel": {
      "2025-Q3": {"NeuroRelief®": 47, "CardioGuard®": 33, "Diabetex®": 20},
      "2025-Q2": {"NeuroRelief®": 44, "CardioGuard®": 35, "Diabetex®": 21}
    },
    "dr_maria_gonzalez": {
      "2025-Q3": {"AllergyFree®": 50, "VitalVit-S®": 30, "RespiraClear®": 20},
      "2025-Q2": {"AllergyFree®": 48, "VitalVit-S®": 32, "RespiraClear®": 20}
    },
    "dr_li_wei": {
      "2025-Q3": {"NeuroRelief®": 45, "CardioGuard®": 40, "Diabetex®": 15},
      "2025-Q2": {"NeuroRelief®": 42, "CardioGuard®": 38, "Diabetex®": 20}
    },
    "dr_kevin_muller": {
      "2025-Q3": {"CardioGuard®": 44, "NeuroRelief®": 34, "AllergyFree®": 22},
      "2025-Q2": {"CardioGuard®": 41, "NeuroRelief®": 36, "AllergyFree®": 23}
    },
    "dr_olivia_svensson": {
      "2025-Q3": {"VitalVit-S®": 52, "RespiraClear®": 28, "Diabetex®": 20},
      "2025-Q2": {"VitalVit-S®": 50, "RespiraClear®": 30, "Diabetex®": 20}
    }
  },
  "inventory": {
    "dolo 650|ahmedabad": {"on_hand": 180, "days_of_cover": 9, "updated": "1h ago"},
    "paracetamol 500|mumbai": {"on_hand": 600, "days_of_cover": 30, "updated": "2d ago"},
    "cardioguard-50mg|new york": {"on_hand": 130, "days_of_cover": 7, "updated": "2h ago"},
    "diabetex-500mg|london": {"on_hand": 210, "days_of_cover": 11, "updated": "4h ago"},
    "neurorelief-10mg|bangkok": {"on_hand": 150, "days_of_cover": 10, "updated": "3h ago"},
    "allergyfree-10mg|toronto": {"on_hand": 305, "days_of_cover": 13, "updated": "5h ago"},
    "respiraclear-100mg|sydney": {"on_hand": 270, "days_of_cover": 12, "updated": "6h ago"},
    "vitalvit-s|cape town": {"on_hand": 440, "days_of_cover": 19, "updated": "8h ago"},
    "para500-tab-10|berlin": {"on_hand": 230, "days_of_cover": 12, "updated": "3h ago"},
    "brandBB-20mg-tab-30|mexico city": {"on_hand": 315, "days_of_cover": 14, "updated": "5h ago"}
  },
  "customer360": {
    "dr_tejas_m_patel": {
      "sales_last_3m": 140_000,
      "sales_last_6m": 275_000,
      "sales_last_12m": 510_000,
      "rcpa_snapshot": {"NeuroRelief®": 47, "CardioGuard®": 33, "Diabetex®": 20},
      "last_notes": [
        {"date": "2025-10-15", "note": "Requested additional sample pack for NeuroRelief®."},
        {"date": "2025-07-22", "note": "Interested in new clinical data on Diabetex®."}
      ],
      "sparkline": [23_000, 24_000, 26_000, 22_000, 20_000, 25_000]
    },
    "dr_maria_gonzalez": {
      "sales_last_3m": 120_000,
      "sales_last_6m": 240_000,
      "sales_last_12m": 460_000,
      "rcpa_snapshot": {"AllergyFree®": 50, "VitalVit-S®": 30, "RespiraClear®": 20},
      "last_notes": [
        {"date": "2025-10-01", "note": "Asked for bilingual brochure for AllergyFree®."},
        {"date": "2025-05-18", "note": "Interested in vitamin support via VitalVit-S®."}
      ],
      "sparkline": [20_000, 21_000, 22_500, 19_000, 18_000, 23_000]
    },
    "dr_li_wei": {
      "sales_last_3m": 130_000,
      "sales_last_6m": 260_000,
      "sales_last_12m": 500_000,
      "rcpa_snapshot": {"NeuroRelief®": 45, "CardioGuard®": 40, "Diabetex®": 15},
      "last_notes": [
        {"date": "2025-10-23", "note": "Requested Asia-Pacific event materials for NeuroRelief®."},
        {"date": "2025-06-12", "note": "Feedback: CardioGuard® performance good."}
      ],
      "sparkline": [22_000, 23_000, 24_000, 21_500, 21_000, 24_500]
    },
    "dr_kevin_muller": {
      "sales_last_3m": 115_000,
      "sales_last_6m": 230_000,
      "sales_last_12m": 470_000,
      "rcpa_snapshot": {"CardioGuard®": 44, "NeuroRelief®": 34, "AllergyFree®": 22},
      "last_notes": [
        {"date": "2025-10-09", "note": "Requested German-language datasheet for CardioGuard®."},
        {"date": "2025-05-26", "note": "Wants to trial AllergyFree® in new branch."}
      ],
      "sparkline": [19_000, 20_500, 21_000, 18_500, 18_000, 21_500]
    },
    "dr_olivia_svensson": {
      "sales_last_3m": 110_000,
      "sales_last_6m": 215_000,
      "sales_last_12m": 430_000,
      "rcpa_snapshot": {"VitalVit-S®": 52, "RespiraClear®": 28, "Diabetex®": 20},
      "last_notes": [
        {"date": "2025-10-18", "note": "Planning Nordic conference presence for VitalVit-S®."},
        {"date": "2025-05-14", "note": "Interested in patient engagement program for RespiraClear®."}
      ],
      "sparkline": [18_500, 19_000, 20_500, 17_000, 16_000, 20_000]
    }
  }
}

SYSTEM_PROMPT = f"""
You are MR Data Assistant — a friendly, short, and accurate assistant that answers MR (sales, inventory, RCPA, customer360, SKU) questions using ONLY the DATA_JSON below. Be conversational for greetings and clarifying follow-ups. Never invent facts.

Primary objectives:
- If the user asks a data question, return a concise factual answer (≤5 lines) computed from DATA_JSON.
- If the user asks a general/ambiguous question, try to resolve it with one short clarifying question; if none needed, use the sensible default described below.
- Keep conversation context (track last doctor, last SKU, last topic) to resolve pronouns and follow-ups.

Defaults & calculation rules (apply automatically):
- When the user asks for an overall best/ highest selling SKU without specifying a doctor, compute **across all sales records and all MRs**.
- Use this algorithm:
  1. Count occurrences: treat each SKU appearance inside a sales record's "skus" list as one sold pack (count occurrences across all dates and reps).
  2. Derive estimated revenue = occurrences × SKU MRP (from sku_data).
  3. Rank SKUs primarily by total occurrences (units sold). Break ties by estimated revenue.
- When user requests "best SKU for <doctor>" compute counts using only that doctor's sales entries.
- When user requests "top N" return top N by the same ranking rules.

Conversation flow (step-by-step):
1. Classify intent: GREETING / FAREWELL / SMALL_TALK / DATA_QUERY / CLARIFY / IRRELEVANT.
2. GREETING -> "Hello, how can I help you today?"
3. FAREWELL -> "Goodbye let me know if you need anything else."
4. SMALL_TALK -> short friendly reply (≤1 line).
5. DATA_QUERY:
   - If doctor or SKU not specified and needed, ask one short clarifying question (e.g., "Which doctor should I fetch data for?").
   - If user asked for an overall result (no doctor requested), run the default overall calculation above and reply.
6. CLARIFY & CONTEXT: remember last-specified doctor/SKU/topic to resolve pronouns ("his", "that", "it") and meta-requests ("repeat what I asked").
7. IRRELEVANT -> reply exactly: "Sorry, I don't have the information you're looking for. Can I help you with something else?"

Response style:
- Plain conversational text, no JSON or code in replies.
- Concise (≤5 lines). Friendly and professional.
- If appropriate, append a short offer: "Would you like more details?" 

DATA_JSON:
{ 
json.dumps(DUMMY_DB, indent=2)
}
(Use the full DATA_JSON inserted by the caller at runtime. Do not fetch external data.)

Take a deep breath and work on this problem step-by-step.
"""





# ------------------ UI (exact design) ----------------
st.set_page_config(page_title="MediRep Assistant", layout="centered")

st.markdown(
    """
    <style>
    main > div.block-container {
        max-width: 920px;
        margin: 28px auto !important;
        background: linear-gradient(180deg, #fbfdff 0%, #ffffff 100%);
        border-radius: 14px;
        padding: 22px 28px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
        border: 1px solid rgba(2,6,23,0.06);
    }
    body { background-color: #f3f6fb; }
    .main-title { text-align: center; font-size: 2.2rem; font-weight: 700; margin-bottom: 1rem; color: #2c3e50; }
    .intro-box {
        background: #f8fafc; color: #0f172a;
        padding: 12px 14px; border-radius: 12px;
        margin-bottom: 14px; border: 1px solid rgba(2,6,23,0.04);
        font-size: 0.95rem;
    }
    .chat-bubble-user {
        background-color: #2563eb; color: white;
        padding: 10px 15px; border-radius: 14px 14px 0 14px;
        margin: 6px 0; margin-left: auto; max-width: 75%;
        white-space: pre-wrap;
    }
    .chat-bubble-assistant {
        background-color: #374151; color: #e5e7eb;
        padding: 10px 15px; border-radius: 14px 14px 14px 0;
        margin: 6px 0; max-width: 75%;
        white-space: pre-wrap;
    }
    /* new typing bubble style: lightest grey and fits text width */
    .chat-bubble-typing {
        background-color: #f3f4f6; color: #374151;
        padding: 6px 10px;
        border-radius: 12px 12px 12px 0;
        margin: 6px 0;
        display: inline-block;
        font-style: italic;
        font-size: 0.95rem;
    }
    .typing { opacity: 0.9; font-style: italic; }
    div.stButton > button {
        background-color: #2563eb !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 8px 14px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 10px rgba(37,99,235,0.15) !important;
    }
    div.stDownloadButton > button {
        background-color: #10b981 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 8px 14px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 10px rgba(16,185,129,0.12) !important;
    }
    .transcript-area { font-family: monospace; white-space: pre-wrap; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">🩺 MediRep Assistant</div>', unsafe_allow_html=True)

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# single placeholder for rendering chat (prevents duplicate rendering)
chat_placeholder = st.empty()

# Render function that writes into the chat_placeholder only
def render_into_placeholder():
    with chat_placeholder.container():
        # show intro box inside placeholder only when there are no user messages
        user_messages_exist = any(m["role"] == "user" for m in st.session_state.messages)
        if not user_messages_exist:
            st.markdown(
                '<div class="intro-box">Ask about MR data (sales, RCPA, inventory, Customer 360). The assistant will answer using the data available to it.</div>',
                unsafe_allow_html=True
            )

        # show each assistant/user message in order (skip system)
        for msg in st.session_state.messages:
            if msg["role"] == "system":
                continue
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
            elif msg["role"] == "assistant":
                # if this assistant message is a typing placeholder, render the typing bubble (light grey)
                # we detect typing placeholders by exact html we insert below
                if msg["content"] == "<div class='chat-bubble-typing'>Thinking...</div>":
                    st.markdown(msg["content"], unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-bubble-assistant'>{msg['content']}</div>", unsafe_allow_html=True)

# Show current history initially
render_into_placeholder()

# Capture user input
user_input = st.chat_input("Type your question...")

if user_input:
    # 1) Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2) Append assistant typing placeholder (use the exact div html so we can detect it later)
    typing_html = "<div class='chat-bubble-typing'>Thinking...</div>"
    st.session_state.messages.append({"role": "assistant", "content": typing_html})

    # 3) Render immediately (user + typing visible)
    render_into_placeholder()

    # 4) Call model (full conversation) - exclude the typing placeholder when sending
    try:
        to_send = []
        for m in st.session_state.messages:
            if m["role"] == "assistant" and m["content"] == typing_html:
                continue
            to_send.append({"role": m["role"], "content": m["content"]})

        resp = client.chat.completions.create(
            model=MODEL,
            messages=to_send,
            temperature=0.0,
            max_tokens=700
        )
        try:
            assistant_reply = resp.choices[0].message.content.strip()
        except Exception:
            assistant_reply = str(resp)
    except Exception:
        assistant_reply = "Sorry — could not get a response right now."

    # 5) Replace the last assistant placeholder content with real reply (in-place)
    for i in range(len(st.session_state.messages)-1, -1, -1):
        if st.session_state.messages[i]["role"] == "assistant" and st.session_state.messages[i]["content"] == typing_html:
            st.session_state.messages[i]["content"] = assistant_reply
            break

    # 6) Re-render into the same placeholder so the typing bubble is replaced
    render_into_placeholder()
