import os
import fitz
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, KeepTogether, Image, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# ---------------------------------------------------------
# Numbered Canvas for Page X of Y Header/Footer
# ---------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(HexColor("#1a1a2e"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 805, "SIH SMART AUTOMATION: UNIVERSAL TECH STACK & PREDICTIONS REPORT")
            self.setStrokeColor(HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, 798, 559, 798)
            
        # Footer (all pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(HexColor("#64748b"))
        self.setStrokeColor(HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 40, 559, 40)
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 28, page_str)
        self.drawString(36, 28, "Confidential | Smart India Hackathon Strategic Technical Report")
        self.restoreState()

# ---------------------------------------------------------
# PDF Document Generator
# ---------------------------------------------------------
def create_report_pdf():
    pdf_filename = r"d:\Testing\Research\SIH_Smart_Automation_Analysis_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=48,
        bottomMargin=48
    )

    # Styles
    styles = getSampleStyleSheet()
    
    # Custom Palette
    COLOR_PRIMARY = HexColor("#1a1a2e")
    COLOR_ACCENT = HexColor("#0f3460")
    COLOR_TEAL = HexColor("#16213e")
    COLOR_BLUE = HexColor("#0284c7")
    COLOR_LIGHT_BG = HexColor("#f8fafc")
    COLOR_BORDER = HexColor("#cbd5e1")
    COLOR_TEXT = HexColor("#1e293b")
    COLOR_MUTED = HexColor("#475569")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=COLOR_PRIMARY,
        alignment=TA_CENTER,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=COLOR_MUTED,
        alignment=TA_CENTER,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=COLOR_ACCENT,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=COLOR_PRIMARY,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=COLOR_TEXT,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=body_style,
        alignment=TA_LEFT,
        leftIndent=10,
        firstLineIndent=-6,
        spaceAfter=3
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=COLOR_TEXT
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )

    story = []

    # ---------------------------------------------------------
    # COVER / HEADER TITLE BLOCK
    # ---------------------------------------------------------
    story.append(Paragraph("SIH SMART AUTOMATION THEME", ParagraphStyle('SubHeader', fontName='Helvetica-Bold', fontSize=9, textColor=COLOR_BLUE, alignment=TA_CENTER, spaceAfter=2)))
    story.append(Paragraph("Comprehensive Technical Analysis, Universal Stack & 2026 Predictions Report", title_style))
    story.append(Paragraph("A Complete Guide for Hackathon Participants, Solution Architects, and Developers", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=COLOR_ACCENT, spaceAfter=8))

    # Executive Summary Box
    summary_html = "<b>EXECUTIVE SUMMARY:</b> This report provides a deep-dive technical analysis of 103 official Smart India Hackathon (SIH) problem statements under the <b>Smart Automation</b> theme across 2023, 2024, and 2025/2026. It establishes a <b>Universal Tech Stack Framework</b> (a standardized architecture that satisfies over 90% of hackathon automation challenges) and presents <b>12 realistic, predicted problem statements</b> for SIH 2026 complete with recommended production and buzzword tech stacks."
    summary_p = Paragraph(summary_html, ParagraphStyle('ExecSummary', parent=body_style, fontSize=8, leading=11, textColor=HexColor("#1e293b")))
    
    summary_table = Table([[summary_p]], colWidths=[523])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#f0f9ff")),
        ('BOX', (0,0), (-1,-1), 1, HexColor("#0284c7")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # SECTION 1: SOURCE DATA ANALYSIS & TRENDS
    # ---------------------------------------------------------
    story.append(Paragraph("1. Source Dataset Analysis & Domain Trends", h1_style))
    story.append(Paragraph("Analysis of the 103 extracted official problem statements reveals distinct technological preferences and domain focuses across Indian Ministries and State Governments:", body_style))

    # Bullet points
    story.append(Paragraph("• <b>Category Dominance</b>: Software-only projects constitute <b>74.8%</b> (77 statements) of all problem statements, focusing on web platforms, AI/ML models, and mobile apps. Pure Hardware comprises <b>20.4%</b> (21 statements), while Hardware+Software (Cyber-Physical IIoT) accounts for <b>4.8%</b> (5 statements).", bullet_style))
    story.append(Paragraph("• <b>Top Sponsoring Bodies</b>: The <i>Ministry of Jal Shakti</i> (Water Resources) leads with 15 problem statements, followed closely by <i>State Governments</i> (14 statements), <i>National Technical Research Organisation (NTRO)</i> (12 statements), <i>Ministry of Coal</i> (10 statements), and <i>ISRO</i> (8 statements).", bullet_style))
    story.append(Paragraph("• <b>Core Tech Drivers</b>: Python and React.js remain the undeniable standard, appearing in nearly every software stack requirement. PostgreSQL dominates database choices, while FastAPI has overtaken Flask/Django as the preferred REST API engine for AI pipelines.", bullet_style))
    story.append(Spacer(1, 6))

    # Diagrams 2 & 3 side by side
    img_cat = Image(r"d:\Testing\Research\diagrams\category_split.png", width=3.2*inch, height=2.1*inch)
    img_min = Image(r"d:\Testing\Research\diagrams\ministry_dist.png", width=3.8*inch, height=2.1*inch)
    
    diag_table = Table([[img_cat, img_min]], colWidths=[245, 278])
    diag_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(diag_table)
    story.append(Spacer(1, 6))

    # Tech frequency chart
    img_freq = Image(r"d:\Testing\Research\diagrams\tech_frequency.png", width=7.0*inch, height=2.7*inch)
    story.append(img_freq)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 2: THE UNIVERSAL TECH STACK FRAMEWORK
    # ---------------------------------------------------------
    story.append(Paragraph("2. The Universal Tech Stack Framework", h1_style))
    story.append(Paragraph("In hackathons, 80% of project requirements across diverse problem statements share the exact same architectural foundation. A <b>Universal Tech Stack</b> allows team members to master a core set of reliable tools while plugging in specialized modules (AI/ML, GIS, IoT, AR/VR) depending on the specific problem statement.", body_style))
    story.append(Spacer(1, 4))

    # Architecture Image
    img_arch = Image(r"d:\Testing\Research\diagrams\tech_stack_arch.png", width=7.1*inch, height=3.0*inch)
    story.append(img_arch)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Core Universal Stack Components (The Standard 80%)", h2_style))
    
    # Core Stack Table
    core_data = [
        [Paragraph("Layer", table_header), Paragraph("Technology Choice", table_header), Paragraph("Why It Is Universal & When To Use", table_header)],
        [Paragraph("Frontend (Web)", table_cell_bold), Paragraph("React.js / Next.js + TailwindCSS", table_cell), Paragraph("Fastest UI prototyping, rich component ecosystem, seamless integration with maps, charts, and real-time WebSockets.", table_cell)],
        [Paragraph("Frontend (Mobile)", table_cell_bold), Paragraph("Flutter or React Native", table_cell), Paragraph("Build once, deploy on Android & iOS. Mandatory for field-agent apps, offline mobile collection, and PWA requirements.", table_cell)],
        [Paragraph("Backend API Engine", table_cell_bold), Paragraph("Python FastAPI (or Django REST)", table_cell), Paragraph("Python is the native language of AI/ML. FastAPI delivers high performance (async/await), automatic OpenAPI docs, and easy integration with OpenCV, PyTorch, and LangChain.", table_cell)],
        [Paragraph("Database & Cache", table_cell_bold), Paragraph("PostgreSQL + Redis", table_cell), Paragraph("PostgreSQL handles relational data, spatial geospatial queries (via PostGIS), and time-series data. Redis acts as in-memory cache and async queue engine.", table_cell)],
        [Paragraph("Document Storage", table_cell_bold), Paragraph("MinIO / AWS S3", table_cell), Paragraph("Standard object storage for PDFs, inspection images, video clips, and model weight checkpoints.", table_cell)],
        [Paragraph("DevOps & Containers", table_cell_bold), Paragraph("Docker + Nginx + GitHub Actions", table_cell), Paragraph("Ensures zero deployment surprises during live judging. Single 'docker-compose up' command launches the full application stack.", table_cell)]
    ]
    t_core = Table(core_data, colWidths=[95, 145, 283])
    t_core.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_LIGHT_BG])
    ]))
    story.append(t_core)
    story.append(Spacer(1, 10))

    # Domain Extensions Table
    story.append(Paragraph("Specialized Domain Modular Extensions (The 20% Plugins)", h2_style))
    
    mod_data = [
        [Paragraph("Domain Module", table_header), Paragraph("Key Tools & Libraries", table_header), Paragraph("Hackathon Application Context", table_header)],
        [Paragraph("AI / LLM & RAG Engine", table_cell_bold), Paragraph("LangChain, Ollama (Llama 3), ChromaDB, Bhashini API", table_cell), Paragraph("Chatbots, legal document processing, policy virtual assistants, Indic multilingual support for 13+ regional languages.", table_cell)],
        [Paragraph("Computer Vision Edge", table_cell_bold), Paragraph("OpenCV, YOLOv8/v9, PyTorch, Tesseract OCR", table_cell), Paragraph("Crowd monitoring, vehicle counting, document scanning, defect detection, and marine organism identification.", table_cell)],
        [Paragraph("IoT Hardware Automation", table_cell_bold), Paragraph("ESP32, STM32, Raspberry Pi, MQTT (Mosquitto), C++", table_cell), Paragraph("Smart track monitoring, water quality sensors, automated MCB testing, electric fence tampering detection.", table_cell)],
        [Paragraph("GIS & Remote Sensing", table_cell_bold), Paragraph("PostGIS, Leaflet.js, Mapbox GL, ISRO Bhuvan API", table_cell), Paragraph("Rooftop rainwater harvesting potential, groundwater level tracking, navigation route rationalization.", table_cell)],
        [Paragraph("Digital Twin & AR/VR", table_cell_bold), Paragraph("Three.js, Unity, ARCore, Autodesk Fusion 360", table_cell), Paragraph("Live digital twin of power plants, CAD model generative design, AR visualization for rural house construction.", table_cell)]
    ]
    t_mod = Table(mod_data, colWidths=[110, 150, 263])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_ACCENT),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_LIGHT_BG])
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 10))

    # Workflow Diagram
    story.append(Paragraph("End-to-End System Dataflow Workflow", h2_style))
    img_wf = Image(r"d:\Testing\Research\diagrams\system_workflow.png", width=7.1*inch, height=2.2*inch)
    story.append(img_wf)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 3: JUDGES' WINNING BUZZWORDS & NEXT-GEN TECH
    # ---------------------------------------------------------
    story.append(Paragraph("3. Judges' 'Winning Buzzwords' & Advanced Tech Stack", h1_style))
    story.append(Paragraph("In competitive hackathons like SIH, standard implementations earn passing marks, but implementing <b>Advanced Next-Gen Tech ('Buzzwords')</b> creates the 'WOW factor' that secures top podium finishes.", body_style))
    story.append(Spacer(1, 4))

    buzz_data = [
        [Paragraph("Buzzword / Concept", table_header), Paragraph("What It Means", table_header), Paragraph("How To Demonstrate to Judges", table_header)],
        [Paragraph("Agentic RAG & Multi-Agent", table_cell_bold), Paragraph("Autonomous AI agents with tool-calling capabilities that break complex queries into multi-step actions.", table_cell), Paragraph("Show chatbot executing database lookups, generating PDF reports, and triggering SMS alerts automatically.", table_cell)],
        [Paragraph("Explainable AI (XAI)", table_cell_bold), Paragraph("Providing human-interpretable reasons behind AI predictions (e.g., using SHAP or LIME values).", table_cell), Paragraph("Display a visual breakdown of feature importance explaining *why* an intern candidate was matched or a loan was flagged.", table_cell)],
        [Paragraph("Edge AI & TinyML", table_cell_bold), Paragraph("Running ML inference directly on microcontrollers or edge chips without internet access.", table_cell), Paragraph("Demonstrate YOLO object detection running locally on Raspberry Pi / ESP32-CAM with zero cloud latency.", table_cell)],
        [Paragraph("Live Digital Twin", table_cell_bold), Paragraph("A real-time 3D/virtual replica of physical assets updated dynamically via IoT sensor feeds.", table_cell), Paragraph("Display a 3D model (Three.js/Unity) of a machine or track that updates color/orientation in sync with physical sensors.", table_cell)],
        [Paragraph("Blockchain Audit Trail", table_cell_bold), Paragraph("Tamper-proof, immutable ledger for logs, certificates, and compliance records.", table_cell), Paragraph("Show generated certificate cryptographic hash verification page on an immutable local ledger (Hyperledger/Solidity).", table_cell)],
        [Paragraph("Federated Learning", table_cell_bold), Paragraph("Privacy-preserving AI training across distributed edge nodes without sharing raw data.", table_cell), Paragraph("Explain how sensitive hospital or metro rail logs remain local while aggregating global AI weights.", table_cell)]
    ]
    t_buzz = Table(buzz_data, colWidths=[115, 180, 228])
    t_buzz.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor("#854d0e")),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, HexColor("#fefce8")])
    ]))
    story.append(t_buzz)
    story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # SECTION 4: PREDICTED PROBLEM STATEMENTS FOR SIH 2026
    # ---------------------------------------------------------
    story.append(Paragraph("4. SIH 2026 Problem Statement Predictions & Tech Stacks", h1_style))
    story.append(Paragraph("Based on national initiatives (Viksit Bharat 2047, Digital India, PM Gati Shakti, Bhashini AI Mission) and domain analysis from past editions, here are <b>12 realistic predicted problem statements</b> for SIH 2026 along with their winning tech stacks:", body_style))
    story.append(Spacer(1, 6))

    predictions = [
        {
            "num": "PS 1",
            "title": "AI-Driven Automated Underground Water Pipeline Leak & Contamination Detection",
            "org": "Ministry of Jal Shakti",
            "cat": "Hardware + Software",
            "desc": "Develop a cyber-physical system using acoustic vibration sensors, pressure transducers, and satellite thermal GIS data to detect hidden underground pipe leaks and water contamination in real-time.",
            "std": "Hardware: ESP32, Hydrophone/Acoustic sensors, pressure sensors | Backend: Python FastAPI, PostgreSQL+PostGIS | Mobile: Flutter app with Leaflet.js map.",
            "buzz": "Edge AI acoustic anomaly fingerprinting, Satellite Synthetic Aperture Radar (SAR) leak detection, Digital Twin hydraulic pressure simulation."
        },
        {
            "num": "PS 2",
            "title": "Edge-AI Powered Overhead Equipment (OHE) Catenary Line Defect Inspection System",
            "org": "Ministry of Railways",
            "cat": "Hardware + Software",
            "desc": "Real-time automated vision system mounted on locomotive rooftops to detect sparkings, physical catenary wear, and pantograph contact anomalies while operating at high speeds.",
            "std": "Hardware: NVIDIA Jetson Orin Nano, Industrial High-speed Global Shutter Camera | AI: YOLOv8 / TensorRT | Dashboard: React.js, WebSockets, Grafana.",
            "buzz": "5G-NR ultra-low latency alerts, Vision Transformer (ViT) spark detection, Edge TPU acceleration, Automated track deficit logging."
        },
        {
            "num": "PS 3",
            "title": "Deepfake Video & Synthetic Audio Detection Engine for Public Redressal Portals",
            "org": "MeitY / National Cyber Security",
            "cat": "Software",
            "desc": "Build an automated verification service that inspects user-submitted video/audio evidence in cybercrime and citizen complaint portals for AI manipulation, face swapping, and voice cloning.",
            "std": "Frontend: React.js, Next.js | Backend: Python FastAPI, PyTorch | Models: MesoNet, EfficientNet, Wav2Vec2 | DB: PostgreSQL, Redis.",
            "buzz": "Explainable Deepfake Heatmap (SHAP/Grad-CAM), Cryptographic Authenticity C2PA Stamp Verification, Multimodal Anti-Spoofing Architecture."
        },
        {
            "num": "PS 4",
            "title": "AI-Personalized Multilingual Adaptive Remedial Learning Engine Aligned with NEP 2020",
            "org": "Ministry of Education / AICTE",
            "cat": "Software",
            "desc": "An adaptive web platform for rural school students that assesses individual learning gaps and generates dynamic, voice-enabled remedial lessons in 13+ Indian languages.",
            "std": "Frontend: React.js PWA | Backend: Python Django | AI: HuggingFace Transformers, Bhashini API (Voice Translation) | DB: PostgreSQL.",
            "buzz": "Knowledge Tracing Graph (KTG), Reinforcement Learning for path recommendation, Indic-LLM voice tutoring assistant, Offline PWA Sync."
        },
        {
            "num": "PS 5",
            "title": "Autonomous Portable IIoT Soil Health & Crop Disease Analyzer with Voice Advisory",
            "org": "Ministry of Agriculture",
            "cat": "Hardware + Software",
            "desc": "A handheld sensor kit + smartphone app that measures NPK soil levels, moisture, and crop leaf disease using on-device camera ML, providing localized audio advisory.",
            "std": "Hardware: ESP32, NPK Soil Optical Sensor | Mobile: React Native / Flutter | CV: OpenCV, MobileNetV3 | Advisory: Bhashini TTS Engine.",
            "buzz": "TinyML soil spectral analysis, Offline leaf disease diagnosis via ONNX Micro, Solar-powered IoT edge node."
        },
        {
            "num": "PS 6",
            "title": "AI-Assisted Automated Cold-Chain & Vaccine Inventory Tracker for Rural Health Centres",
            "org": "Ministry of Health & Family Welfare",
            "cat": "Hardware + Software",
            "desc": "Real-time IoT temperature logging and predictive inventory management system to eliminate vaccine wastage in remote Primary Health Centres (PHCs).",
            "std": "Hardware: STM32 / ESP32, DS18B20 Temp sensors, GSM/4G SIM7600 module | Backend: FastAPI, PostgreSQL | Web: React.js, Chart.js.",
            "buzz": "LSTM temperature breach prediction 6 hours in advance, Blockchain-based vaccine batch provenance, Low-power NB-IoT protocol."
        },
        {
            "num": "PS 7",
            "title": "Real-time Microgrid Load Forecasting & Renewable Energy Dispatch Optimizer",
            "org": "Ministry of Power",
            "cat": "Software",
            "desc": "An AI system for regional electricity discoms to project peak power demand 24 hours ahead and automatically balance solar/wind grid integration.",
            "std": "Frontend: React.js, D3.js | Backend: Python FastAPI | ML: XGBoost, Prophet, PyTorch LSTM | DB: TimescaleDB, Redis.",
            "buzz": "Physics-Informed Neural Networks (PINN), Autonomous Smart Contract Energy Trading, Live Digital Twin Grid Simulation."
        },
        {
            "num": "PS 8",
            "title": "Computer Vision-Based Automated Pothole, Garbage & Infrastructure Monitoring System",
            "org": "Ministry of Housing & Urban Affairs",
            "cat": "Software",
            "desc": "Utilize dashcam feeds from public buses and municipal sanitation vehicles to automatically log street defects, potholes, and open garbage dumps on a GIS map.",
            "std": "CV: YOLOv8 object detection, OpenCV | Backend: Python FastAPI | GIS: PostGIS, Mapbox GL JS | Frontend: React.js dashboard.",
            "buzz": "3D LiDAR Point-Cloud Pothole Depth Estimation, Automated Municipal Work-Order Ticket Dispatching Agent, GeoAI Heatmaps."
        },
        {
            "num": "PS 9",
            "title": "Autonomous Underground Gas Leakage & Slope Instability Warning System for Coal Mines",
            "org": "Ministry of Coal & Mines",
            "cat": "Hardware + Software",
            "desc": "A ruggedized Wireless Sensor Network (WSN) that continuously monitors methane ($CH_4$), carbon monoxide ($CO$), and rock slope displacement in underground coal mines.",
            "std": "Hardware: STM32, MQ-4 Methane Sensor, MQ-7 CO Sensor, Tiltmeter | Wireless: LoRaWAN | Backend: Python, PostgreSQL | Web: React.js.",
            "buzz": "LoRa Mesh subterranean topology, AI gas dispersion modeling, IIoT automated ventilation damper control, Digital Twin Mine Model."
        },
        {
            "num": "PS 10",
            "title": "Offline Edge-AI Drone Tracking & Perimeter Intrusion Early Warning System",
            "org": "Ministry of Defense / MHA",
            "cat": "Hardware + Software",
            "desc": "Deploy low-cost thermal camera arrays and acoustic microphone arrays at remote perimeter posts to detect unauthorized drone incursions without cloud connectivity.",
            "std": "Hardware: Raspberry Pi 5 / NVIDIA Jetson Nano, Acoustic Microphone Array, Thermal Camera | ML: YOLOv8-Nano, Librosa | GUI: PyQt5.",
            "buzz": "Sensor Fusion (Acoustic + Thermal RF), Radar Doppler FFT Signature Classification, Anti-Swarm Autonomous RF Countermeasure Trigger."
        },
        {
            "num": "PS 11",
            "title": "AI-Driven Shell Company & Tax Evasion Detection Graph Neural Network",
            "org": "Ministry of Corporate Affairs",
            "cat": "Software",
            "desc": "Analyze vast corporate registry filings, directorship patterns, and transaction logs to automatically uncover circular trading and shell company networks.",
            "std": "Backend: Python FastAPI | Graph Database: Neo4j | Graph ML: PyTorch Geometric (PyG), NetworkX | Frontend: React.js, Cytoscape.js.",
            "buzz": "Graph Neural Networks (GNN - GraphSAGE), Automated Beneficial Ownership Disambiguation, Explainable Fraud Path Visualization."
        },
        {
            "num": "PS 12",
            "title": "Driver Fatigue, Distraction & Lane Departure Warning System with Fleet IIoT Telematics",
            "org": "Ministry of Road Transport (MoRTH)",
            "cat": "Hardware + Software",
            "desc": "In-cabin driver monitoring camera paired with vehicle OBD-II telematics to alert sleepy drivers and log unsafe driving behavior to fleet central operations.",
            "std": "Hardware: Raspberry Pi 4, IR Camera Module, CAN-Bus OBD-II reader | CV: MediaPipe Face Mesh, OpenCV | Server: Node.js, PostgreSQL.",
            "buzz": "Eye Aspect Ratio (EAR) & Yawn Frequency Edge Inference, Driver Risk Scoring Engine, Live Telematics Geo-Fencing."
        }
    ]

    for p in predictions:
        p_table_data = [
            [Paragraph(f"<b>{p['num']}: {p['title']}</b>", table_header), Paragraph(f"<b>Org:</b> {p['org']} | <b>Cat:</b> {p['cat']}", ParagraphStyle('HeadRight', parent=table_header, alignment=TA_RIGHT))],
            [Paragraph(f"<b>Problem Summary:</b> {p['desc']}", table_cell), Paragraph("", table_cell)],
            [Paragraph(f"<b>Standard Tech Stack:</b> {p['std']}", table_cell), Paragraph("", table_cell)],
            [Paragraph(f"<b>Judges' Winning Buzzword Stack:</b> {p['buzz']}", ParagraphStyle('BuzzCell', parent=table_cell, textColor=HexColor("#854d0e"))), Paragraph("", table_cell)]
        ]
        
        t_p = Table(p_table_data, colWidths=[370, 153])
        t_p.setStyle(TableStyle([
            ('SPAN', (0,0), (0,0)),
            ('SPAN', (0,1), (1,1)),
            ('SPAN', (0,2), (1,2)),
            ('SPAN', (0,3), (1,3)),
            ('BACKGROUND', (0,0), (-1,0), COLOR_ACCENT),
            ('BACKGROUND', (0,1), (-1,1), COLOR_LIGHT_BG),
            ('BACKGROUND', (0,3), (-1,3), HexColor("#fefce8")),
            ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        
        story.append(KeepTogether([t_p, Spacer(1, 6)]))

    # ---------------------------------------------------------
    # SECTION 5: HACKATHON WINNING STRATEGY
    # ---------------------------------------------------------
    story.append(Spacer(1, 8))
    story.append(Paragraph("5. Practical Action Plan for Hackathon Teams", h1_style))
    story.append(Paragraph("To maximize your evaluation scores during the Smart India Hackathon, follow this proven execution checklist:", body_style))
    
    story.append(Paragraph("1. <b>Pre-Build the Universal Foundation</b>: Do not waste hackathon time writing basic user login, Docker scripts, or database setups. Keep a ready boilerplate repo containing React + FastAPI + PostgreSQL + Docker Compose.", bullet_style))
    story.append(Paragraph("2. <b>Implement 'The 3-Click Demo'</b>: Ensure judges can experience your core innovation within 30 seconds of starting your demo without complex registration steps.", bullet_style))
    story.append(Paragraph("3. <b>Highlight Edge Hardware & Offline Mode</b>: If doing a hardware/IIoT project, demonstrate that your solution works reliably even when Wi-Fi is disabled.", bullet_style))
    story.append(Paragraph("4. <b>Integrate Bhashini Multilingual Support</b>: Adding Hindi and regional language voice support instantly elevates any citizen service app in official SIH evaluation rubrics.", bullet_style))
    story.append(Paragraph("5. <b>Show Explainability & Analytics</b>: Include a clean admin dashboard featuring live charts (Chart.js / D3.js) and XAI feature breakdown for judges.", bullet_style))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {pdf_filename}")

if __name__ == "__main__":
    create_report_pdf()
