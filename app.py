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
EXPANDED_DUMMY_DB = {
  "meta": {
    "generated_on": "2025-11-11",
    "description": "Expanded dummy MR dataset for POC. Based on original DUMMY_DB, enlarged with additional SKUs, sales reps, rcpa entries, inventory locations and customer360 records."
  },
  "sku_data": {
    "PARA500-TAB-10": {"sku_id": "PARA500-TAB-10","brand": "Paracetamol 500","pack_size": "10 tablets","dosage_form": "Tablet","strength": "500 mg","mrp": 18.00},
    "PARA500-TAB-20": {"sku_id": "PARA500-TAB-20","brand": "Paracetamol 500","pack_size": "20 tablets","dosage_form": "Tablet","strength": "500 mg","mrp": 32.00},
    "DOLO650-TAB-10": {"sku_id": "DOLO650-TAB-10","brand": "Dolo 650","pack_size": "10 tablets","dosage_form": "Tablet","strength": "650 mg","mrp": 42.00},
    "DOLO650-TAB-20": {"sku_id": "DOLO650-TAB-20","brand": "Dolo 650","pack_size": "20 tablets","dosage_form": "Tablet","strength": "650 mg","mrp": 80.00},
    "CARDIOGUARD-50MG-TAB-30": {"sku_id": "CARDIOGUARD-50MG-TAB-30","brand": "CardioGuard®","pack_size": "30 tablets","dosage_form": "Tablet","strength": "50 mg","mrp": 150.00},
    "DIABETEX-500MG-TAB-30": {"sku_id": "DIABETEX-500MG-TAB-30","brand": "Diabetex®","pack_size": "30 tablets","dosage_form": "Tablet","strength": "500 mg","mrp": 120.00},
    "NEURORELIEF-10MG-CAP-10": {"sku_id": "NEURORELIEF-10MG-CAP-10","brand": "NeuroRelief®","pack_size": "10 capsules","dosage_form": "Capsule","strength": "10 mg","mrp": 95.00},
    "ALLERGYFREE-10MG-TAB-30": {"sku_id": "ALLERGYFREE-10MG-TAB-30","brand": "AllergyFree®","pack_size": "30 tablets","dosage_form": "Tablet","strength": "10 mg","mrp": 60.00},
    "RESPIRACLEAR-100MG-TAB-10": {"sku_id": "RESPIRACLEAR-100MG-TAB-10","brand": "RespiraClear®","pack_size": "10 tablets","dosage_form": "Tablet","strength": "100 mg","mrp": 85.00},
    "VITALVIT-S-TAB-30": {"sku_id": "VITALVIT-S-TAB-30","brand": "VitalVit-S®","pack_size": "30 tablets","dosage_form": "Tablet","strength": "Multivitamin","mrp": 45.00},

    "AMOX500-CAP-10": {"sku_id": "AMOX500-CAP-10","brand": "AmoxiPlus","pack_size": "10 capsules","dosage_form": "Capsule","strength": "500 mg","mrp": 55.00},
    "AZITH250-TAB-3": {"sku_id": "AZITH250-TAB-3","brand": "Azithro","pack_size": "3 tablets","dosage_form": "Tablet","strength": "250 mg","mrp": 48.00},
    "ATORVA20-TAB-30": {"sku_id": "ATORVA20-TAB-30","brand": "Atorva","pack_size": "30 tablets","dosage_form": "Tablet","strength": "20 mg","mrp": 220.00},
    "LISIN10-TAB-30": {"sku_id": "LISIN10-TAB-30","brand": "Lisinex","pack_size": "30 tablets","dosage_form": "Tablet","strength": "10 mg","mrp": 95.00},
    "METFORMIN-500-TAB-60": {"sku_id": "METFORMIN-500-TAB-60","brand": "GlucoSafe","pack_size": "60 tablets","dosage_form": "Tablet","strength": "500 mg","mrp": 140.00},
    "OMEGA3-1000-TAB-30": {"sku_id": "OMEGA3-1000-TAB-30","brand": "CardioOmega","pack_size": "30 tablets","dosage_form": "Tablet","strength": "1000 mg","mrp": 180.00},
    "OMEPRAZOLE-20-TAB-14": {"sku_id": "OMEPRAZOLE-20-TAB-14","brand": "Omepral","pack_size": "14 tablets","dosage_form": "Tablet","strength": "20 mg","mrp": 72.00},
    "SALBUTAMOL-2MG-INH-1": {"sku_id": "SALBUTAMOL-2MG-INH-1","brand": "BreatheEasy","pack_size": "1 inhaler","dosage_form": "Inhaler","strength": "2 mg","mrp": 350.00},
    "RANITIDINE-150-TAB-15": {"sku_id": "RANITIDINE-150-TAB-15","brand": "AcidNoMore","pack_size": "15 tablets","dosage_form": "Tablet","strength": "150 mg","mrp": 85.00},
    "CLARITHRO-500TAB-14": {"sku_id": "CLARITHRO-500TAB-14","brand": "Clarithro","pack_size": "14 tablets","dosage_form": "Tablet","strength": "500 mg","mrp": 260.00},

    "CEFTRIAX-1G-VIAL-1": {"sku_id": "CEFTRIAX-1G-VIAL-1","brand": "Ceftriax","pack_size": "1 vial","dosage_form": "Injectable","strength": "1 g","mrp": 325.00},
    "HYGRO-200MG-TAB-10": {"sku_id": "HYGRO-200MG-TAB-10","brand": "Hygrofen","pack_size": "10 tablets","dosage_form": "Tablet","strength": "200 mg","mrp": 72.00},
    "PREDNISOL-5MG-TAB-30": {"sku_id": "PREDNISOL-5MG-TAB-30","brand": "Prednisol","pack_size": "30 tablets","dosage_form": "Tablet","strength": "5 mg","mrp": 150.00},
    "ZOLPIDEM-10MG-TAB-10": {"sku_id": "ZOLPIDEM-10MG-TAB-10","brand": "SleepWell","pack_size": "10 tablets","dosage_form": "Tablet","strength": "10 mg","mrp": 95.00},
    "IBUPROF-400-TAB-10": {"sku_id": "IBUPROF-400-TAB-10","brand": "IbuFast","pack_size": "10 tablets","dosage_form": "Tablet","strength": "400 mg","mrp": 40.00},
    "FEXOFEN-120MG-TAB-10": {"sku_id": "FEXOFEN-120MG-TAB-10","brand": "FexoClear","pack_size": "10 tablets","dosage_form": "Tablet","strength": "120 mg","mrp": 70.00},
    "LEVOCET-5MG-TAB-10": {"sku_id": "LEVOCET-5MG-TAB-10","brand": "LevoC","pack_size": "10 tablets","dosage_form": "Tablet","strength": "5 mg","mrp": 85.00},
    "VITD-1000IU-TAB-30": {"sku_id": "VITD-1000IU-TAB-30","brand": "SunD","pack_size": "30 tablets","dosage_form": "Tablet","strength": "1000 IU","mrp": 120.00},
    "COLDRELIEF-SYR-100ML": {"sku_id": "COLDRELIEF-SYR-100ML","brand": "ColdRelief","pack_size": "100 ml","dosage_form": "Syrup","strength": "N/A","mrp": 95.00},
    "ANTACID-GEL-200ML": {"sku_id": "ANTACID-GEL-200ML","brand": "NeutralB","pack_size": "200 ml","dosage_form": "Gel","strength": "N/A","mrp": 60.00}
  },

  "sales": {
    "mr_anna_kim": [
      {"date": "2025-11-01", "value": 50000, "sku_count": 5, "skus": ["PARA500-TAB-10","DOLO650-TAB-10","NEURORELIEF-10MG-CAP-10","ALLERGYFREE-10MG-TAB-30","VITALVIT-S-TAB-30"]},
      {"date": "2025-11-06", "value": 76000, "sku_count": 7, "skus": ["DOLO650-TAB-20","CARDIOGUARD-50MG-TAB-30","DIABETEX-500MG-TAB-30","NEURORELIEF-10MG-CAP-10","PARA500-TAB-20","VITALVIT-S-TAB-30","RESPIRACLEAR-100MG-TAB-10"]},
      {"date": "2025-10-05", "value": 45000, "sku_count": 6, "skus": ["PARA500-TAB-10","ALLERGYFREE-10MG-TAB-30","RESPIRACLEAR-100MG-TAB-10","VITALVIT-S-TAB-30","DIABETEX-500MG-TAB-30","NEURORELIEF-10MG-CAP-10"]},
      {"date": "2025-09-02", "value": 42000, "sku_count": 5, "skus": ["PARA500-TAB-20","DOLO650-TAB-10","ALLERGYFREE-10MG-TAB-30","VITALVIT-S-TAB-30","PARA500-TAB-10"]},
      {"date": "2025-08-17", "value": 38000, "sku_count": 5, "skus": ["IBUPROF-400-TAB-10","PARA500-TAB-10","VITD-1000IU-TAB-30","COLDRELIEF-SYR-100ML","ANTACID-GEL-200ML"]},
      {"date": "2025-06-11", "value": 47000, "sku_count": 6, "skus": ["AMOX500-CAP-10","AZITH250-TAB-3","OMEGA3-1000-TAB-30","PARA500-TAB-20","DOLO650-TAB-10","ALLERGYFREE-10MG-TAB-30"]}
    ],

    "mr_john_smith": [
      {"date": "2025-11-02", "value": 38000, "sku_count": 4, "skus": ["PARA500-TAB-10","PARA500-TAB-20","VITALVIT-S-TAB-30","RESPIRACLEAR-100MG-TAB-10"]},
      {"date": "2025-11-07", "value": 65000, "sku_count": 6, "skus": ["DOLO650-TAB-10","DOLO650-TAB-20","CARDIOGUARD-50MG-TAB-30","PARA500-TAB-10","PARA500-TAB-20","ALLERGYFREE-10MG-TAB-30"]},
      {"date": "2025-10-10", "value": 52000, "sku_count": 5, "skus": ["DIABETEX-500MG-TAB-30","NEURORELIEF-10MG-CAP-10","PARA500-TAB-10","VITALVIT-S-TAB-30","PARA500-TAB-20"]},
      {"date": "2025-09-12", "value": 48000, "sku_count": 5, "skus": ["PARA500-TAB-20","ALLERGYFREE-10MG-TAB-30","RESPIRACLEAR-100MG-TAB-10","PARA500-TAB-10","NEURORELIEF-10MG-CAP-10"]},
      {"date": "2025-07-22", "value": 43000, "sku_count": 5, "skus": ["ATORVA20-TAB-30","LISIN10-TAB-30","VITALVIT-S-TAB-30","PARA500-TAB-10","OMEGA3-1000-TAB-30"]},
      {"date": "2025-05-15", "value": 36000, "sku_count": 4, "skus": ["AMOX500-CAP-10","AZITH250-TAB-3","COLDRELIEF-SYR-100ML","ANTACID-GEL-200ML"]}
    ],

    "mr_sophia_lopez": [
      {"date": "2025-11-03", "value": 90000, "sku_count": 8, "skus": ["DOLO650-TAB-10","DOLO650-TAB-20","CARDIOGUARD-50MG-TAB-30","DIABETEX-500MG-TAB-30","NEURORELIEF-10MG-CAP-10","ALLERGYFREE-10MG-TAB-30","VITALVIT-S-TAB-30","RESPIRACLEAR-100MG-TAB-10"]},
      {"date": "2025-11-08", "value": 82000, "sku_count": 7, "skus": ["DOLO650-TAB-20","CARDIOGUARD-50MG-TAB-30","DIABETEX-500MG-TAB-30","PARA500-TAB-20","RESPIRACLEAR-100MG-TAB-10","VITALVIT-S-TAB-30","NEURORELIEF-10MG-CAP-10"]},
      {"date": "2025-10-15", "value": 68000, "sku_count": 6, "skus": ["PARA500-TAB-10","PARA500-TAB-20","DOLO650-TAB-10","ALLERGYFREE-10MG-TAB-30","NEURORELIEF-10MG-CAP-10","RESPIRACLEAR-100MG-TAB-10"]},
      {"date": "2025-09-20", "value": 60000, "sku_count": 5, "skus": ["PARA500-TAB-10","DOLO650-TAB-10","VITALVIT-S-TAB-30","ALLERGYFREE-10MG-TAB-30","PARA500-TAB-20"]},
      {"date": "2025-06-28", "value": 54000, "sku_count": 6, "skus": ["CEFTRIAX-1G-VIAL-1","PREDNISOL-5MG-TAB-30","CLARITHRO-500TAB-14","PARA500-TAB-10","VITD-1000IU-TAB-30","IBUPROF-400-TAB-10"]},
      {"date": "2025-03-11", "value": 47000, "sku_count": 5, "skus": ["LISIN10-TAB-30","ATORVA20-TAB-30","OMEGA3-1000-TAB-30","PARA500-TAB-10","DOLO650-TAB-10"]}
    ],

    "mr_liam_nguyen": [
      {"date": "2025-11-04", "value": 72000, "sku_count": 7, "skus": ["ATORVA20-TAB-30","LISIN10-TAB-30","OMEGA3-1000-TAB-30","CARDIOGUARD-50MG-TAB-30","VITD-1000IU-TAB-30","PARA500-TAB-10","IBUPROF-400-TAB-10"]},
      {"date": "2025-10-09", "value": 51000, "sku_count": 5, "skus": ["METFORMIN-500-TAB-60","DIABETEX-500MG-TAB-30","PARA500-TAB-20","DOLO650-TAB-10","FEXOFEN-120MG-TAB-10"]},
      {"date": "2025-08-03", "value": 43000, "sku_count": 4, "skus": ["OMEPRAZOLE-20-TAB-14","RANITIDINE-150-TAB-15","ANTACID-GEL-200ML","COLDRELIEF-SYR-100ML"]},
      {"date": "2025-05-30", "value": 39000, "sku_count": 4, "skus": ["AMOX500-CAP-10","AZITH250-TAB-3","CLARITHRO-500TAB-14","CEFTRIAX-1G-VIAL-1"]}
    ],

    "mr_ayesha_khan": [
      {"date": "2025-11-05", "value": 66000, "sku_count": 6, "skus": ["NEURORELIEF-10MG-CAP-10","CARDIOGUARD-50MG-TAB-30","DIABETEX-500MG-TAB-30","VITALVIT-S-TAB-30","PARA500-TAB-20","FEXOFEN-120MG-TAB-10"]},
      {"date": "2025-09-28", "value": 48000, "sku_count": 5, "skus": ["LEVOCET-5MG-TAB-10","ALLERGYFREE-10MG-TAB-30","VITD-1000IU-TAB-30","PARA500-TAB-10","IBUPROF-400-TAB-10"]},
      {"date": "2025-06-12", "value": 41000, "sku_count": 4, "skus": ["COLDRELIEF-SYR-100ML","ANTACID-GEL-200ML","OMEPRAZOLE-20-TAB-14","RANITIDINE-150-TAB-15"]}
    ],

    "mr_chen_hua": [
      {"date": "2025-11-06", "value": 72000, "sku_count": 7, "skus": ["NEURORELIEF-10MG-CAP-10","CARDIOGUARD-50MG-TAB-30","ATORVA20-TAB-30","OMEGA3-1000-TAB-30","PARA500-TAB-10","PREDNISOL-5MG-TAB-30","CEFTRIAX-1G-VIAL-1"]},
      {"date": "2025-10-02", "value": 53000, "sku_count": 5, "skus": ["DIABETEX-500MG-TAB-30","METFORMIN-500-TAB-60","PARA500-TAB-20","DOLO650-TAB-20","CLARITHRO-500TAB-14"]},
      {"date": "2025-07-18", "value": 36000, "sku_count": 4, "skus": ["AMOX500-CAP-10","AZITH250-TAB-3","CEFTRIAX-1G-VIAL-1","OMEGA3-1000-TAB-30"]}
    ],

    "mr_lucas_martinez": [
      {"date": "2025-11-01", "value": 48000, "sku_count": 5, "skus": ["PARA500-TAB-20","DOLO650-TAB-20","VITALVIT-S-TAB-30","RESPIRACLEAR-100MG-TAB-10","ALLERGYFREE-10MG-TAB-30"]},
      {"date": "2025-09-05", "value": 42000, "sku_count": 4, "skus": ["PARA500-TAB-10","IBUPROF-400-TAB-10","VITD-1000IU-TAB-30","COLDRELIEF-SYR-100ML"]},
      {"date": "2025-06-22", "value": 39000, "sku_count": 4, "skus": ["LISIN10-TAB-30","ATORVA20-TAB-30","CARDIOGUARD-50MG-TAB-30","OMEGA3-1000-TAB-30"]}
    ],

    "mr_emma_jones": [
      {"date": "2025-11-07", "value": 54000, "sku_count": 6, "skus": ["ALLERGYFREE-10MG-TAB-30","RESPIRACLEAR-100MG-TAB-10","LEVOCET-5MG-TAB-10","VITD-1000IU-TAB-30","PARA500-TAB-10","COLDRELIEF-SYR-100ML"]},
      {"date": "2025-08-14", "value": 36000, "sku_count": 4, "skus": ["OMEPRAZOLE-20-TAB-14","RANITIDINE-150-TAB-15","ANTACID-GEL-200ML","ZOLPIDEM-10MG-TAB-10"]},
      {"date": "2025-04-09", "value": 29000, "sku_count": 3, "skus": ["PARA500-TAB-10","IBUPROF-400-TAB-10","VITD-1000IU-TAB-30"]}
    ],

    "mr_felix_schmidt": [
      {"date": "2025-11-02", "value": 69000, "sku_count": 7, "skus": ["CARDIOGUARD-50MG-TAB-30","ATORVA20-TAB-30","OMEGA3-1000-TAB-30","LISIN10-TAB-30","PARA500-TAB-20","IBUPROF-400-TAB-10","VITALVIT-S-TAB-30"]},
      {"date": "2025-10-05", "value": 44000, "sku_count": 4, "skus": ["CEFTRIAX-1G-VIAL-1","CLARITHRO-500TAB-14","AMOX500-CAP-10","AZITH250-TAB-3"]}
    ],

    "mr_marta_rodriguez": [
      {"date": "2025-11-03", "value": 53000, "sku_count": 6, "skus": ["DIABETEX-500MG-TAB-30","METFORMIN-500-TAB-60","PARA500-TAB-10","VITD-1000IU-TAB-30","IBUPROF-400-TAB-10","ANTACID-GEL-200ML"]},
      {"date": "2025-07-12", "value": 39000, "sku_count": 4, "skus": ["ALLERGYFREE-10MG-TAB-30","LEVOCET-5MG-TAB-10","RESPIRACLEAR-100MG-TAB-10","COLDRELIEF-SYR-100ML"]}
    ],

    "mr_omar_ali": [
      {"date": "2025-11-06", "value": 47000, "sku_count": 5, "skus": ["PARA500-TAB-10","DOLO650-TAB-10","PARA500-TAB-20","VITALVIT-S-TAB-30","IBUPROF-400-TAB-10"]},
      {"date": "2025-08-29", "value": 36000, "sku_count": 4, "skus": ["OMEPRAZOLE-20-TAB-14","ANTACID-GEL-200ML","RANITIDINE-150-TAB-15","COLDRELIEF-SYR-100ML"]}
    ],

    "mr_kate_wilson": [
      {"date": "2025-10-30", "value": 62000, "sku_count": 6, "skus": ["NEURORELIEF-10MG-CAP-10","CARDIOGUARD-50MG-TAB-30","ATORVA20-TAB-30","OMEGA3-1000-TAB-30","PARA500-TAB-20","VITALVIT-S-TAB-30"]},
      {"date": "2025-06-18", "value": 41000, "sku_count": 4, "skus": ["AMOX500-CAP-10","AZITH250-TAB-3","CLARITHRO-500TAB-14","CEFTRIAX-1G-VIAL-1"]}
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
    },

    "dr_anna_petrov": {
      "2025-Q3": {"CardioGuard®": 38, "Atorva": 30, "NeuroRelief®": 32},
      "2025-Q2": {"CardioGuard®": 36, "Atorva": 32, "NeuroRelief®": 32}
    },
    "dr_kamran_hussain": {
      "2025-Q3": {"Diabetex®": 46, "Metformin": 30, "CardioGuard®": 24},
      "2025-Q2": {"Diabetex®": 44, "Metformin": 32, "CardioGuard®": 24}
    },
    "dr_sophie_dubois": {
      "2025-Q3": {"VitalVit-S®": 40, "AllergyFree®": 35, "RespiraClear®": 25},
      "2025-Q2": {"VitalVit-S®": 38, "AllergyFree®": 36, "RespiraClear®": 26}
    },
    "dr_akiko_tanaka": {
      "2025-Q3": {"NeuroRelief®": 43, "CardioGuard®": 37, "VitalVit-S®": 20},
      "2025-Q2": {"NeuroRelief®": 41, "CardioGuard®": 39, "VitalVit-S®": 20}
    },
    "dr_pedro_morales": {
      "2025-Q3": {"AllergyFree®": 42, "RespiraClear®": 33, "VitalVit-S®": 25},
      "2025-Q2": {"AllergyFree®": 40, "RespiraClear®": 34, "VitalVit-S®": 26}
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
    "brandBB-20mg-tab-30|mexico city": {"on_hand": 315, "days_of_cover": 14, "updated": "5h ago"},

    "atorva20-tab-30|madrid": {"on_hand": 160, "days_of_cover": 10, "updated": "2h ago"},
    "lisin10-tab-30|paris": {"on_hand": 190, "days_of_cover": 12, "updated": "3h ago"},
    "metformin-500-tab-60|delhi": {"on_hand": 420, "days_of_cover": 25, "updated": "1d ago"},
    "omeg a3-1000-tab-30|san francisco": {"on_hand": 140, "days_of_cover": 9, "updated": "4h ago"},
    "amox500-cap-10|jakarta": {"on_hand": 210, "days_of_cover": 11, "updated": "3h ago"},
    "azith250-tab-3|manila": {"on_hand": 330, "days_of_cover": 18, "updated": "5h ago"},
    "ceftriax-1g-vial-1|cairo": {"on_hand": 85, "days_of_cover": 6, "updated": "6h ago"},
    "omeprazole-20-tab-14|milan": {"on_hand": 190, "days_of_cover": 14, "updated": "8h ago"},
    "salbutamol-inh|abu dhabi": {"on_hand": 120, "days_of_cover": 7, "updated": "2h ago"},
    "vitd-1000iu-tab-30|johannesburg": {"on_hand": 400, "days_of_cover": 22, "updated": "10h ago"},
    "ibuprof-400-tab-10|istanbul": {"on_hand": 260, "days_of_cover": 15, "updated": "4h ago"},
    "clarithro-500tab-14|sao paulo": {"on_hand": 95, "days_of_cover": 7, "updated": "2h ago"},
    "coldrelief-syr-100ml|bangalore": {"on_hand": 380, "days_of_cover": 20, "updated": "3h ago"},
    "antacid-gel-200ml|kuala lumpur": {"on_hand": 210, "days_of_cover": 12, "updated": "6h ago"},
    "fexofen-120mg-tab-10|vancouver": {"on_hand": 150, "days_of_cover": 11, "updated": "5h ago"}
  },

  "customer360": {
    "dr_tejas_m_patel": {
      "sales_last_3m": 140000,
      "sales_last_6m": 275000,
      "sales_last_12m": 510000,
      "rcpa_snapshot": {"NeuroRelief®": 47, "CardioGuard®": 33, "Diabetex®": 20},
      "last_notes": [
        {"date": "2025-10-15", "note": "Requested additional sample pack for NeuroRelief®."},
        {"date": "2025-07-22", "note": "Interested in new clinical data on Diabetex®."}
      ],
      "sparkline": [23000, 24000, 26000, 22000, 20000, 25000]
    },
    "dr_maria_gonzalez": {
      "sales_last_3m": 120000,
      "sales_last_6m": 240000,
      "sales_last_12m": 460000,
      "rcpa_snapshot": {"AllergyFree®": 50, "VitalVit-S®": 30, "RespiraClear®": 20},
      "last_notes": [
        {"date": "2025-10-01", "note": "Asked for bilingual brochure for AllergyFree®."},
        {"date": "2025-05-18", "note": "Interested in vitamin support via VitalVit-S®."}
      ],
      "sparkline": [20000, 21000, 22500, 19000, 18000, 23000]
    },
    "dr_li_wei": {
      "sales_last_3m": 130000,
      "sales_last_6m": 260000,
      "sales_last_12m": 500000,
      "rcpa_snapshot": {"NeuroRelief®": 45, "CardioGuard®": 40, "Diabetex®": 15},
      "last_notes": [
        {"date": "2025-10-23", "note": "Requested Asia-Pacific event materials for NeuroRelief®."},
        {"date": "2025-06-12", "note": "Feedback: CardioGuard® performance good."}
      ],
      "sparkline": [22000, 23000, 24000, 21500, 21000, 24500]
    },
    "dr_kevin_muller": {
      "sales_last_3m": 115000,
      "sales_last_6m": 230000,
      "sales_last_12m": 470000,
      "rcpa_snapshot": {"CardioGuard®": 44, "NeuroRelief®": 34, "AllergyFree®": 22},
      "last_notes": [
        {"date": "2025-10-09", "note": "Requested German-language datasheet for CardioGuard®."},
        {"date": "2025-05-26", "note": "Wants to trial AllergyFree® in new branch."}
      ],
      "sparkline": [19000, 20500, 21000, 18500, 18000, 21500]
    },
    "dr_olivia_svensson": {
      "sales_last_3m": 110000,
      "sales_last_6m": 215000,
      "sales_last_12m": 430000,
      "rcpa_snapshot": {"VitalVit-S®": 52, "RespiraClear®": 28, "Diabetex®": 20},
      "last_notes": [
        {"date": "2025-10-18", "note": "Planning Nordic conference presence for VitalVit-S®."},
        {"date": "2025-05-14", "note": "Interested in patient engagement program for RespiraClear®."}
      ],
      "sparkline": [18500, 19000, 20500, 17000, 16000, 20000]
    },

    "dr_anna_petrov": {
      "sales_last_3m": 95000,
      "sales_last_6m": 190000,
      "sales_last_12m": 380000,
      "rcpa_snapshot": {"CardioGuard®": 38, "Atorva": 30, "NeuroRelief®": 32},
      "last_notes": [
        {"date": "2025-09-30", "note": "Wants patient leaflet in Russian for CardioGuard®."},
        {"date": "2025-04-21", "note": "Interested in lipid management data."}
      ],
      "sparkline": [15000, 16000, 17000, 14000, 13000, 17000]
    },
    "dr_kamran_hussain": {
      "sales_last_3m": 125000,
      "sales_last_6m": 250000,
      "sales_last_12m": 510000,
      "rcpa_snapshot": {"Diabetex®": 46, "Metformin": 30, "CardioGuard®": 24},
      "last_notes": [
        {"date": "2025-10-05", "note": "Asked for local diabetic management posters."},
        {"date": "2025-06-30", "note": "Requested educational grant application form."}
      ],
      "sparkline": [20000, 21000, 22000, 19000, 18500, 24000]
    },
    "dr_sophie_dubois": {
      "sales_last_3m": 98000,
      "sales_last_6m": 195000,
      "sales_last_12m": 400000,
      "rcpa_snapshot": {"VitalVit-S®": 40, "AllergyFree®": 35, "RespiraClear®": 25},
      "last_notes": [
        {"date": "2025-10-11", "note": "Interested in co-branded patient leaflets."},
        {"date": "2025-07-01", "note": "Wants to trial RespiraClear® at outpatient clinic."}
      ],
      "sparkline": [16000, 16500, 17500, 15000, 14800, 18500]
    },
    "dr_akiko_tanaka": {
      "sales_last_3m": 102000,
      "sales_last_6m": 205000,
      "sales_last_12m": 430000,
      "rcpa_snapshot": {"NeuroRelief®": 43, "CardioGuard®": 37, "VitalVit-S®": 20},
      "last_notes": [
        {"date": "2025-10-20", "note": "Requested Asia-Pacific clinical slides for NeuroRelief®."},
        {"date": "2025-06-19", "note": "Inquired about samples for VitalVit-S®."}
      ],
      "sparkline": [17000, 17500, 18500, 16000, 15800, 20500]
    },
    "dr_pedro_morales": {
      "sales_last_3m": 87000,
      "sales_last_6m": 170000,
      "sales_last_12m": 350000,
      "rcpa_snapshot": {"AllergyFree®": 42, "RespiraClear®": 33, "VitalVit-S®": 25},
      "last_notes": [
        {"date": "2025-10-14", "note": "Asked for discount pricing on bulk allergy kits."},
        {"date": "2025-05-05", "note": "Requested in-clinic signage for RespiraClear®."}
      ],
      "sparkline": [14000, 14500, 15000, 13500, 13200, 17000]
    }
  }
}

SYSTEM_PROMPT = f"""
Act like MR Data Assistant - a friendly, concise, and accurate assistant that answers MR (sales, inventory, RCPA, customer360, SKU) questions using ONLY the DATA_JSON below. Be conversational for greetings and clarifying follow-ups. Never invent facts.

Primary objectives:
- For data questions, return concise factual answers (no more than five lines) computed strictly from DATA_JSON.
- For general or ambiguous questions, ask one short clarifying question; if none is required, use sensible defaults defined below.
- Maintain conversation context: track last-mentioned entities (doctor, SKU, MR, product, or topic) to resolve pronouns and follow-ups.

When the user request or topic is outside the medical, MR, or sales-related scope of DATA_JSON:
- Respond dynamically and politely, e.g.: "I am a medical chatbot prototype and can only help with medical or MR-related information. Please ask me something related to sales, inventory, or medical data."
- Avoid using any fixed or hard-coded examples; automatically adjust the reply depending on the user’s request type.
- Offer a gentle follow-up like: "Would you like to know about sales or doctor data instead?"
- Never fabricate answers or external details outside the available dataset.

When the requested entity (doctor, SKU, MR, product, or customer) is not found in DATA_JSON:
- Respond transparently and dynamically: "I am a prototype bot with limited data access. Here is what I currently have data for:" then list available entities of the same type from DATA_JSON.
- Do not hard-code entity names; determine the relevant type based on the user’s question.
- Suggest one short next step, such as: "Would you like me to show data for one of these instead?"

Defaults and calculation rules:
- When the user asks for an overall or highest performing result without specifying an entity, compute across all available data in DATA_JSON.
- Algorithm:
  1. Count occurrences: each SKU appearance inside a sales record's "skus" list equals one sold pack.
  2. Estimated revenue = occurrences × SKU MRP from sku_data.
  3. Rank SKUs primarily by total occurrences; break ties by estimated revenue.
- For "top N" or "best" type questions, apply the same ranking rules dynamically to available data.

Conversation flow:
1. Classify intent: GREETING / FAREWELL / SMALL_TALK / DATA_QUERY / OUT_OF_SCOPE / CLARIFY / IRRELEVANT.
2. GREETING -> "Hello, how can I help you today?"
3. FAREWELL -> "Goodbye, let me know if you need anything else."
4. SMALL_TALK -> respond with a short friendly line.
5. DATA_QUERY -> if entity missing or not found, trigger the dynamic limited-data response above. If overall, use default calculation.
6. OUT_OF_SCOPE -> trigger the medical prototype message.
7. CLARIFY & CONTEXT -> remember last mentioned entity or topic.
8. IRRELEVANT -> reply politely: "Sorry,I do not have data for that, I am a medical chatbot prototype with limited data access. Can I help you with that?"

Response style:
- Plain conversational text, no JSON or code in replies.
- Concise (≤5 lines). Friendly and professional.
- If appropriate, append: "Would you like more details?"

DATA_JSON:
{
json.dumps(EXPANDED_DUMMY_DB, indent=2)
}

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
