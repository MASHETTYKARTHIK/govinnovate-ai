"""Centralized UI translations for the Streamlit application."""

from __future__ import annotations

DEFAULT_LANGUAGE = "en"

LANGUAGE_OPTIONS = {
    "en": "English",
    "te": "తెలుగు",
    "hi": "हिन्दी",
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "active_brief": "Active brief",
        "analysis_complete": "Analysis complete",
        "app_title": "GovInnovate AI",
        "average_impact": "Average impact",
        "challenge_define": "Define the challenge",
        "challenge_intake": "CHALLENGE INTAKE",
        "confidence": "Confidence",
        "core_challenges": "Core challenges",
        "created_report": "Created {report_id}",
        "dashboard_description": (
            "Explore local evidence, run transparent mock AI analysis, and produce "
            "decision-ready briefs."
        ),
        "dashboard_eyebrow": "MISSION CONTROL",
        "dashboard_title": "Turn public challenges into pilot-ready action.",
        "dataset": "Dataset",
        "datasets_online": "Datasets online",
        "download_markdown": "Download Markdown report",
        "download_report": "Download Report",
        "estimated_cost": "Estimated cost",
        "evidence_detail": "Evidence detail",
        "evidence_landscape": "Evidence landscape",
        "evidence_map": "Evidence map",
        "evidence_matched": "Evidence matched",
        "evidence_records": "Evidence records",
        "evidence_register": "Preview evidence register",
        "extracted_signals": "Extracted signals",
        "full_report": "Preview full Markdown report",
        "go_upload": "Go to problem upload",
        "impact": "Impact",
        "indicative_budget": "Indicative budget",
        "innovation": "Innovation",
        "language": "Language",
        "local_stack": "Local datasets | Mock AI | SQLite",
        "location": "Location",
        "map_empty": "No mappable evidence is available for this report.",
        "map_loading": "Preparing evidence map...",
        "map_unavailable": "Evidence map is unavailable for the current evidence set.",
        "matched_evidence": "Matched evidence by category",
        "new_analysis": "Start a new analysis",
        "no_reports": "No reports yet. Your first analysis will appear here.",
        "open_analysis": "Open AI analysis",
        "page_analysis": "AI Analysis",
        "page_dashboard": "Dashboard",
        "page_download": "Download Report",
        "page_recommendations": "Recommendations",
        "page_upload": "Upload Problem",
        "pilot_actions": "Pilot actions",
        "policy_recommendations": "Policy recommendations",
        "problem_help": (
            "Describe the challenge, affected communities, current constraints, "
            "and the outcome the government wants to achieve."
        ),
        "problem_short": (
            "Please provide at least 30 characters so the analysis has enough context."
        ),
        "problem_statement": "Problem statement",
        "processing_search": "Searching the local FAISS-style evidence index",
        "processing_score": "Scoring interventions and assembling the report",
        "processing_structure": (
            "Structuring the challenge and extracting decision signals"
        ),
        "processing_title": "GovInnovate AI is building the innovation brief...",
        "public_innovation": "PUBLIC INNOVATION INTELLIGENCE",
        "readiness": "Readiness",
        "recommendations": "Recommendations",
        "recent_analyses": "Recent analyses",
        "reports_generated": "Reports generated",
        "report_center": "REPORT CENTER",
        "report_description": "A portable, auditable artifact for stakeholders.",
        "report_id": "Report ID",
        "report_title": "Export the decision brief.",
        "require_report": "Run an innovation analysis first to unlock this view.",
        "run_analysis": "Run innovation analysis",
        "sector": "Sector",
        "strategic_objectives": "Strategic objectives",
        "target_population": "Target population",
        "target_timeframe": "Target timeframe",
        "timeframe": "Timeframe",
        "upload_description": (
            "The stronger the context, the sharper the evidence matching and "
            "recommendations."
        ),
        "upload_title": "Describe the public problem.",
        "urgency": "Urgency",
        "workflow": "Workflow",
        "workflow_html": (
            '<div class="glass-card">'
            '<b>01. Define</b><p class="muted">Capture local needs, constraints, '
            "budget, and timing.</p>"
            '<b>02. Discover</b><p class="muted">Rank research, cases, startups, '
            "and programs.</p>"
            '<b>03. Decide</b><p class="muted">Compare impact, innovation, cost, '
            "and policy actions.</p>"
            '<b>04. Deliver</b><p class="muted">Download an auditable Markdown '
            "brief.</p></div>"
        ),
        "workspace_description": "Prioritized by local evidence match.",
        "workspace_eyebrow": "DECISION WORKSPACE",
        "workspace_title": "Compare pilot-ready interventions.",
        "reasoning_description": "Every output is derived from local data.",
        "reasoning_eyebrow": "AI REASONING",
        "reasoning_title": "Understand the challenge signals.",
        "unlock_message": "Create an analysis to unlock the full workspace.",
    },
    "te": {
        "app_title": "గోవ్ ఇన్నోవేట్ AI",
        "language": "భాష",
        "page_dashboard": "డాష్‌బోర్డ్",
        "page_upload": "సమస్య అప్లోడ్",
        "page_analysis": "AI విశ్లేషణ",
        "page_recommendations": "సిఫార్సులు",
        "page_download": "రిపోర్ట్ డౌన్‌లోడ్",
        "public_innovation": "ప్రజా ఆవిష్కరణ ఇంటెలిజెన్స్",
        "dashboard_eyebrow": "మిషన్ కంట్రోల్",
        "dashboard_title": "ప్రజా సవాళ్లను పైలట్‌కు సిద్ధమైన చర్యలుగా మార్చండి.",
        "dashboard_description": (
            "స్థానిక ఆధారాలను పరిశీలించండి, పారదర్శక మాక్ AI విశ్లేషణను నడపండి, "
            "నిర్ణయాలకు సిద్ధమైన బ్రీఫ్‌లను తయారు చేయండి."
        ),
        "evidence_records": "ఆధార రికార్డులు",
        "datasets_online": "డేటాసెట్లు ఆన్‌లైన్‌లో",
        "recommendations": "సిఫార్సులు",
        "recent_analyses": "ఇటీవలి విశ్లేషణలు",
        "reports_generated": "సృష్టించిన రిపోర్టులు",
        "average_impact": "సగటు ప్రభావం",
        "evidence_landscape": "ఆధారాల దృశ్యం",
        "workflow": "వర్క్‌ఫ్లో",
        "workflow_html": (
            '<div class="glass-card">'
            '<b>01. నిర్వచించండి</b><p class="muted">స్థానిక అవసరాలు, పరిమితులు, '
            "బడ్జెట్, సమయాన్ని నమోదు చేయండి.</p>"
            '<b>02. కనుగొనండి</b><p class="muted">పరిశోధన, కేసులు, స్టార్టప్‌లు, '
            "కార్యక్రమాలను ర్యాంక్ చేయండి.</p>"
            '<b>03. నిర్ణయించండి</b><p class="muted">ప్రభావం, ఆవిష్కరణ, ఖర్చు, '
            "విధాన చర్యలను పోల్చండి.</p>"
            '<b>04. అందించండి</b><p class="muted">ఆడిట్ చేయదగిన మార్క్‌డౌన్ '
            "బ్రీఫ్‌ను డౌన్‌లోడ్ చేయండి.</p></div>"
        ),
        "new_analysis": "కొత్త విశ్లేషణ ప్రారంభించండి",
        "no_reports": "ఇంకా రిపోర్టులు లేవు. మీ మొదటి విశ్లేషణ ఇక్కడ కనిపిస్తుంది.",
        "challenge_intake": "సవాలు నమోదు",
        "upload_title": "ప్రజా సమస్యను వివరించండి.",
        "upload_description": "సందర్భం బలంగా ఉంటే ఆధారాల సరిపోలిక, సిఫార్సులు మెరుగ్గా ఉంటాయి.",
        "challenge_define": "సవాలును నిర్వచించండి",
        "problem_statement": "సమస్య వివరణ",
        "problem_help": "సవాలు, ప్రభావిత సమూహాలు, పరిమితులు, ఆశించిన ఫలితాన్ని వివరించండి.",
        "location": "ప్రాంతం",
        "sector": "రంగం",
        "target_population": "లక్ష్య జనాభా",
        "indicative_budget": "సూచనాత్మక బడ్జెట్",
        "target_timeframe": "లక్ష్య కాలవ్యవధి",
        "run_analysis": "ఆవిష్కరణ విశ్లేషణ నడపండి",
        "problem_short": "విశ్లేషణకు సరిపడా సందర్భం కోసం కనీసం 30 అక్షరాలు ఇవ్వండి.",
        "processing_title": "గోవ్ ఇన్నోవేట్ AI ఆవిష్కరణ బ్రీఫ్‌ను నిర్మిస్తోంది...",
        "processing_structure": "సవాలును నిర్మాణీకరించి నిర్ణయ సంకేతాలను తీస్తోంది",
        "processing_search": "స్థానిక FAISS-శైలి ఆధార సూచికలో శోధిస్తోంది",
        "processing_score": "జోక్యాలకు స్కోర్లు ఇచ్చి రిపోర్ట్‌ను రూపొందిస్తోంది",
        "analysis_complete": "విశ్లేషణ పూర్తైంది",
        "open_analysis": "AI విశ్లేషణ తెరవండి",
        "reasoning_eyebrow": "AI తర్కం",
        "reasoning_title": "సవాలు సంకేతాలను అర్థం చేసుకోండి.",
        "reasoning_description": "ప్రతి ఫలితం స్థానిక డేటా నుంచే ఉత్పన్నమవుతుంది.",
        "readiness": "సిద్ధత",
        "urgency": "అత్యవసరత",
        "evidence_matched": "సరిపోలిన ఆధారాలు",
        "core_challenges": "ప్రధాన సవాళ్లు",
        "strategic_objectives": "వ్యూహాత్మక లక్ష్యాలు",
        "extracted_signals": "తీసిన సంకేతాలు",
        "evidence_map": "ఆధారాల మ్యాప్",
        "map_loading": "ఆధారాల మ్యాప్ సిద్ధమవుతోంది...",
        "map_empty": "ఈ రిపోర్టుకు మ్యాప్ చేయదగిన ఆధారాలు లేవు.",
        "map_unavailable": "ప్రస్తుత ఆధారాల సమితికి మ్యాప్ అందుబాటులో లేదు.",
        "matched_evidence": "వర్గాల వారీగా సరిపోలిన ఆధారాలు",
        "workspace_eyebrow": "నిర్ణయ కార్యస్థలం",
        "workspace_title": "పైలట్‌కు సిద్ధమైన జోక్యాలను పోల్చండి.",
        "workspace_description": "స్థానిక ఆధారాల సరిపోలిక ఆధారంగా ప్రాధాన్యం ఇవ్వబడింది.",
        "confidence": "నమ్మకం",
        "estimated_cost": "అంచనా వ్యయం",
        "timeframe": "కాలవ్యవధి",
        "pilot_actions": "పైలట్ చర్యలు",
        "policy_recommendations": "విధాన సిఫార్సులు",
        "report_center": "రిపోర్ట్ సెంటర్",
        "report_title": "నిర్ణయ బ్రీఫ్‌ను ఎగుమతి చేయండి.",
        "report_description": "భాగస్వాముల కోసం తీసుకెళ్లగల, ఆడిట్ చేయదగిన పత్రం.",
        "report_id": "రిపోర్ట్ ID",
        "dataset": "డేటాసెట్",
        "download_markdown": "మార్క్‌డౌన్ రిపోర్ట్ డౌన్‌లోడ్",
        "evidence_register": "ఆధారాల రిజిస్టర్ ప్రివ్యూ",
        "full_report": "పూర్తి మార్క్‌డౌన్ రిపోర్ట్ ప్రివ్యూ",
        "require_report": "ఈ వీక్షణను తెరవడానికి ముందుగా ఆవిష్కరణ విశ్లేషణ నడపండి.",
        "go_upload": "సమస్య అప్లోడ్‌కు వెళ్ళండి",
        "active_brief": "సక్రియ బ్రీఫ్",
        "unlock_message": "పూర్తి వర్క్‌స్పేస్ కోసం విశ్లేషణను సృష్టించండి.",
        "local_stack": "స్థానిక డేటాసెట్లు | మాక్ AI | SQLite",
    },
    "hi": {
        "app_title": "गवइनोवेट AI",
        "language": "भाषा",
        "page_dashboard": "डैशबोर्ड",
        "page_upload": "समस्या अपलोड",
        "page_analysis": "AI विश्लेषण",
        "page_recommendations": "सिफारिशें",
        "page_download": "रिपोर्ट डाउनलोड",
        "public_innovation": "लोक नवाचार इंटेलिजेंस",
        "dashboard_eyebrow": "मिशन कंट्रोल",
        "dashboard_title": "लोक समस्याओं को पायलट-तैयार कार्रवाई में बदलें.",
        "dashboard_description": (
            "स्थानीय प्रमाण देखें, पारदर्शी मॉक AI विश्लेषण चलाएं, और निर्णय-तैयार "
            "ब्रीफ बनाएं."
        ),
        "evidence_records": "प्रमाण रिकॉर्ड",
        "datasets_online": "डेटासेट ऑनलाइन",
        "recommendations": "सिफारिशें",
        "recent_analyses": "हाल के विश्लेषण",
        "reports_generated": "बनी रिपोर्टें",
        "average_impact": "औसत प्रभाव",
        "evidence_landscape": "प्रमाण परिदृश्य",
        "workflow": "वर्कफ़्लो",
        "workflow_html": (
            '<div class="glass-card">'
            '<b>01. परिभाषित करें</b><p class="muted">स्थानीय जरूरतें, सीमाएं, '
            "बजट, और समय दर्ज करें.</p>"
            '<b>02. खोजें</b><p class="muted">शोध, केस, स्टार्टअप, और कार्यक्रमों '
            "को रैंक करें.</p>"
            '<b>03. निर्णय लें</b><p class="muted">प्रभाव, नवाचार, लागत, और नीति '
            "कार्रवाइयों की तुलना करें.</p>"
            '<b>04. वितरित करें</b><p class="muted">ऑडिट योग्य मार्कडाउन ब्रीफ '
            "डाउनलोड करें.</p></div>"
        ),
        "new_analysis": "नया विश्लेषण शुरू करें",
        "no_reports": "अभी कोई रिपोर्ट नहीं है. आपका पहला विश्लेषण यहां दिखेगा.",
        "challenge_intake": "समस्या इनटेक",
        "upload_title": "लोक समस्या का वर्णन करें.",
        "upload_description": "संदर्भ जितना मजबूत होगा, प्रमाण मिलान और सिफारिशें उतनी बेहतर होंगी.",
        "challenge_define": "समस्या परिभाषित करें",
        "problem_statement": "समस्या विवरण",
        "problem_help": "समस्या, प्रभावित समुदाय, सीमाएं, और इच्छित परिणाम बताएं.",
        "location": "स्थान",
        "sector": "क्षेत्र",
        "target_population": "लक्षित आबादी",
        "indicative_budget": "अनुमानित बजट",
        "target_timeframe": "लक्षित समयसीमा",
        "run_analysis": "नवाचार विश्लेषण चलाएं",
        "problem_short": "विश्लेषण के लिए पर्याप्त संदर्भ देने हेतु कम से कम 30 अक्षर दर्ज करें.",
        "processing_title": "गवइनोवेट AI नवाचार ब्रीफ बना रहा है...",
        "processing_structure": "समस्या को संरचित कर निर्णय संकेत निकाले जा रहे हैं",
        "processing_search": "स्थानीय FAISS-शैली प्रमाण सूचकांक में खोज हो रही है",
        "processing_score": "हस्तक्षेपों को स्कोर कर रिपोर्ट तैयार की जा रही है",
        "analysis_complete": "विश्लेषण पूरा हुआ",
        "open_analysis": "AI विश्लेषण खोलें",
        "reasoning_eyebrow": "AI तर्क",
        "reasoning_title": "समस्या संकेतों को समझें.",
        "reasoning_description": "हर आउटपुट स्थानीय डेटा से निकाला गया है.",
        "readiness": "तैयारी",
        "urgency": "तात्कालिकता",
        "evidence_matched": "मिले प्रमाण",
        "core_challenges": "मुख्य चुनौतियां",
        "strategic_objectives": "रणनीतिक उद्देश्य",
        "extracted_signals": "निकाले गए संकेत",
        "evidence_map": "प्रमाण मानचित्र",
        "map_loading": "प्रमाण मानचित्र तैयार हो रहा है...",
        "map_empty": "इस रिपोर्ट के लिए मानचित्र योग्य प्रमाण उपलब्ध नहीं है.",
        "map_unavailable": "वर्तमान प्रमाण सेट के लिए मानचित्र उपलब्ध नहीं है.",
        "matched_evidence": "श्रेणी के अनुसार मिले प्रमाण",
        "workspace_eyebrow": "निर्णय कार्यक्षेत्र",
        "workspace_title": "पायलट-तैयार हस्तक्षेपों की तुलना करें.",
        "workspace_description": "स्थानीय प्रमाण मिलान के आधार पर प्राथमिकता दी गई.",
        "confidence": "विश्वास",
        "estimated_cost": "अनुमानित लागत",
        "timeframe": "समयसीमा",
        "pilot_actions": "पायलट कार्रवाइयां",
        "policy_recommendations": "नीति सिफारिशें",
        "report_center": "रिपोर्ट केंद्र",
        "report_title": "निर्णय ब्रीफ निर्यात करें.",
        "report_description": "हितधारकों के लिए पोर्टेबल, ऑडिट योग्य दस्तावेज.",
        "report_id": "रिपोर्ट ID",
        "dataset": "डेटासेट",
        "download_markdown": "मार्कडाउन रिपोर्ट डाउनलोड करें",
        "evidence_register": "प्रमाण रजिस्टर पूर्वावलोकन",
        "full_report": "पूरी मार्कडाउन रिपोर्ट पूर्वावलोकन",
        "require_report": "यह दृश्य खोलने के लिए पहले नवाचार विश्लेषण चलाएं.",
        "go_upload": "समस्या अपलोड पर जाएं",
        "active_brief": "सक्रिय ब्रीफ",
        "unlock_message": "पूरा कार्यक्षेत्र खोलने के लिए विश्लेषण बनाएं.",
        "local_stack": "स्थानीय डेटासेट | मॉक AI | SQLite",
    },
}


def t(key: str, language: str = DEFAULT_LANGUAGE) -> str:
    """Return a translated string, falling back to English and then the key."""
    return TRANSLATIONS.get(language, {}).get(
        key, TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key)
    )
