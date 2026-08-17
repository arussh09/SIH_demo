"""
SIH Smart Automation Problem Statements - Tech Stack Analysis PDF Generator
============================================================================
Generates a professional PDF with all problem statements, their original info,
and deeply researched tech stacks (standard + buzzword sections).
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, KeepTogether
)
from reportlab.lib.colors import HexColor
import os

# ============================================================================
# COLOR PALETTE
# ============================================================================
DARK_HEADER = HexColor("#1a1a2e")
ACCENT_BLUE = HexColor("#0f3460")
ACCENT_TEAL = HexColor("#16213e")
ROW_ALT_1 = HexColor("#f8f9fa")
ROW_ALT_2 = HexColor("#ffffff")
HEADER_TEXT = colors.white
BORDER_COLOR = HexColor("#dee2e6")
SECTION_BG = HexColor("#e8f4f8")
BUZZWORD_BG = HexColor("#fff3cd")
YEAR_HEADER_BG = HexColor("#0d6efd")

# ============================================================================
# STYLES
# ============================================================================
styles = getSampleStyleSheet()

cell_style = ParagraphStyle(
    'CellStyle',
    parent=styles['Normal'],
    fontSize=6.5,
    leading=8,
    spaceBefore=1,
    spaceAfter=1,
)

cell_style_bold = ParagraphStyle(
    'CellStyleBold',
    parent=cell_style,
    fontName='Helvetica-Bold',
    fontSize=6.5,
    leading=8,
)

header_style = ParagraphStyle(
    'HeaderStyle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=7,
    leading=9,
    textColor=colors.white,
    alignment=TA_CENTER,
)

tech_style = ParagraphStyle(
    'TechStyle',
    parent=styles['Normal'],
    fontSize=5.8,
    leading=7.2,
    spaceBefore=0,
    spaceAfter=0,
)

tech_bold = ParagraphStyle(
    'TechBold',
    parent=tech_style,
    fontName='Helvetica-Bold',
    fontSize=6,
    leading=7.5,
)

buzzword_style = ParagraphStyle(
    'BuzzwordStyle',
    parent=styles['Normal'],
    fontSize=5.5,
    leading=7,
    textColor=HexColor("#856404"),
)

title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Title'],
    fontSize=18,
    leading=22,
    textColor=DARK_HEADER,
    alignment=TA_CENTER,
    spaceAfter=6,
)

subtitle_style = ParagraphStyle(
    'SubtitleStyle',
    parent=styles['Normal'],
    fontSize=10,
    leading=14,
    textColor=HexColor("#495057"),
    alignment=TA_CENTER,
    spaceAfter=12,
)

year_title_style = ParagraphStyle(
    'YearTitleStyle',
    parent=styles['Heading2'],
    fontSize=13,
    leading=16,
    textColor=ACCENT_BLUE,
    spaceBefore=10,
    spaceAfter=6,
)


# ============================================================================
# ALL PROBLEM STATEMENTS WITH DEEP TECH STACK ANALYSIS
# ============================================================================

problem_statements = [
    # ========================================================================
    # SIH 2025 / 2026 (12 Statements)
    # ========================================================================
    {
        "year": "SIH 2025 / 2026",
        "ps_no": "SIH25020",
        "org": "Ministry of Railways",
        "category": "Hardware",
        "description": "Development of indigenous contactless Integrated Track Monitoring Systems (ITMS) for Track Recording on Indian Railways",
        "tech_stack": (
            "<b>Hardware:</b> STM32/ESP32 MCU, IMU sensors (MPU6050/ADXL345), LVDT displacement sensors, "
            "laser profilometers, ultrasonic flaw detectors (UT probes), vibration/accelerometer sensors, "
            "GPS module (NEO-6M/u-blox), LoRa/4G communication module, LiPo battery + solar charging circuit, "
            "custom PCB (KiCad/Altium), ruggedized IP67 enclosure<br/>"
            "<b>Edge Computing:</b> Raspberry Pi 4/5 or NVIDIA Jetson Nano for on-device ML inference<br/>"
            "<b>Firmware:</b> C/C++ (FreeRTOS or bare-metal), Arduino framework for prototyping<br/>"
            "<b>Signal Processing:</b> Python (NumPy, SciPy) for offline calibration; DSP libraries on MCU<br/>"
            "<b>ML/AI:</b> TensorFlow Lite / TinyML for anomaly detection on edge; scikit-learn for model training<br/>"
            "<b>Backend:</b> Python (FastAPI/Flask), PostgreSQL + TimescaleDB for time-series data<br/>"
            "<b>Dashboard:</b> React.js, Chart.js/D3.js, Leaflet.js for geo-mapping track defects<br/>"
            "<b>Communication:</b> MQTT protocol, LoRaWAN gateway, GSM/4G fallback<br/>"
            "<b>DevOps:</b> Docker, GitHub Actions CI/CD"
        ),
        "buzzword": (
            "AIoT Edge Intelligence, Predictive Maintenance 4.0, Digital Twin Track Simulation, "
            "Federated Learning for distributed sensor nodes, Blockchain-based tamper-proof maintenance logs, "
            "5G-NR URLLC for ultra-reliable low-latency track alerts"
        ),
    },
    {
        "year": "SIH 2025 / 2026",
        "ps_no": "SIH25033",
        "org": "Ministry of Corporate Affairs",
        "category": "Software",
        "description": "AI-Based Smart Allocation Engine for PM Internship Scheme",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript (ES6+), Axios<br/>"
            "<b>Backend:</b> Python (Django REST Framework / FastAPI), Celery for async task processing<br/>"
            "<b>Database:</b> PostgreSQL (primary), Redis (caching + job queue)<br/>"
            "<b>AI/ML:</b> scikit-learn (classification, clustering), XGBoost / LightGBM for ranking, "
            "pandas, NumPy for data processing, NLTK/spaCy for resume parsing<br/>"
            "<b>Matching Algorithm:</b> Hungarian Algorithm / Gale-Shapley for optimal allocation, "
            "cosine similarity + TF-IDF for skill matching<br/>"
            "<b>Authentication:</b> JWT, OAuth 2.0, DigiLocker API integration<br/>"
            "<b>Deployment:</b> Docker, Nginx, Gunicorn, AWS EC2/ECS or NIC Cloud<br/>"
            "<b>Testing:</b> pytest, Selenium for E2E tests"
        ),
        "buzzword": (
            "Transformer-based Skill Embeddings (BERT/IndicBERT), Graph Neural Networks for "
            "applicant-internship matching, Reinforcement Learning for adaptive allocation optimization, "
            "Explainable AI (SHAP/LIME) for transparent decision-making"
        ),
    },
    {
        "year": "SIH 2025 / 2026",
        "ps_no": "SIH25043",
        "org": "Ministry of Earth Sciences (MoES)",
        "category": "Hardware",
        "description": "Embedded Intelligent Microscopy System for Identification and Counting of Microscopic Marine Organisms",
        "tech_stack": (
            "<b>Hardware:</b> Raspberry Pi 4/5, Pi Camera Module v3 (HQ) or USB microscope camera, "
            "motorized XY stage (stepper motors + A4988 drivers), LED ring illumination, "
            "custom 3D-printed microscope mount, Arduino Nano for stage control<br/>"
            "<b>Optics:</b> Brightfield/darkfield illumination, 10x-40x objective lenses, "
            "achromatic lens assembly<br/>"
            "<b>Computer Vision:</b> OpenCV, YOLOv8/YOLOv9 for object detection, "
            "U-Net for segmentation of organisms<br/>"
            "<b>ML Framework:</b> PyTorch / TensorFlow, ONNX Runtime for edge inference, "
            "dataset: annotated marine plankton images (WHOI-Plankton dataset as baseline)<br/>"
            "<b>Backend:</b> Python (Flask), SQLite for local storage, JSON export<br/>"
            "<b>GUI:</b> PyQt5 / Tkinter for on-device interface, or React.js web dashboard<br/>"
            "<b>Communication:</b> Wi-Fi (built-in RPi), optional 4G HAT for remote areas"
        ),
        "buzzword": (
            "Vision Transformer (ViT) for plankton classification, Few-Shot Learning for rare species, "
            "Edge TPU acceleration (Google Coral), Automated Microscopy Digital Twin, "
            "Citizen Science API integration for crowd-validated taxonomy"
        ),
    },
    {
        "year": "SIH 2025 / 2026",
        "ps_no": "SIH25054",
        "org": "Ministry of Consumer Affairs, Food & Public Distribution",
        "category": "Hardware",
        "description": "Automated High-Current Short-Circuit Test System for MCB to comply with IEC 60898-1:2015",
        "tech_stack": (
            "<b>Hardware:</b> High-current transformer (adjustable up to 10kA), programmable power supply, "
            "current shunt resistors + Hall-effect sensors (ACS758), voltage dividers, "
            "high-speed DAQ (NI DAQ / ADS1256 24-bit ADC), relay switching matrix, "
            "solenoid-actuated test fixture, safety interlock system<br/>"
            "<b>Microcontroller:</b> STM32F4 / Arduino Mega for test sequencing and relay control<br/>"
            "<b>Instrumentation:</b> Oscilloscope integration (SCPI protocol), Rogowski coils for transient current<br/>"
            "<b>Software:</b> Python (PyVISA for instrument control, NumPy/SciPy for waveform analysis), "
            "LabVIEW alternative: Python + NI-DAQmx<br/>"
            "<b>GUI:</b> PyQt5 / Electron.js for test control panel<br/>"
            "<b>Data & Reports:</b> SQLite/PostgreSQL, ReportLab/Matplotlib for auto-generated test certificates<br/>"
            "<b>Safety:</b> Hardware watchdog timer, emergency stop circuit, optocoupler isolation"
        ),
        "buzzword": (
            "IIoT-enabled remote test monitoring, Cloud-based compliance certificate blockchain, "
            "Digital Twin of MCB breaking mechanism, AI-based pass/fail waveform classification, "
            "Automated robotic MCB loading system"
        ),
    },
    {
        "year": "SIH 2025 / 2026",
        "ps_no": "SIH25065",
        "org": "Ministry of Jal Shakti",
        "category": "Software",
        "description": "Designing and development of an application for on spot assessment of Roof Top Rain water harvesting and artificial recharge potential and size of the RTRWH and AR.",
        "tech_stack": (
            "<b>Frontend:</b> React Native / Flutter (cross-platform mobile), HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js (Express) as alternative<br/>"
            "<b>Database:</b> PostgreSQL + PostGIS (geospatial queries), MongoDB for flexible document storage<br/>"
            "<b>GIS/Mapping:</b> Leaflet.js / Mapbox GL JS, OpenStreetMap tiles, Google Maps API, "
            "QGIS for offline geospatial analysis<br/>"
            "<b>Hydrology Calculations:</b> Python (NumPy, SciPy) — runoff coefficient models, "
            "rational method (Q=CIA), storage tank sizing algorithms, infiltration rate estimation<br/>"
            "<b>Data Sources:</b> IMD rainfall data API, CGWB aquifer maps, SRTM/DEM elevation data, "
            "Bhuvan (ISRO) satellite imagery API<br/>"
            "<b>Camera/AR:</b> Device camera for roof measurement (ARCore/ARKit for area estimation)<br/>"
            "<b>Reports:</b> PDF generation (jsPDF / ReportLab), offline-first with PWA capabilities<br/>"
            "<b>Auth:</b> Firebase Auth / JWT"
        ),
        "buzzword": (
            "LiDAR-based rooftop area computation via smartphone, Satellite-AI roof segmentation "
            "(DeepLabV3+), Digital Twin Water Balance Model, Blockchain-verified rainwater credits, "
            "GeoAI for automated aquifer recharge suitability mapping"
        ),
    },
    {
        "year": "SIH 2025 / 2026",
        "ps_no": "SIH25066",
        "org": "Ministry of Jal Shakti",
        "category": "Software",
        "description": "Development of an AI-driven ChatBOT for INGRES as a virtual assistant",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, WebSocket for real-time chat<br/>"
            "<b>Backend:</b> Python (FastAPI / Flask), Node.js (Express) as alternative<br/>"
            "<b>NLP/AI:</b> LangChain + RAG (Retrieval-Augmented Generation), OpenAI API / Gemini API / "
            "local LLM (Llama 3, Mistral via Ollama), sentence-transformers for embeddings, "
            "Bhashini API for multilingual support (Hindi + regional languages)<br/>"
            "<b>Vector Database:</b> ChromaDB / FAISS / Pinecone for document embedding search<br/>"
            "<b>Knowledge Base:</b> INGRES documents ingested via LlamaIndex / LangChain document loaders, "
            "PDF/DOCX parsing (PyMuPDF, python-docx)<br/>"
            "<b>Database:</b> PostgreSQL (conversation logs), Redis (session cache)<br/>"
            "<b>Voice:</b> Web Speech API / Google Speech-to-Text for voice input<br/>"
            "<b>Deployment:</b> Docker, Nginx, Gunicorn, AWS/GCP or NIC Cloud<br/>"
            "<b>Testing:</b> pytest, Postman for API testing"
        ),
        "buzzword": (
            "Agentic RAG with tool-calling capabilities, Multi-modal input (image + text), "
            "Knowledge Graph integration (Neo4j) for connected water resource data, "
            "Conversational Memory with sliding window + summary buffers, "
            "Fine-tuned IndicBERT for groundwater domain-specific NLU"
        ),
    },
    {
        "year": "SIH 2025 / 2026",
        "ps_no": "SIH25077",
        "org": "Government of Kerala",
        "category": "Hardware",
        "description": "A hardware that can detect and prevent unauthorized use of electric fences",
        "tech_stack": (
            "<b>Hardware:</b> ESP32/STM32 MCU, current transformer (CT) sensors for line monitoring, "
            "voltage sensors (ZMPT101B), relay modules for fence power cutoff, "
            "GSM/4G module (SIM800L/SIM7600) for alerts, GPS module, "
            "tamper-proof enclosure (IP65), backup battery (18650 LiPo)<br/>"
            "<b>Sensing:</b> Non-invasive AC current sensor (SCT-013), pulse frequency analysis "
            "for fence energizer signature detection, PIR/IR beam sensors for perimeter<br/>"
            "<b>Firmware:</b> C/C++ (Arduino / ESP-IDF), FreeRTOS for multi-task scheduling<br/>"
            "<b>Signal Processing:</b> FFT-based frequency analysis to distinguish authorized vs "
            "unauthorized energizer patterns<br/>"
            "<b>Backend:</b> Python (Flask/FastAPI), MySQL/PostgreSQL<br/>"
            "<b>Dashboard:</b> React.js / HTML5+JS, Leaflet.js for location mapping<br/>"
            "<b>Alerts:</b> SMS (Twilio/GSM), push notifications (Firebase FCM), buzzer/siren<br/>"
            "<b>Power:</b> Solar panel + charge controller for off-grid deployment"
        ),
        "buzzword": (
            "AI-based energizer signature fingerprinting, LoRaMesh network for wide-area fence monitoring, "
            "Drone-based aerial fence inspection integration, Blockchain-based fence registration ledger, "
            "Computer Vision for physical fence tampering detection"
        ),
    },
    {
        "year": "SIH 2025 / 2026",
        "ps_no": "SIH25080",
        "org": "Government of Kerala",
        "category": "Software",
        "description": "Document Overload at Kochi Metro Rail Limited (KMRL)-An automated solution",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Angular, HTML5, CSS3, JavaScript, Material UI<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js (Express)<br/>"
            "<b>Database:</b> PostgreSQL (metadata), Elasticsearch (full-text search & indexing)<br/>"
            "<b>Document Processing:</b> Apache Tika / PyMuPDF for text extraction from PDFs, "
            "python-docx for DOCX, Tesseract OCR for scanned documents, "
            "pdf2image + PIL for image preprocessing<br/>"
            "<b>NLP/AI:</b> spaCy / NLTK for NER and keyword extraction, "
            "sentence-transformers for semantic search, "
            "topic modeling (LDA via Gensim), auto-summarization (T5/BART)<br/>"
            "<b>Classification:</b> scikit-learn / XGBoost for document categorization, "
            "rule-based tagging engine<br/>"
            "<b>Storage:</b> MinIO / AWS S3 for document blob storage, versioning support<br/>"
            "<b>Workflow:</b> Camunda / custom workflow engine for approval routing<br/>"
            "<b>Auth:</b> LDAP/AD integration, RBAC, JWT<br/>"
            "<b>Deployment:</b> Docker, Docker Compose, Nginx"
        ),
        "buzzword": (
            "LLM-powered intelligent document assistant (chat with your documents), "
            "Knowledge Graph construction from unstructured documents, "
            "Zero-shot document classification using CLIP/BERT, "
            "Robotic Process Automation (RPA) for auto-filing, "
            "Generative AI-based report drafting from ingested documents"
        ),
    },
    {
        "year": "SIH 2025 / 2026",
        "ps_no": "SIH25081",
        "org": "Government of Kerala",
        "category": "Software",
        "description": "AI-Driven Train Induction Planning & Scheduling for Kochi Metro Rail Limited (KMRL)",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, FullCalendar.js for scheduling UI, "
            "D3.js / Plotly for Gantt charts and visualizations<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Celery + Redis for async scheduling jobs<br/>"
            "<b>Database:</b> PostgreSQL (schedules, constraints, rolling stock data)<br/>"
            "<b>Optimization:</b> Google OR-Tools (constraint programming, vehicle routing), "
            "PuLP / SciPy.optimize for linear programming, "
            "custom genetic algorithm (DEAP library) for multi-objective scheduling<br/>"
            "<b>AI/ML:</b> scikit-learn / XGBoost for demand prediction, "
            "LSTM / Prophet for passenger flow forecasting, "
            "pandas, NumPy for data processing<br/>"
            "<b>Simulation:</b> SimPy for discrete-event train movement simulation<br/>"
            "<b>Integration:</b> REST APIs for real-time train status feeds, "
            "GTFS format support for public transit data<br/>"
            "<b>Deployment:</b> Docker, PostgreSQL replication, Nginx, Gunicorn"
        ),
        "buzzword": (
            "Deep Reinforcement Learning (DRL) for dynamic rescheduling, "
            "Digital Twin of metro network for what-if scenario simulation, "
            "Quantum-inspired optimization (D-Wave / Qiskit), "
            "Multi-Agent System for decentralized train coordination, "
            "Federated Learning across metro systems for transfer-learning schedules"
        ),
    },
    {
        "year": "SIH 2025 / 2026",
        "ps_no": "SIH25091",
        "org": "Government of Jammu and Kashmir",
        "category": "Software",
        "description": "AI-Based Timetable Generation System aligned with NEP 2020 for Multidisciplinary Education Structures",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript, "
            "react-big-calendar / FullCalendar.js for timetable display<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js (Express) as alternative<br/>"
            "<b>Database:</b> PostgreSQL (faculty, rooms, courses, constraints), Redis (caching)<br/>"
            "<b>Optimization Engine:</b> Google OR-Tools (CP-SAT solver for constraint satisfaction), "
            "PuLP for integer linear programming, "
            "custom genetic algorithm (DEAP / PyGAD) for timetable optimization<br/>"
            "<b>NEP 2020 Logic:</b> Multi-entry/multi-exit rules engine, credit-based semester mapping, "
            "major/minor/elective slot allocation logic<br/>"
            "<b>AI/ML:</b> scikit-learn for preference learning from historical timetable data, "
            "reinforcement learning (Stable Baselines3) for iterative improvement<br/>"
            "<b>Export:</b> PDF (ReportLab), Excel (openpyxl), iCal (.ics) format<br/>"
            "<b>Auth:</b> JWT, role-based access (Admin, HOD, Faculty, Student)<br/>"
            "<b>Deployment:</b> Docker, Nginx, Gunicorn, CI/CD with GitHub Actions"
        ),
        "buzzword": (
            "Graph Coloring Neural Networks for conflict-free scheduling, "
            "Transformer-based preference modeling for faculty satisfaction, "
            "Quantum Annealing for NP-hard timetable optimization, "
            "Self-adaptive evolutionary algorithms with real-time constraint relaxation, "
            "LLM-powered natural language constraint specification"
        ),
    },
    {
        "year": "SIH 2025 / 2026",
        "ps_no": "SIH25102",
        "org": "Government of Rajasthan",
        "category": "Software",
        "description": "AI-based drop-out prediction and counseling system",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript, Chart.js for analytics dashboards<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Celery for batch prediction jobs<br/>"
            "<b>Database:</b> PostgreSQL (student records, attendance, grades), Redis (caching)<br/>"
            "<b>AI/ML:</b> scikit-learn (Random Forest, Gradient Boosting), XGBoost / LightGBM for "
            "dropout risk scoring, pandas + NumPy for feature engineering, "
            "SMOTE for handling class imbalance<br/>"
            "<b>Feature Engineering:</b> Attendance %, grade trends, socioeconomic indicators, "
            "engagement metrics, distance-from-school, family income proxy<br/>"
            "<b>Explainability:</b> SHAP / LIME for transparent risk factor reporting<br/>"
            "<b>Counseling Module:</b> Appointment scheduling (FullCalendar.js), "
            "video call integration (Jitsi Meet / WebRTC), chatbot for student queries<br/>"
            "<b>Notifications:</b> SMS (Twilio / MSG91), Email (SendGrid), Push (Firebase FCM)<br/>"
            "<b>Auth:</b> JWT, RBAC (Admin, Teacher, Counselor, Student, Parent)<br/>"
            "<b>Deployment:</b> Docker, Nginx, Gunicorn"
        ),
        "buzzword": (
            "Temporal Graph Networks for social influence modeling on dropout, "
            "Survival Analysis (Cox Proportional Hazards) for time-to-dropout prediction, "
            "LLM-powered empathetic counseling chatbot, "
            "Causal Inference (DoWhy) for intervention impact estimation, "
            "Federated Learning across school districts for privacy-preserving model training"
        ),
    },
    {
        "year": "SIH 2025 / 2026",
        "ps_no": "SIH25103",
        "org": "Government of Rajasthan",
        "category": "Software",
        "description": "ERP-based Integrated Student Management system",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Angular, HTML5, CSS3, JavaScript, Ant Design / Material UI<br/>"
            "<b>Backend:</b> Python (Django) or Java (Spring Boot), REST API architecture<br/>"
            "<b>Database:</b> PostgreSQL (primary RDBMS), Redis (session management, caching)<br/>"
            "<b>ERP Modules:</b> Admission management, fee collection (Razorpay/PayU integration), "
            "attendance tracking, exam & grading system, library management, "
            "hostel management, transport tracking, HR/payroll<br/>"
            "<b>Reporting:</b> Jasper Reports / ReportLab for PDF generation, "
            "Apache POI / openpyxl for Excel exports, Chart.js for dashboards<br/>"
            "<b>Authentication:</b> JWT + OAuth 2.0, LDAP integration, SSO support<br/>"
            "<b>File Storage:</b> MinIO / AWS S3 for documents and certificates<br/>"
            "<b>Messaging:</b> RabbitMQ / Kafka for inter-module event-driven communication<br/>"
            "<b>Mobile:</b> React Native / Flutter for companion app<br/>"
            "<b>Deployment:</b> Docker, Kubernetes (for scale), Nginx, PostgreSQL replication"
        ),
        "buzzword": (
            "Microservices Architecture with API Gateway (Kong/Traefik), "
            "Event Sourcing + CQRS for audit-grade data integrity, "
            "AI-powered academic analytics and performance prediction, "
            "Blockchain-based tamper-proof transcript/certificate issuance, "
            "Low-code workflow builder for custom administrative processes"
        ),
    },

    # ========================================================================
    # SIH 2024 (55 Statements)
    # ========================================================================
    {
        "year": "SIH 2024",
        "ps_no": "SIH1771",
        "org": "Ministry of Jal Shakti",
        "category": "Hardware",
        "description": "Personalized testing kits for testing Residual Silver ion level at delivery points",
        "tech_stack": (
            "<b>Hardware:</b> Colorimetric test strip with silver-ion-specific reagent (DPD analog for Ag+), "
            "portable spectrophotometer/colorimeter (photodiode + LED at specific wavelength), "
            "Arduino Nano / ESP32 for ADC reading and BLE data transfer, "
            "3D-printed cuvette holder, LCD display (SSD1306 OLED)<br/>"
            "<b>Optics:</b> 420nm LED source, TSL2591 light sensor or OPT3001 for absorbance measurement<br/>"
            "<b>Calibration:</b> Known silver-ion standard solutions, polynomial curve fitting (NumPy)<br/>"
            "<b>Mobile App:</b> Flutter / React Native for result display, camera-based colorimetric analysis (OpenCV)<br/>"
            "<b>Backend:</b> Python (FastAPI), PostgreSQL for test logs, geolocation tagging<br/>"
            "<b>Reports:</b> Auto-generated PDF compliance reports"
        ),
        "buzzword": (
            "Electrochemical Ion-Selective Electrode (ISE) with nanomaterial-enhanced sensitivity, "
            "AI-based color gradient analysis for sub-ppm detection, "
            "IoT-connected water quality mesh network, "
            "Lateral Flow Assay with smartphone-readable QR-coded results"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1770",
        "org": "Ministry of Jal Shakti",
        "category": "Hardware",
        "description": "Personalized testing kits for testing Bacteriological contamination at delivery points",
        "tech_stack": (
            "<b>Hardware:</b> ATP bioluminescence sensor module (luminometer), "
            "enzyme substrate test (Colilert-type ONPG/MUG reagent), UV LED (365nm) + photodetector, "
            "ESP32/Arduino Nano MCU, temperature-controlled incubation chamber (Peltier + PID control), "
            "3D-printed portable enclosure, OLED display<br/>"
            "<b>Detection:</b> Fluorescence detection circuit (PMT or photodiode), "
            "membrane filtration assembly for concentration<br/>"
            "<b>Mobile App:</b> Flutter / React Native, camera for fluorescence image capture, "
            "OpenCV for intensity quantification<br/>"
            "<b>Backend:</b> Python (FastAPI), PostgreSQL, GPS-tagged test results<br/>"
            "<b>Compliance:</b> IS 10500 / WHO guidelines comparison engine<br/>"
            "<b>Connectivity:</b> BLE for data sync to phone, 4G upload to central server"
        ),
        "buzzword": (
            "CRISPR-Cas12a/13 based rapid pathogen detection, "
            "Microfluidic Lab-on-a-Chip for single-cell bacterial counting, "
            "AI-powered colony morphology classification, "
            "Blockchain-immutable water safety certification chain"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1752",
        "org": "Ministry of Communication",
        "category": "Software",
        "description": "Measurement and Monitoring of Counter Services - Develop a simple to use application for measurement and monitoring of counter services offered by Post Offices for their customers while providing ease of access to mail, parcel, financial, payment, insurance and citizen centric services from each Post Office.",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript, responsive design (Bootstrap/MUI)<br/>"
            "<b>Backend:</b> Python (Django / FastAPI) or Node.js (Express)<br/>"
            "<b>Database:</b> PostgreSQL (transactional data), InfluxDB/TimescaleDB (time-series metrics)<br/>"
            "<b>Computer Vision:</b> YOLOv8 for people counting, OpenCV for queue length estimation, "
            "DeepSORT for person tracking in CCTV feed<br/>"
            "<b>Video Processing:</b> FFmpeg for stream handling, GStreamer, RTSP protocol<br/>"
            "<b>Analytics:</b> Python (pandas, Matplotlib, Plotly), service time calculation, "
            "wait time estimation, counter utilization metrics<br/>"
            "<b>Dashboard:</b> Grafana / custom React dashboard with real-time WebSocket updates<br/>"
            "<b>Notifications:</b> Email (SMTP), SMS (MSG91), push notifications<br/>"
            "<b>Deployment:</b> Docker, Nginx, CUDA-enabled GPU server for CV inference"
        ),
        "buzzword": (
            "Transformer-based activity recognition for service categorization, "
            "Emotion AI (sentiment analysis from facial cues) for customer satisfaction scoring, "
            "Digital Twin of post office layout for footfall simulation, "
            "Edge AI on NVIDIA Jetson for real-time on-premise processing"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1742",
        "org": "Ministry of Education",
        "category": "Software",
        "description": "Standardizing Odd School Structures to Improve Educational Policy Implementation and Resource Allocation",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, Ant Design / Material UI<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js (Express)<br/>"
            "<b>Database:</b> PostgreSQL (school records, UDISE+ data), Elasticsearch (search/filter)<br/>"
            "<b>Data Processing:</b> pandas, NumPy, OpenPyXL for UDISE+ data ingestion, "
            "fuzzy matching (fuzzywuzzy / RapidFuzz) for school name deduplication<br/>"
            "<b>Classification:</b> scikit-learn (decision trees, clustering) for school structure categorization, "
            "rule-based engine for NEP 2020 structure mapping (5+3+3+4)<br/>"
            "<b>GIS/Mapping:</b> Leaflet.js / Mapbox, PostGIS for geospatial school distribution analysis<br/>"
            "<b>Reporting:</b> Chart.js / D3.js for policy dashboards, ReportLab for PDF reports<br/>"
            "<b>Auth:</b> JWT, RBAC (Central, State, District, Block levels)<br/>"
            "<b>Deployment:</b> Docker, Nginx, Gunicorn"
        ),
        "buzzword": (
            "Graph Database (Neo4j) for school network relationship modeling, "
            "AI-powered resource optimization via multi-objective genetic algorithms, "
            "Predictive modeling for enrollment trend analysis, "
            "NLP-based policy document parsing for automated compliance checking"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1740",
        "org": "Indian Space Research Organization (ISRO)",
        "category": "Software",
        "description": "Development of map-matching algorithm using AI-ML techniques to distinguish vehicular movement on highway and service road",
        "tech_stack": (
            "<b>Frontend:</b> React.js, Leaflet.js / Mapbox GL JS for map visualization<br/>"
            "<b>Backend:</b> Python (FastAPI / Flask)<br/>"
            "<b>GIS:</b> PostGIS, OpenStreetMap data (Overpass API), OSRM for routing, "
            "Shapely / GeoPandas for geometric operations<br/>"
            "<b>Map Matching:</b> Hidden Markov Model (HMM) based map matching (Valhalla / GraphHopper), "
            "custom HMM implementation (hmmlearn), Viterbi algorithm<br/>"
            "<b>AI/ML:</b> scikit-learn (SVM, Random Forest for road classification), "
            "TensorFlow/PyTorch for deep learning approach (1D-CNN on GPS sequences), "
            "feature engineering: speed, heading change, altitude delta, HDOP<br/>"
            "<b>Data:</b> GPS trajectory datasets, road network shapefiles (NRSC/Bhuvan), "
            "pandas, NumPy for processing<br/>"
            "<b>Evaluation:</b> Precision/recall on ground-truth labeled trajectories<br/>"
            "<b>Deployment:</b> Docker, REST API for real-time map matching"
        ),
        "buzzword": (
            "Attention-based Sequence-to-Sequence model for trajectory classification, "
            "Graph Neural Networks on road network topology, "
            "Satellite imagery fusion (Sentinel-2) for road segment verification, "
            "Reinforcement Learning for adaptive map matching under GPS drift"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1737",
        "org": "Indian Space Research Organization (ISRO)",
        "category": "Software",
        "description": "Automatic Modulation Recognition software for DVB-S2X waveforms",
        "tech_stack": (
            "<b>Signal Processing:</b> Python (NumPy, SciPy), GNU Radio for SDR pipeline, "
            "FFT/STFT for spectral analysis, cyclostationary feature extraction<br/>"
            "<b>AI/ML:</b> PyTorch / TensorFlow for deep learning AMR models, "
            "CNN (AlexNet/ResNet on constellation diagrams), "
            "LSTM/GRU for temporal feature extraction from I/Q samples, "
            "scikit-learn baseline (SVM, k-NN on cumulant features)<br/>"
            "<b>DVB-S2X Specifics:</b> LDPC/BCH decoder awareness, MODCOD identification, "
            "support for QPSK to 256APSK modulation schemes<br/>"
            "<b>Data Generation:</b> MATLAB/Simulink or GNU Radio for synthetic waveform generation "
            "with varying SNR, channel impairments (AWGN, Rician fading)<br/>"
            "<b>GUI:</b> PyQt5 / Tkinter for real-time spectrum and constellation display<br/>"
            "<b>SDR Hardware:</b> RTL-SDR / ADALM-Pluto / USRP B200 for real-world testing<br/>"
            "<b>Deployment:</b> C++ optimized inference, ONNX Runtime"
        ),
        "buzzword": (
            "Transformer-based AMR (Signal Transformer), "
            "Generative Adversarial Networks for data augmentation under low-SNR, "
            "Federated Learning across ground stations, "
            "Neuromorphic computing for ultra-low-latency modulation recognition, "
            "Explainable AI for modulation decision confidence scoring"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1736",
        "org": "Indian Space Research Organization (ISRO)",
        "category": "Software",
        "description": "AI based frame interpolation, video generation and display system for WMS services",
        "tech_stack": (
            "<b>Frontend:</b> React.js, Leaflet.js / OpenLayers for WMS tile display, HTML5 Canvas/WebGL<br/>"
            "<b>Backend:</b> Python (FastAPI / Flask), GeoServer for WMS endpoints<br/>"
            "<b>AI/Frame Interpolation:</b> PyTorch (RIFE / IFRNet / AMT for frame interpolation), "
            "optical flow estimation (RAFT), temporal super-resolution<br/>"
            "<b>Video Generation:</b> FFmpeg for encoding/muxing, H.264/H.265 codec, "
            "OpenCV for frame manipulation<br/>"
            "<b>Geospatial:</b> GDAL, Rasterio for GeoTIFF processing, pyproj for CRS transformations, "
            "OGC WMS/WMTS protocol compliance<br/>"
            "<b>Data:</b> Satellite imagery tiles (Bhuvan, Sentinel), "
            "time-series raster data for weather/environment<br/>"
            "<b>GPU:</b> CUDA, cuDNN for accelerated inference<br/>"
            "<b>Deployment:</b> Docker, Nginx, GPU-enabled server (NVIDIA T4/A10)"
        ),
        "buzzword": (
            "Diffusion Models for satellite image temporal interpolation, "
            "Neural Radiance Fields (NeRF) for 3D geospatial view synthesis, "
            "Foundation Models for remote sensing (Prithvi by NASA/IBM), "
            "Streaming latent video generation for real-time WMS animation"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1735",
        "org": "Indian Space Research Organization (ISRO)",
        "category": "Software",
        "description": "On-device semantic segmentation of WMS services with geospatial data export",
        "tech_stack": (
            "<b>AI/ML:</b> PyTorch / TensorFlow for training (DeepLabV3+, U-Net, SegFormer), "
            "ONNX export for cross-platform inference, "
            "TensorFlow Lite / ONNX Runtime Mobile for on-device deployment<br/>"
            "<b>Dataset:</b> Satellite imagery (Sentinel-2, Landsat), land use/land cover labels, "
            "augmentation (Albumentations)<br/>"
            "<b>On-Device:</b> Android (Kotlin/Java + TFLite), iOS (Swift + Core ML), "
            "model quantization (INT8) for mobile performance<br/>"
            "<b>Geospatial:</b> GDAL, Rasterio, GeoPandas for vector export (GeoJSON, Shapefile, KML), "
            "pyproj for coordinate transformations, WMS/WMTS client (OWSLib)<br/>"
            "<b>Frontend:</b> React Native / Flutter for cross-platform mobile app, Mapbox/Leaflet<br/>"
            "<b>Export:</b> GeoJSON, GeoTIFF with segmentation mask overlay, KML for Google Earth<br/>"
            "<b>Backend:</b> Python (FastAPI), PostgreSQL + PostGIS"
        ),
        "buzzword": (
            "Foundation Models for Earth Observation (Prithvi, SatMAE), "
            "Edge TPU / Neural Processing Unit acceleration, "
            "Self-supervised pre-training on unlabeled satellite imagery, "
            "Federated Learning for privacy-preserving distributed model training across devices"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1730",
        "org": "AICTE",
        "category": "Software",
        "description": "AI driven Inspection of Institutions",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript, Material UI<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js (Express)<br/>"
            "<b>Database:</b> PostgreSQL, Elasticsearch for document search<br/>"
            "<b>Document Analysis:</b> Tesseract OCR, PyMuPDF for PDF parsing, "
            "spaCy for NER (extract faculty names, infrastructure details), "
            "regex-based compliance checkers<br/>"
            "<b>Computer Vision:</b> YOLOv8 for infrastructure verification from uploaded images "
            "(lab equipment, classrooms), image classification (ResNet/EfficientNet)<br/>"
            "<b>AI/ML:</b> scikit-learn for risk scoring and anomaly detection, "
            "XGBoost for compliance prediction, NLP for self-assessment report analysis<br/>"
            "<b>Video:</b> WebRTC for remote virtual inspection, screen recording<br/>"
            "<b>Scheduling:</b> Celery + Redis for inspection task queue<br/>"
            "<b>Reporting:</b> ReportLab / WeasyPrint for auto-generated inspection reports<br/>"
            "<b>Auth:</b> JWT, OAuth 2.0, RBAC"
        ),
        "buzzword": (
            "LLM-powered automated compliance Q&A from uploaded documents, "
            "360° virtual campus tour verification using VR, "
            "Deepfake detection for video inspection integrity, "
            "Satellite imagery verification of campus area claims, "
            "AI-generated inspection report narratives"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1729",
        "org": "AICTE",
        "category": "Software",
        "description": "AI supported AICTE Approval process portal",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Angular, HTML5, CSS3, JavaScript, Ant Design<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Celery for background processing<br/>"
            "<b>Database:</b> PostgreSQL (application data), Redis (caching, session), "
            "Elasticsearch (search across applications)<br/>"
            "<b>Document Processing:</b> Tesseract OCR, PyMuPDF, python-docx, "
            "tabula-py for table extraction from PDFs<br/>"
            "<b>AI/ML:</b> scikit-learn (decision tree, rule-based) for auto-verification of criteria, "
            "NLP (spaCy) for document information extraction, "
            "anomaly detection for fraudulent submissions<br/>"
            "<b>Workflow Engine:</b> Django-viewflow / custom state machine for multi-stage approval<br/>"
            "<b>Notifications:</b> Email (Django email), SMS (MSG91), dashboard alerts<br/>"
            "<b>Reporting:</b> ReportLab, openpyxl for Excel exports<br/>"
            "<b>Auth:</b> JWT, OAuth 2.0, Aadhaar eKYC integration<br/>"
            "<b>Deployment:</b> Docker, Nginx, Gunicorn, CI/CD"
        ),
        "buzzword": (
            "LLM-based intelligent form-filling assistant, "
            "Knowledge Graph for regulatory cross-referencing, "
            "AI-driven predictive application outcome scoring, "
            "Blockchain-based immutable approval audit trail, "
            "Robotic Process Automation for data entry from legacy systems"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1726",
        "org": "Ministry of Housing and Urban Affairs",
        "category": "Software",
        "description": "Utilization of aerial/drone-based images for monitoring of progress of construction activities for building construction projects",
        "tech_stack": (
            "<b>Frontend:</b> React.js, Leaflet.js / Cesium.js (3D), HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (Django / FastAPI)<br/>"
            "<b>Computer Vision:</b> YOLOv8 / Detectron2 for object detection (cranes, structures, materials), "
            "semantic segmentation (DeepLabV3+) for construction area mapping, "
            "OpenCV for image preprocessing<br/>"
            "<b>Photogrammetry:</b> OpenDroneMap (ODM) for orthomosaic and 3D point cloud generation, "
            "COLMAP for Structure-from-Motion<br/>"
            "<b>Change Detection:</b> Siamese CNN for temporal image comparison, "
            "pixel-level differencing with thresholding<br/>"
            "<b>GIS:</b> PostGIS, GDAL, Rasterio, GeoJSON overlays<br/>"
            "<b>Storage:</b> MinIO / AWS S3 for drone image storage<br/>"
            "<b>Dashboard:</b> Chart.js, Plotly for progress % visualization<br/>"
            "<b>Database:</b> PostgreSQL<br/>"
            "<b>Deployment:</b> Docker, GPU server for inference"
        ),
        "buzzword": (
            "4D BIM + Drone imagery overlay for as-planned vs as-built analysis, "
            "NeRF for photorealistic 3D construction site reconstruction, "
            "Foundation models (SAM - Segment Anything) for zero-shot construction element detection, "
            "Autonomous drone flight planning with AI-optimized waypoints"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1725",
        "org": "Ministry of Housing and Urban Affairs",
        "category": "Software",
        "description": "Utilization of images for monitoring of progress of construction activities for building construction projects.",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, image comparison slider<br/>"
            "<b>Backend:</b> Python (Django / FastAPI)<br/>"
            "<b>Computer Vision:</b> YOLOv8 for construction element detection, "
            "OpenCV for image registration and alignment, "
            "ResNet/EfficientNet for progress stage classification<br/>"
            "<b>Change Detection:</b> Image differencing (structural similarity - SSIM), "
            "Siamese networks for temporal comparison<br/>"
            "<b>Progress Estimation:</b> Rule-based stage mapping (foundation→structure→finishing), "
            "regression models for % completion estimation<br/>"
            "<b>Database:</b> PostgreSQL, MinIO for image storage<br/>"
            "<b>Mobile:</b> React Native / Flutter for on-site photo capture with GPS tagging<br/>"
            "<b>Reporting:</b> Chart.js, ReportLab for progress reports<br/>"
            "<b>Deployment:</b> Docker, Nginx"
        ),
        "buzzword": (
            "Vision-Language Model (GPT-4V / Gemini Vision) for natural language construction status reports, "
            "BIM (Building Information Modeling) integration for planned vs actual overlay, "
            "Generative AI for construction milestone prediction, "
            "AR overlay on-site for expected vs current structure comparison"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1721",
        "org": "Ministry of Youth Affairs & Sports",
        "category": "Software",
        "description": "Intelligence and Investigations - Enhancing Anti-Doping Efforts",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript, D3.js for network graphs<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL (athlete profiles, test records), Neo4j (relationship graphs between athletes/coaches/suppliers)<br/>"
            "<b>AI/ML:</b> scikit-learn (anomaly detection - Isolation Forest), "
            "social network analysis (NetworkX) for suspicious connection detection, "
            "NLP (spaCy) for tip-off text analysis, pattern mining from ABP data<br/>"
            "<b>Data Integration:</b> ADAMS (Anti-Doping Administration & Management System) API integration, "
            "WADA code compliance rules engine<br/>"
            "<b>Analytics:</b> pandas, Matplotlib, Plotly for trend analysis, "
            "risk scoring algorithms for targeted testing<br/>"
            "<b>Security:</b> AES-256 encryption, RBAC, audit logging, GDPR/DPDP compliance<br/>"
            "<b>Notifications:</b> Secure email, encrypted messaging<br/>"
            "<b>Deployment:</b> Docker, air-gapped option for sensitive data"
        ),
        "buzzword": (
            "Graph Neural Networks for doping ring detection, "
            "Predictive AI for Biological Passport anomaly forecasting, "
            "NLP-powered dark web/social media monitoring for substance trafficking, "
            "Blockchain-based tamper-proof chain of custody for samples, "
            "Privacy-preserving computation (homomorphic encryption) for cross-border data sharing"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1711",
        "org": "Ministry of Railway",
        "category": "Software",
        "description": "Enhancing Rail Madad with AI-powered Complaint Management",
        "tech_stack": (
            "<b>Frontend:</b> React.js / React Native (mobile), HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js (Express)<br/>"
            "<b>Database:</b> PostgreSQL (complaints), Elasticsearch (full-text search), Redis (caching)<br/>"
            "<b>NLP/AI:</b> spaCy / NLTK for text classification and entity extraction, "
            "BERT/IndicBERT for multilingual complaint categorization, "
            "sentiment analysis (VADER / transformers), "
            "Bhashini API for Hindi + regional language support<br/>"
            "<b>Routing:</b> Rule-based + ML (Random Forest) for auto-assignment to departments, "
            "priority scoring algorithm based on urgency keywords<br/>"
            "<b>Analytics:</b> pandas, Matplotlib, Plotly for complaint trends and resolution dashboards<br/>"
            "<b>Image/Video:</b> OpenCV + YOLOv8 for complaint evidence analysis (dirty coaches, broken fixtures)<br/>"
            "<b>Notifications:</b> SMS (MSG91), push (FCM), email<br/>"
            "<b>Deployment:</b> Docker, Nginx, Gunicorn, CI/CD"
        ),
        "buzzword": (
            "LLM-powered auto-response drafting for common complaints, "
            "Voice-based complaint lodging with Whisper ASR, "
            "Emotion-aware priority escalation using sentiment transformers, "
            "Predictive maintenance triggers from complaint pattern analysis, "
            "Gamified resolution tracking for staff with leaderboard"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1709",
        "org": "Ministry of Power",
        "category": "Software",
        "description": "Comprehensive Automated Document Verification System for Official Documentation",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, drag-and-drop file upload<br/>"
            "<b>Backend:</b> Python (Django / FastAPI)<br/>"
            "<b>OCR:</b> Tesseract OCR, PaddleOCR (better for multi-language), "
            "Google Vision API as fallback<br/>"
            "<b>Document Parsing:</b> PyMuPDF, pdf2image, python-docx, tabula-py for tables<br/>"
            "<b>NLP/AI:</b> spaCy (NER for names, dates, IDs), regex for pattern matching "
            "(PAN, Aadhaar, GSTIN formats), "
            "LayoutLM / LayoutLMv3 for document understanding<br/>"
            "<b>Verification:</b> Cross-referencing with DigiLocker API, "
            "hash-based document tampering detection (SHA-256), "
            "digital signature validation (PyKCS11)<br/>"
            "<b>Database:</b> PostgreSQL, MinIO for document storage<br/>"
            "<b>Security:</b> AES-256 encryption at rest, TLS 1.3, audit trail logging<br/>"
            "<b>Deployment:</b> Docker, Nginx"
        ),
        "buzzword": (
            "Zero-Knowledge Proof for privacy-preserving document verification, "
            "Deepfake/forgery detection using forensic AI, "
            "Verifiable Credentials (W3C standard) with DID (Decentralized Identifiers), "
            "Multi-modal document authenticity scoring using transformer ensembles"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1702",
        "org": "Ministry of Law & Justice",
        "category": "Software",
        "description": "Bail Reckoner",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript, "
            "step-by-step wizard UI for data input<br/>"
            "<b>Backend:</b> Python (Django / FastAPI)<br/>"
            "<b>Database:</b> PostgreSQL (case data, bail criteria, IPC/BNS sections)<br/>"
            "<b>Legal Logic:</b> Rule-based engine mapping IPC/BNS sections to bail provisions, "
            "decision tree for bailable/non-bailable/cognizable classification, "
            "CrPC Section 436/437/439 logic implementation<br/>"
            "<b>NLP:</b> spaCy for legal entity extraction, "
            "sentence-transformers for case similarity matching (precedent search), "
            "LangChain + RAG for AI-assisted bail argument research<br/>"
            "<b>Data:</b> Indian Kanoon API / eSCR for case law database, "
            "structured IPC/BNS/CrPC dataset<br/>"
            "<b>Reporting:</b> ReportLab for bail application draft generation<br/>"
            "<b>Auth:</b> JWT, RBAC (Judge, Lawyer, Court Staff)<br/>"
            "<b>Deployment:</b> Docker, Nginx, data encryption at rest"
        ),
        "buzzword": (
            "Legal LLM fine-tuned on Indian case law (InLegalBERT), "
            "Graph-based case precedent network analysis, "
            "Predictive bail outcome scoring using historical data, "
            "Blockchain-based immutable bail order registry, "
            "AI-generated bail risk assessment reports with explainability"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1701",
        "org": "Ministry of Law & Justice",
        "category": "Software",
        "description": "AI-Driven Research Engine for Commercial Courts",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript, "
            "faceted search UI, document viewer (PDF.js)<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Elasticsearch for legal document search<br/>"
            "<b>Database:</b> PostgreSQL (case metadata), Elasticsearch (full-text indexing)<br/>"
            "<b>NLP/AI:</b> sentence-transformers for semantic search, "
            "LangChain + RAG (ChromaDB/FAISS as vector store), "
            "spaCy + custom NER for legal entities (parties, sections, citations), "
            "text summarization (BART / T5), "
            "citation network analysis (NetworkX)<br/>"
            "<b>Legal Data:</b> Indian Kanoon scraper/API, eSCR database, "
            "Commercial Courts Act provisions<br/>"
            "<b>Features:</b> Case timeline generation, related judgment clustering, "
            "argument extraction, statutory provision linking<br/>"
            "<b>Auth:</b> JWT, RBAC<br/>"
            "<b>Deployment:</b> Docker, Elasticsearch cluster, Nginx"
        ),
        "buzzword": (
            "Legal-domain Large Language Model (LegalLLM / InLegalBERT), "
            "Knowledge Graph of Indian commercial law with ontology (OWL/RDF), "
            "Cross-lingual legal research (Hindi-English bilingual models), "
            "Automated legal brief generation using generative AI, "
            "Quantum-enhanced similarity search for massive case databases"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1700",
        "org": "Ministry of Law & Justice",
        "category": "Software",
        "description": "Developing an AI based interactive Chatbot or virtual assistant for the Department of Justice's Website.",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, chat widget (Botpress UI / custom)<br/>"
            "<b>Backend:</b> Python (FastAPI / Flask), Node.js<br/>"
            "<b>NLP/AI:</b> LangChain + RAG with FAISS/ChromaDB, "
            "OpenAI API / Gemini API / local Llama 3 (via Ollama), "
            "Bhashini API for multilingual (Hindi + 12 regional languages), "
            "Whisper for voice-to-text<br/>"
            "<b>Knowledge Base:</b> DoJ website content, legal FAQs, Acts & Rules, "
            "LlamaIndex document loaders for PDF/HTML ingestion<br/>"
            "<b>Database:</b> PostgreSQL (logs), Redis (sessions), vector DB (ChromaDB)<br/>"
            "<b>Voice:</b> Web Speech API, Google TTS for voice responses<br/>"
            "<b>Analytics:</b> Query analytics dashboard, feedback collection, unanswered query tracking<br/>"
            "<b>Auth:</b> Session-based, optional login for personalized history<br/>"
            "<b>Deployment:</b> Docker, Nginx, Gunicorn"
        ),
        "buzzword": (
            "Multi-turn conversational AI with memory (ConversationBufferMemory), "
            "Agentic RAG with tool-use for live case status lookup, "
            "Emotion-aware response generation, "
            "Avatarized AI assistant with lip-sync (SadTalker/Wav2Lip), "
            "Voice cloning for consistent assistant persona"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1697",
        "org": "Ministry of Jal Shakti",
        "category": "Software",
        "description": "AI based chatbot for collating and dissemination of information on groundwater.",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, chat UI component<br/>"
            "<b>Backend:</b> Python (FastAPI / Flask)<br/>"
            "<b>NLP/AI:</b> LangChain + RAG, FAISS / ChromaDB for vector search, "
            "sentence-transformers for embeddings, "
            "OpenAI API / Gemini API / Llama 3 for response generation, "
            "Bhashini API for multilingual support<br/>"
            "<b>Knowledge Base:</b> CGWB reports, aquifer maps, DWLR data, "
            "well inventory databases, PDF/CSV ingestion pipeline<br/>"
            "<b>GIS Integration:</b> Leaflet.js for groundwater level maps, "
            "PostGIS for spatial queries, CGWB GIS data layers<br/>"
            "<b>Database:</b> PostgreSQL + PostGIS, Redis<br/>"
            "<b>Data Processing:</b> pandas, NumPy for water level trend analysis<br/>"
            "<b>Deployment:</b> Docker, Nginx, Gunicorn"
        ),
        "buzzword": (
            "Multimodal chatbot (accept map queries, images of well logs), "
            "Knowledge Graph of aquifer systems (Neo4j), "
            "GeoAI for groundwater potential zone prediction, "
            "LLM fine-tuned on hydrogeology corpus, "
            "Real-time DWLR data streaming into chatbot responses"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1696",
        "org": "Ministry of Jal Shakti",
        "category": "Software",
        "description": "A software application - Ground Water Level Predictor",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, Plotly.js / Chart.js for time-series plots, "
            "Leaflet.js for spatial visualization<br/>"
            "<b>Backend:</b> Python (Django / FastAPI)<br/>"
            "<b>Database:</b> PostgreSQL + PostGIS (well locations, historical levels), TimescaleDB for time-series<br/>"
            "<b>AI/ML:</b> LSTM / GRU (PyTorch/TensorFlow) for time-series forecasting, "
            "Prophet (Facebook) for seasonal decomposition, "
            "XGBoost / LightGBM for feature-based prediction, "
            "scikit-learn for baseline models<br/>"
            "<b>Features:</b> Rainfall (IMD data), temperature, soil type, land use, "
            "pumping rates, river proximity, previous water levels<br/>"
            "<b>Data Sources:</b> CGWB DWLR data, IMD rainfall API, ISRO Bhuvan land use<br/>"
            "<b>Visualization:</b> Heatmaps, contour plots (SciPy interpolation), prediction confidence intervals<br/>"
            "<b>Export:</b> CSV, PDF reports (ReportLab)<br/>"
            "<b>Deployment:</b> Docker, Nginx, scheduled model retraining (Celery/cron)"
        ),
        "buzzword": (
            "Transformer-based temporal forecasting (Temporal Fusion Transformer), "
            "Physics-Informed Neural Networks (PINNs) incorporating Darcy's law, "
            "Ensemble deep learning with uncertainty quantification, "
            "Satellite-derived soil moisture fusion (SMAP/Sentinel-1), "
            "AutoML (Auto-sklearn/TPOT) for automated model selection"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1695",
        "org": "Ministry of Jal Shakti",
        "category": "Software",
        "description": "A software application for analysis of DWLR data and raise alarms in respect of anomalous values, faulty DWLRs etc",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, Grafana-style dashboards, "
            "Leaflet.js for DWLR location map<br/>"
            "<b>Backend:</b> Python (FastAPI / Django), Celery for scheduled anomaly checks<br/>"
            "<b>Database:</b> PostgreSQL + TimescaleDB (time-series DWLR data), Redis<br/>"
            "<b>Anomaly Detection:</b> scikit-learn (Isolation Forest, LOF, DBSCAN), "
            "statistical methods (Z-score, IQR, moving average deviation), "
            "LSTM-based anomaly detection for temporal patterns<br/>"
            "<b>Fault Detection:</b> Rule-based checks (stuck values, sudden jumps, flatline detection, "
            "value range violations per aquifer type), "
            "sensor health scoring algorithm<br/>"
            "<b>Alerting:</b> Email (SMTP), SMS (MSG91/Twilio), dashboard notifications, "
            "configurable alert thresholds per DWLR<br/>"
            "<b>Reporting:</b> Automated daily/weekly reports (ReportLab/Matplotlib), "
            "pandas for data aggregation<br/>"
            "<b>Deployment:</b> Docker, Nginx, cron/Celery for periodic analysis"
        ),
        "buzzword": (
            "AutoEncoder-based anomaly detection for complex failure patterns, "
            "Predictive maintenance of DWLR hardware using survival analysis, "
            "Digital Twin of well-DWLR system for simulation, "
            "Federated anomaly detection across state-level DWLR networks, "
            "Self-healing alerts with automated ticket creation (Jira/ServiceNow API)"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1694",
        "org": "Ministry of Jal Shakti",
        "category": "Software",
        "description": "Real-time Ganga river water quality forecasting using AI-enabled DSS, satellite data, IoT, and dynamic models.",
        "tech_stack": (
            "<b>Frontend:</b> React.js, Leaflet.js / Mapbox for river stretch visualization, "
            "D3.js / Plotly.js for water quality dashboards<br/>"
            "<b>Backend:</b> Python (FastAPI / Django), Celery for async data ingestion<br/>"
            "<b>Database:</b> PostgreSQL + PostGIS + TimescaleDB, InfluxDB alternative<br/>"
            "<b>IoT Integration:</b> MQTT broker (Mosquitto), REST APIs for sensor data ingestion, "
            "CPCB real-time water quality API<br/>"
            "<b>Satellite Data:</b> Sentinel-2/Landsat (Google Earth Engine API), "
            "NDWI/chlorophyll-a indices, Rasterio/GDAL for raster processing<br/>"
            "<b>AI/ML:</b> LSTM/GRU for time-series WQ forecasting, "
            "Random Forest/XGBoost for feature-based prediction, "
            "QUAL2E/WASP-type water quality model integration<br/>"
            "<b>DSS:</b> Decision matrix for intervention recommendations, "
            "scenario simulation engine<br/>"
            "<b>Parameters:</b> BOD, COD, pH, DO, turbidity, fecal coliform, temperature<br/>"
            "<b>Deployment:</b> Docker, GPU server for model inference, CI/CD"
        ),
        "buzzword": (
            "Physics-Informed Neural Networks for hydrodynamic-water quality coupling, "
            "Digital Twin of Ganga river system, "
            "Satellite-AI fusion for real-time chlorophyll and turbidity mapping, "
            "Edge AI on IoT nodes for local anomaly detection, "
            "Transformer-based multi-variate water quality forecasting"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1693",
        "org": "Ministry of Jal Shakti",
        "category": "Software",
        "description": "Developing a Robust Hydraulic Transient Analysis Model for Hydro Power and Pumped Storage Schemes.",
        "tech_stack": (
            "<b>Numerical Methods:</b> Python (NumPy, SciPy) - Method of Characteristics (MOC) for water hammer simulation, "
            "finite difference/finite volume schemes for pressure wave propagation<br/>"
            "<b>Simulation:</b> MATLAB/Simulink (industry standard for hydraulic transients), "
            "Python alternatives: PyFluids, EPANET (via wntr library)<br/>"
            "<b>Physics:</b> Joukowsky equation implementation, surge tank modeling, "
            "turbine/pump characteristic curves (hill charts), "
            "governor response modeling<br/>"
            "<b>Frontend:</b> React.js, Plotly.js / D3.js for pressure-time curves, "
            "3D pipeline visualization (Three.js)<br/>"
            "<b>Backend:</b> Python (FastAPI), job queue (Celery) for long simulations<br/>"
            "<b>Database:</b> PostgreSQL (project configurations, simulation results)<br/>"
            "<b>Validation:</b> Comparison with HAMMER/AFT Impulse benchmarks<br/>"
            "<b>Export:</b> CSV, PDF reports with pressure envelope diagrams"
        ),
        "buzzword": (
            "Physics-Informed Neural Networks (PINNs) for real-time transient prediction, "
            "Digital Twin of penstock-turbine system, "
            "GPU-accelerated CFD (OpenFOAM) for 3D transient validation, "
            "Reduced-Order Models (ROM) for real-time control system integration, "
            "ML-based surrogate models replacing expensive MOC simulations"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1688",
        "org": "Ministry of Jal Shakti",
        "category": "Software",
        "description": "Development of handheld device/Mobile based Operation & Maintenance tool for asset & consumables inventories and finance management in context of drinking water supply scheme.",
        "tech_stack": (
            "<b>Mobile:</b> Flutter / React Native (cross-platform), offline-first with SQLite local DB<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js (Express)<br/>"
            "<b>Database:</b> PostgreSQL (server), SQLite (mobile offline), sync via REST API + conflict resolution<br/>"
            "<b>Features:</b> QR/barcode scanner (ZXing library) for asset tracking, "
            "GPS tagging for asset location, camera for condition documentation, "
            "offline form submission with auto-sync<br/>"
            "<b>Inventory:</b> FIFO/LIFO tracking, reorder level alerts, stock ledger, "
            "consumable usage analytics (pandas)<br/>"
            "<b>Finance:</b> Budget tracking, expenditure recording, bill/voucher upload, "
            "simple accounting module (income-expense ledger)<br/>"
            "<b>Reporting:</b> Chart.js for mobile dashboards, ReportLab for PDF reports<br/>"
            "<b>Auth:</b> JWT, RBAC (State, District, Block, GP levels), biometric option<br/>"
            "<b>Notifications:</b> Push (FCM), SMS for low stock alerts<br/>"
            "<b>Deployment:</b> Docker, Nginx, Play Store / APK distribution"
        ),
        "buzzword": (
            "AR-based asset identification (point camera to auto-detect equipment), "
            "Predictive consumable demand forecasting using time-series ML, "
            "Blockchain-based transparent finance audit trail, "
            "NFC/RFID asset tagging for touchless inventory, "
            "AI-powered image-based asset condition assessment"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1686",
        "org": "National Technical Research Organisation (NTRO)",
        "category": "Software",
        "description": "Tools and techniques for customisation of GPO as per CIS guidelines to deploy on offline / standalone windows.",
        "tech_stack": (
            "<b>Core:</b> PowerShell (primary scripting), Windows Group Policy Management (GPMC), "
            "LGPO.exe (Microsoft Local Group Policy Object utility), "
            "Security Compliance Toolkit (SCT) from Microsoft<br/>"
            "<b>CIS Benchmarks:</b> CIS-CAT Pro Assessor for validation, "
            "CIS Benchmark PDF parser (Python + PyMuPDF) for rule extraction<br/>"
            "<b>Automation:</b> PowerShell DSC (Desired State Configuration) for declarative policy enforcement, "
            "Ansible (Windows modules) for multi-machine deployment, "
            "Python (subprocess) for orchestration<br/>"
            "<b>GUI:</b> C# WPF / Electron.js for user-friendly GPO customization tool<br/>"
            "<b>Registry:</b> Direct registry manipulation (reg.exe, PowerShell Set-ItemProperty), "
            "SecurityPolicy .inf file generation<br/>"
            "<b>Validation:</b> Automated compliance scanning (CIS-CAT), "
            "custom PowerShell scripts for pre/post-deployment verification<br/>"
            "<b>Packaging:</b> NSIS / WiX for installer creation, USB-deployable offline package<br/>"
            "<b>Logging:</b> Windows Event Log, custom XML-based audit trail"
        ),
        "buzzword": (
            "Zero Trust Architecture alignment with CIS + NIST 800-53, "
            "ML-based policy conflict detection and resolution, "
            "Infrastructure-as-Code (IaC) for reproducible hardened OS images, "
            "Automated STIG compliance cross-mapping, "
            "AI-driven threat surface analysis post-GPO application"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1685",
        "org": "National Technical Research Organisation (NTRO)",
        "category": "Software",
        "description": "Building Offline Parallel AV Pipeline to cater multiple AVs for CII entities.",
        "tech_stack": (
            "<b>Core Architecture:</b> Python / C++ orchestration layer for parallel AV execution, "
            "multi-process architecture (multiprocessing / subprocess), "
            "YARA rules engine for custom signature scanning<br/>"
            "<b>AV Integration:</b> ClamAV (open-source, offline capable), "
            "integration with multiple AV engines via command-line interfaces, "
            "VirusTotal-compatible offline hash database<br/>"
            "<b>Scanning Pipeline:</b> File queue manager (RabbitMQ / ZeroMQ for local IPC), "
            "hash-based deduplication (SHA-256), "
            "file type detection (libmagic / python-magic), "
            "archive extraction (7-Zip, unrar, cabextract)<br/>"
            "<b>Signature Updates:</b> Sneakernet-compatible update package (USB transfer), "
            "differential signature update mechanism, GPG-signed update verification<br/>"
            "<b>Dashboard:</b> Electron.js / PyQt5 desktop application, "
            "scan result aggregation, conflict resolution when AVs disagree<br/>"
            "<b>Database:</b> SQLite (local), scan history, quarantine management<br/>"
            "<b>Deployment:</b> NSIS/WiX installer, portable deployment option"
        ),
        "buzzword": (
            "ML-based malware classification (PE header analysis, opcode sequences), "
            "Sandbox integration (Cuckoo Sandbox) for behavioral analysis, "
            "MITRE ATT&CK mapping for detected threats, "
            "Federated signature sharing between air-gapped CII nodes, "
            "Homomorphic encryption for secure multi-AV result aggregation"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1682",
        "org": "National Technical Research Organisation (NTRO)",
        "category": "Software",
        "description": "Centralized Automated Solution for Price Estimation & Reasonability.",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Angular, HTML5, CSS3, JavaScript, data tables (AG Grid / DataTables)<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL (historical price data, vendor catalog), Elasticsearch (price search)<br/>"
            "<b>Data Collection:</b> Web scraping (Scrapy / BeautifulSoup / Playwright) for market price data, "
            "GeM API integration for government marketplace prices, "
            "structured data ingestion from vendor quotations (PDF parsing via Tabula/Camelot)<br/>"
            "<b>Price Estimation:</b> Statistical methods (mean, median, percentile analysis), "
            "regression models (scikit-learn), time-series (Prophet) for price trend forecasting, "
            "parametric cost estimation models<br/>"
            "<b>Reasonability:</b> IQR-based outlier detection, benchmark comparison, "
            "Should-Cost Model implementation, historical price adjustment (inflation indexing via WPI/CPI data)<br/>"
            "<b>Reporting:</b> Auto-generated price reasonability certificates, "
            "Chart.js for trend visualization, ReportLab for PDF<br/>"
            "<b>Auth:</b> JWT, RBAC, audit trail<br/>"
            "<b>Deployment:</b> Docker, Nginx"
        ),
        "buzzword": (
            "LLM-powered natural language price query interface, "
            "Graph-based vendor relationship analysis for cartel detection, "
            "Reinforcement Learning for dynamic price negotiation strategy, "
            "Blockchain-based transparent procurement price registry, "
            "AutoML for automated cost model selection and tuning"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1680",
        "org": "National Technical Research Organisation (NTRO)",
        "category": "Software",
        "description": "Few Shot Language Agnostic Key Word Spotting system (FSLAKWS) for audio files.",
        "tech_stack": (
            "<b>Audio Processing:</b> Python (librosa, soundfile, torchaudio), "
            "FFmpeg for format conversion, VAD (Voice Activity Detection) - WebRTC VAD / Silero VAD<br/>"
            "<b>Feature Extraction:</b> Mel-spectrograms, MFCC, log-filterbanks, "
            "wav2vec 2.0 / HuBERT for self-supervised audio representations<br/>"
            "<b>Few-Shot Learning:</b> Prototypical Networks / Matching Networks (PyTorch), "
            "Siamese Networks for audio embedding similarity, "
            "metric learning with triplet loss<br/>"
            "<b>Language Agnostic:</b> Multilingual pre-trained models (XLS-R / MMS by Meta), "
            "dynamic time warping (DTW) for query-by-example matching<br/>"
            "<b>Backend:</b> Python (FastAPI), Celery for batch audio processing<br/>"
            "<b>Database:</b> PostgreSQL (metadata), MinIO/S3 for audio file storage<br/>"
            "<b>GUI:</b> React.js web interface for audio upload, keyword registration, search results<br/>"
            "<b>Deployment:</b> Docker, GPU server for inference, ONNX Runtime for optimized serving"
        ),
        "buzzword": (
            "Whisper-based zero-shot keyword detection via ASR transcript mining, "
            "Contrastive Learning (SimCLR) for robust audio embeddings, "
            "Neural Architecture Search for optimal KWS model, "
            "On-device KWS using TinyML for edge deployment, "
            "Attention-based keyword localization in long audio streams"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1672",
        "org": "Ministry of Electronics and Information Technology",
        "category": "Software",
        "description": "Develop a ML Model based solution to refine CAPTCHA.",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5 Canvas, CSS3, JavaScript for CAPTCHA widget<br/>"
            "<b>Backend:</b> Python (FastAPI / Flask), Node.js<br/>"
            "<b>CAPTCHA Generation:</b> Python (Pillow, captcha library) for image generation, "
            "random distortions (noise, rotation, warping, line overlay), "
            "font randomization, color jittering<br/>"
            "<b>Adversarial Testing:</b> PyTorch / TensorFlow - CNN (ResNet, EfficientNet) "
            "trained to break CAPTCHAs, adversarial examples (FGSM, PGD) for robustness testing<br/>"
            "<b>Behavioral Analysis:</b> Mouse movement tracking (JS), "
            "typing pattern analysis, interaction timing features, "
            "scikit-learn classifier for bot vs human behavior<br/>"
            "<b>Challenge Types:</b> Image distortion CAPTCHA, puzzle CAPTCHA (drag-and-drop), "
            "audio CAPTCHA (gTTS + noise overlay), math CAPTCHA<br/>"
            "<b>Security:</b> Rate limiting, token-based validation, session binding<br/>"
            "<b>Database:</b> Redis (token store, rate limit), PostgreSQL (analytics)<br/>"
            "<b>Deployment:</b> Docker, CDN for static assets"
        ),
        "buzzword": (
            "GAN-generated adversarial CAPTCHAs that auto-evolve against bots, "
            "Proof-of-Work based invisible CAPTCHA, "
            "Multimodal CAPTCHA combining vision + audio + interaction, "
            "Federated Learning for continuous CAPTCHA difficulty calibration, "
            "Zero-Knowledge Proof CAPTCHA for privacy-preserving human verification"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1671",
        "org": "Ministry of Electronics and Information Technology",
        "category": "Software",
        "description": "Develop a functional solution that demonstrates the face liveness detection",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, WebRTC for live camera feed<br/>"
            "<b>Backend:</b> Python (FastAPI / Flask)<br/>"
            "<b>Face Detection:</b> MediaPipe Face Mesh, dlib (68-point landmark), "
            "MTCNN, RetinaFace<br/>"
            "<b>Liveness Detection:</b> PyTorch / TensorFlow - binary classifier (live vs spoof), "
            "depth estimation from monocular RGB (MiDaS), "
            "texture analysis (LBP - Local Binary Patterns), "
            "blink detection + head movement tracking, "
            "challenge-response (turn head left/right, smile)<br/>"
            "<b>Anti-Spoofing:</b> Multi-frame analysis, frequency domain analysis (FFT on face patches), "
            "Moiré pattern detection for screen replay attacks, "
            "OULU-NPU / CASIA-FASD datasets for training<br/>"
            "<b>Mobile:</b> TensorFlow Lite / Core ML for on-device inference<br/>"
            "<b>Database:</b> PostgreSQL (session logs), MinIO for frame storage<br/>"
            "<b>Deployment:</b> Docker, ONNX Runtime for optimized serving"
        ),
        "buzzword": (
            "3D Morphable Model (3DMM) fitting for depth-based liveness verification, "
            "Remote Photoplethysmography (rPPG) - heartbeat detection from face video, "
            "Vision Transformer for domain-generalized anti-spoofing, "
            "Neural Radiance Fields for 3D face reconstruction to detect 2D attacks, "
            "Multimodal fusion (RGB + NIR + depth) for enterprise-grade liveness"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1670",
        "org": "Ministry of Electronics and Information Technology",
        "category": "Software",
        "description": "Develop a functional solution that incorporates the security of the ML model.",
        "tech_stack": (
            "<b>ML Framework:</b> PyTorch / TensorFlow for model development<br/>"
            "<b>Adversarial Defense:</b> ART (Adversarial Robustness Toolbox by IBM), "
            "CleverHans library, adversarial training (PGD-AT), "
            "input validation and preprocessing defenses<br/>"
            "<b>Model Protection:</b> ONNX model encryption, model watermarking (embedding verification triggers), "
            "differential privacy (Opacus for PyTorch), "
            "model obfuscation and weight encryption<br/>"
            "<b>Inference Security:</b> Secure enclave deployment (Intel SGX / ARM TrustZone concepts), "
            "input sanitization pipeline, output confidence thresholding<br/>"
            "<b>Monitoring:</b> Model drift detection (Evidently AI / Alibi Detect), "
            "adversarial input detection (statistical outlier checks), "
            "logging and alerting on suspicious queries<br/>"
            "<b>Backend:</b> Python (FastAPI), Redis for rate limiting<br/>"
            "<b>Frontend:</b> React.js demo dashboard showing attack scenarios and defenses<br/>"
            "<b>Deployment:</b> Docker, model served via TorchServe / TF Serving, API gateway with auth"
        ),
        "buzzword": (
            "Homomorphic Encryption for privacy-preserving ML inference, "
            "Federated Learning for decentralized model training without data sharing, "
            "Zero Trust ML Pipeline with continuous integrity verification, "
            "Secure Multi-Party Computation (MPC) for collaborative model training, "
            "AI-based adversarial attack detection using meta-learning"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1669",
        "org": "Ministry of Electronics and Information Technology",
        "category": "Software",
        "description": "Transformo Docs Application: Empowering Machine-Readable Document Management System.",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript, PDF.js for document viewer<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>OCR:</b> Tesseract OCR, PaddleOCR (for multi-language + layout-aware), "
            "EasyOCR for handwritten text<br/>"
            "<b>Document AI:</b> LayoutLMv3 / DocTR for structure-aware text extraction, "
            "table extraction (Camelot / Tabula), "
            "Apache Tika for multi-format parsing (PDF, DOCX, images, scans)<br/>"
            "<b>NLP:</b> spaCy for NER, text classification, keyword extraction, "
            "auto-tagging with TF-IDF / BERT embeddings<br/>"
            "<b>Output Formats:</b> JSON, XML, CSV, machine-readable PDF (PDF/A), "
            "structured data export via API<br/>"
            "<b>Storage:</b> MinIO / S3 for documents, Elasticsearch for full-text search<br/>"
            "<b>Database:</b> PostgreSQL (metadata, extracted fields)<br/>"
            "<b>Auth:</b> JWT, RBAC, audit logging<br/>"
            "<b>Deployment:</b> Docker, Nginx"
        ),
        "buzzword": (
            "Foundation Document Model (Donut / Nougat by Meta) for end-to-end document understanding, "
            "GPT-4V / Gemini Vision for visual document Q&A, "
            "Knowledge Graph auto-construction from extracted entities, "
            "Blockchain-based document provenance and integrity chain, "
            "Self-supervised pre-training on government document corpus"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1660",
        "org": "Ministry of Earth Sciences",
        "category": "Software",
        "description": "Interactive gamified approach to Ocean Literacy",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, Phaser.js / PixiJS for 2D game engine, "
            "Three.js for 3D ocean visualization<br/>"
            "<b>Backend:</b> Node.js (Express) / Python (FastAPI)<br/>"
            "<b>Database:</b> MongoDB (flexible schema for game data) / PostgreSQL, "
            "Redis (leaderboard, session)<br/>"
            "<b>Gamification:</b> Points, badges, levels, leaderboards, quizzes, "
            "story-driven missions (ocean exploration scenarios), "
            "achievement system<br/>"
            "<b>Content:</b> INCOIS ocean data integration, educational modules, "
            "interactive maps (Leaflet.js), animated infographics (Lottie.js)<br/>"
            "<b>Mobile:</b> PWA (Progressive Web App) or React Native<br/>"
            "<b>Audio/Visual:</b> Howler.js for sound effects, CSS animations, "
            "SVG illustrations, particle effects<br/>"
            "<b>Analytics:</b> User engagement tracking, learning outcome assessment, "
            "Chart.js for educator dashboards<br/>"
            "<b>Auth:</b> Firebase Auth / JWT, social login<br/>"
            "<b>Deployment:</b> Vercel / Netlify (frontend), Docker (backend)"
        ),
        "buzzword": (
            "WebXR-based underwater VR exploration experience, "
            "AI-powered adaptive difficulty (Bayesian Knowledge Tracing), "
            "Procedural ocean environment generation using Wave Function Collapse, "
            "LLM-powered NPC ocean scientists for interactive Q&A, "
            "Metaverse-ready multiplayer ocean exploration"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1657",
        "org": "Ministry of Earth Sciences",
        "category": "Software",
        "description": "Integrated Geo-Referenced Fish Catch Data Repository and Access System",
        "tech_stack": (
            "<b>Frontend:</b> React.js, Leaflet.js / Mapbox GL JS for geo-referenced visualization, "
            "HTML5, CSS3, JavaScript, D3.js for catch analytics<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL + PostGIS (spatial queries on catch locations), "
            "Elasticsearch (search across species, zones, dates)<br/>"
            "<b>Data Ingestion:</b> REST APIs for field data upload, CSV/Excel bulk import, "
            "mobile app (Flutter/React Native) with GPS auto-tagging for fishermen<br/>"
            "<b>GIS:</b> GeoServer for WMS/WFS publishing, QGIS for data preparation, "
            "fishing zone boundary shapefiles, EEZ mapping<br/>"
            "<b>Analytics:</b> pandas, NumPy for catch trend analysis, "
            "species diversity indices, seasonal heatmaps, CPUE calculations<br/>"
            "<b>Reporting:</b> Chart.js, Plotly.js dashboards, ReportLab for PDF reports<br/>"
            "<b>Auth:</b> JWT, RBAC (Admin, Researcher, Fisher, Public), API keys for data access<br/>"
            "<b>Deployment:</b> Docker, Nginx, PostGIS replication"
        ),
        "buzzword": (
            "AI-powered species identification from catch photos (image classification), "
            "Satellite-derived ocean color data (chlorophyll-a) for catch prediction, "
            "Blockchain-based catch certification for traceability, "
            "Digital Twin of fishing zones with real-time vessel tracking (AIS), "
            "LLM-powered natural language query interface for catch data"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1655",
        "org": "Ministry of Earth Sciences",
        "category": "Software",
        "description": "Detecting oil spills at marine environment using Automatic Identification System (AIS) and satellite datasets",
        "tech_stack": (
            "<b>Frontend:</b> React.js, Leaflet.js / Mapbox GL JS, HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (FastAPI / Django)<br/>"
            "<b>Satellite Processing:</b> Google Earth Engine (GEE) API, Sentinel-1 SAR data (dark spot detection), "
            "SNAP (ESA) for SAR preprocessing, GDAL / Rasterio for raster ops<br/>"
            "<b>AIS Data:</b> AIS decoder (pyais library), vessel trajectory analysis, "
            "anomaly detection in vessel behavior (speed changes, route deviations)<br/>"
            "<b>AI/ML:</b> U-Net / DeepLabV3+ for SAR image segmentation (oil vs water), "
            "Random Forest / SVM for feature-based classification (texture, contrast, homogeneity), "
            "correlation model: AIS vessel proximity + SAR dark spots<br/>"
            "<b>GIS:</b> PostGIS for spatial joins (vessel tracks × spill polygons), "
            "GeoPandas, Shapely<br/>"
            "<b>Database:</b> PostgreSQL + PostGIS, TimescaleDB for AIS time-series<br/>"
            "<b>Alerting:</b> Email, SMS, dashboard alerts for detected spills<br/>"
            "<b>Deployment:</b> Docker, GPU server for SAR image inference"
        ),
        "buzzword": (
            "Foundation Models for SAR (PhilEO / SSL4EO) for few-shot oil spill detection, "
            "Multi-temporal SAR change detection using attention mechanisms, "
            "Graph Neural Networks for vessel-spill attribution analysis, "
            "Real-time satellite tasking integration for rapid spill confirmation, "
            "Digital Twin of coastal marine environment"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1654",
        "org": "Ministry of Defence",
        "category": "Software",
        "description": "Determining expert relevance with respect to interview board subject and candidates' area of expertise",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, Material UI<br/>"
            "<b>Backend:</b> Python (Django / FastAPI)<br/>"
            "<b>Database:</b> PostgreSQL (expert profiles, subject taxonomies, board schedules)<br/>"
            "<b>NLP/AI:</b> sentence-transformers for semantic similarity between expert profile and subject, "
            "TF-IDF + cosine similarity as baseline, "
            "spaCy for keyword extraction from CVs/profiles, "
            "BERT/IndicBERT for domain-aware text embeddings<br/>"
            "<b>Matching:</b> Hungarian Algorithm for optimal expert-board assignment, "
            "constraint satisfaction (Google OR-Tools) with availability/conflict constraints<br/>"
            "<b>Knowledge Base:</b> Subject taxonomy tree, expert publication/experience database<br/>"
            "<b>Scoring:</b> Weighted scoring model (experience years, publications, past board performance), "
            "scikit-learn for relevance ranking<br/>"
            "<b>Reporting:</b> Auto-generated panel composition reports (ReportLab)<br/>"
            "<b>Auth:</b> JWT, RBAC, encryption for sensitive data"
        ),
        "buzzword": (
            "Knowledge Graph of expert-subject relationships (Neo4j), "
            "LLM-powered expert profile summarization and gap analysis, "
            "Graph-based collaborative filtering for expert recommendation, "
            "Academic paper embedding (SciBERT/Specter) for research expertise mapping, "
            "Federated expert database across multiple organizations"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1653",
        "org": "Ministry of Defence",
        "category": "Software",
        "description": "Web based Selector-Applicant Simulation Software",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript, "
            "drag-and-drop UI (react-dnd), real-time collaboration (Socket.io)<br/>"
            "<b>Backend:</b> Python (Django / FastAPI) / Node.js (Express), WebSocket server<br/>"
            "<b>Database:</b> PostgreSQL (applicant data, selector criteria, simulation configs)<br/>"
            "<b>Simulation Engine:</b> Monte Carlo simulation (NumPy/SciPy) for outcome modeling, "
            "configurable scoring rubrics, weighted criteria matrix, "
            "multi-round selection process simulation<br/>"
            "<b>Analytics:</b> pandas for data processing, Matplotlib/Plotly for outcome distributions, "
            "statistical tests (chi-square, t-test) for bias detection<br/>"
            "<b>Features:</b> Role-play scenarios, timed assessments, video interview simulation (WebRTC), "
            "automated scoring with manual override<br/>"
            "<b>Reporting:</b> Chart.js dashboards, ReportLab for PDF outcome reports<br/>"
            "<b>Auth:</b> JWT, RBAC (Selector, Applicant, Admin, Observer)<br/>"
            "<b>Deployment:</b> Docker, Nginx, WebSocket-compatible reverse proxy"
        ),
        "buzzword": (
            "AI-powered behavioral analysis from video interviews (emotion + confidence scoring), "
            "Digital Twin of selection process for what-if scenario analysis, "
            "LLM-based auto-evaluation of written responses, "
            "Gamified assessment with adaptive difficulty, "
            "VR-based immersive group task simulation"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1652",
        "org": "Ministry of Defence",
        "category": "Software",
        "description": "Extraction and Verification of Information from semi-categorised data.",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, data table with filters (AG Grid)<br/>"
            "<b>Backend:</b> Python (Django / FastAPI)<br/>"
            "<b>Data Extraction:</b> Apache Tika / PyMuPDF for multi-format parsing, "
            "Tesseract OCR for scanned docs, "
            "regex + rule-based extraction for structured patterns, "
            "spaCy NER for entity extraction (names, dates, locations, IDs)<br/>"
            "<b>Classification:</b> scikit-learn (Naive Bayes, SVM) for category assignment, "
            "BERT/DistilBERT for text classification, "
            "semi-supervised learning (Label Propagation) for partially labeled data<br/>"
            "<b>Verification:</b> Cross-referencing extracted fields against master databases, "
            "consistency checks (date ranges, format validation), "
            "confidence scoring for extracted values<br/>"
            "<b>Database:</b> PostgreSQL, Elasticsearch for search<br/>"
            "<b>Reporting:</b> Discrepancy reports (ReportLab), data quality dashboards (Plotly)<br/>"
            "<b>Auth:</b> JWT, RBAC, audit trail<br/>"
            "<b>Deployment:</b> Docker, Nginx"
        ),
        "buzzword": (
            "LayoutLMv3 for visual document understanding, "
            "Active Learning for efficient labeling of ambiguous categories, "
            "Knowledge Graph for cross-document entity resolution, "
            "LLM-powered data cleaning and normalization, "
            "Automated data lineage tracking for provenance verification"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1646",
        "org": "Ministry of Coal",
        "category": "Software",
        "description": "App based Project monitoring of S&T / R&D Projects of Coal Sector",
        "tech_stack": (
            "<b>Mobile:</b> Flutter / React Native (cross-platform), offline capability<br/>"
            "<b>Frontend Web:</b> React.js, HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL (project data, milestones, budgets), Redis<br/>"
            "<b>Project Management:</b> Gantt chart (Frappe Gantt / dhtmlxGantt), "
            "milestone tracking, fund utilization monitoring, "
            "document upload and versioning (MinIO)<br/>"
            "<b>Analytics:</b> pandas for project performance metrics (SPI, CPI), "
            "Chart.js / Plotly for dashboards, deviation alerts<br/>"
            "<b>Workflow:</b> Multi-level approval workflow (Django-viewflow), "
            "progress report submission and review cycle<br/>"
            "<b>Notifications:</b> Push (FCM), email, SMS for deadline reminders<br/>"
            "<b>Reporting:</b> ReportLab for auto-generated quarterly reports, Excel exports<br/>"
            "<b>Auth:</b> JWT, RBAC (Ministry, PI, Institution, Reviewer)<br/>"
            "<b>Deployment:</b> Docker, Nginx, Play Store / App Store"
        ),
        "buzzword": (
            "AI-powered project delay prediction and risk scoring, "
            "NLP-based automated progress report summarization, "
            "Blockchain-based fund flow tracking for transparency, "
            "Digital Twin of R&D project lifecycle, "
            "LLM-powered Q&A over project documents"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1645",
        "org": "Ministry of Coal",
        "category": "Software",
        "description": "An app and web based software for Productivity and safety management of coal mines.",
        "tech_stack": (
            "<b>Mobile:</b> Flutter / React Native, offline-first architecture<br/>"
            "<b>Frontend Web:</b> React.js, HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL + TimescaleDB (sensor data), Redis<br/>"
            "<b>Safety Module:</b> Incident reporting forms, hazard identification checklists, "
            "DGMS compliance tracking, safety audit scheduling, "
            "near-miss reporting with photo/GPS evidence<br/>"
            "<b>Productivity:</b> OEE (Overall Equipment Effectiveness) calculator, "
            "shift-wise production logging, equipment downtime tracking, "
            "target vs actual dashboards<br/>"
            "<b>IoT Integration:</b> MQTT for real-time sensor data (gas levels, ventilation, ground stability), "
            "alert thresholds for CH4, CO, O2 levels<br/>"
            "<b>Analytics:</b> pandas, scikit-learn for accident pattern analysis, "
            "Chart.js / Plotly dashboards<br/>"
            "<b>Notifications:</b> SOS alerts (SMS, siren trigger), push notifications<br/>"
            "<b>Deployment:</b> Docker, Nginx, edge server for mine sites with poor connectivity"
        ),
        "buzzword": (
            "Computer Vision for PPE compliance detection (helmet, vest, boots), "
            "Predictive safety analytics using historical incident data, "
            "Digital Twin of mine for simulation and planning, "
            "AR-based safety training modules, "
            "Wearable IoT integration for miner health monitoring (heart rate, fatigue)"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1625",
        "org": "Government of NCT of Delhi",
        "category": "Software",
        "description": "Smart Classroom Management Software for Enhanced Learning Environments",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript, Material UI<br/>"
            "<b>Backend:</b> Python (Django / FastAPI) / Node.js (Express)<br/>"
            "<b>Database:</b> PostgreSQL (student/teacher/class data), MongoDB (content), Redis<br/>"
            "<b>Features:</b> Attendance (QR code / face recognition), "
            "digital timetable, assignment submission portal, "
            "live quiz/poll (Socket.io for real-time), "
            "resource sharing (PDF, video, links)<br/>"
            "<b>AI/ML:</b> Engagement detection from webcam (facial landmark analysis - MediaPipe), "
            "attention scoring, personalized content recommendations (collaborative filtering)<br/>"
            "<b>Video:</b> WebRTC for live classes, HLS for recorded content<br/>"
            "<b>Analytics:</b> Student performance dashboards, attendance trends, "
            "learning outcome tracking, Chart.js / Plotly<br/>"
            "<b>Mobile:</b> React Native / Flutter companion app<br/>"
            "<b>Auth:</b> JWT, SSO, RBAC (Admin, Teacher, Student, Parent)<br/>"
            "<b>Deployment:</b> Docker, Nginx"
        ),
        "buzzword": (
            "Adaptive Learning Engine powered by Bayesian Knowledge Tracing, "
            "Emotion AI for real-time student sentiment analysis, "
            "LLM-powered AI teaching assistant for doubt resolution, "
            "AR/VR immersive lab simulations, "
            "Metaverse classroom for remote collaboration"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1624",
        "org": "Government of NCT of Delhi",
        "category": "Software",
        "description": "To develop an Artificial Intelligence (AI) based model for electricity demand projection including peak demand projection for Delhi Power system",
        "tech_stack": (
            "<b>Frontend:</b> React.js, Plotly.js / D3.js for interactive demand curves, "
            "HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (FastAPI / Django), Celery for scheduled forecasting jobs<br/>"
            "<b>Database:</b> PostgreSQL + TimescaleDB (historical load data), Redis<br/>"
            "<b>AI/ML:</b> LSTM / GRU (PyTorch/TensorFlow) for time-series load forecasting, "
            "Prophet (seasonal decomposition), "
            "XGBoost / LightGBM for feature-based prediction, "
            "Temporal Fusion Transformer for multi-horizon forecasting<br/>"
            "<b>Features:</b> Temperature, humidity (IMD API), calendar events, holidays, "
            "historical load curves, socioeconomic indicators<br/>"
            "<b>Peak Detection:</b> Signal processing (SciPy find_peaks), "
            "peak demand confidence intervals, coincidence factor analysis<br/>"
            "<b>Visualization:</b> Load duration curves, peak demand heatmaps, "
            "scenario comparison (normal/hot/extreme days)<br/>"
            "<b>Export:</b> CSV, Excel, PDF reports<br/>"
            "<b>Deployment:</b> Docker, Nginx, GPU for model training"
        ),
        "buzzword": (
            "Transformer-based probabilistic load forecasting with uncertainty quantification, "
            "Physics-informed constraints (power grid topology awareness), "
            "Federated Learning across DISCOMs for collaborative forecasting, "
            "Digital Twin of Delhi power grid, "
            "Reinforcement Learning for demand-side management recommendations"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1623",
        "org": "Government of NCT of Delhi",
        "category": "Software",
        "description": "Real-time monitoring and evaluation software for application received in Fire Department relating to inspections, follow-ups, issue of NOCs",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, Material UI, Kanban board view<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL (applications, inspections, NOCs), Redis (caching)<br/>"
            "<b>Workflow Engine:</b> Django-viewflow / custom state machine for multi-stage application tracking "
            "(Received → Assigned → Inspected → Approved/Rejected → NOC Issued)<br/>"
            "<b>GIS:</b> Leaflet.js / Google Maps API for building location mapping, "
            "PostGIS for spatial queries<br/>"
            "<b>Features:</b> Application form builder, document upload, "
            "inspector assignment and scheduling, "
            "inspection checklist (digital), photo evidence upload, "
            "auto-generated NOC certificate, follow-up task management<br/>"
            "<b>Mobile:</b> React Native / Flutter for field inspectors (offline capable)<br/>"
            "<b>Notifications:</b> SMS, email, push for status updates<br/>"
            "<b>Analytics:</b> Application processing time, inspector workload, "
            "bottleneck identification, Chart.js dashboards<br/>"
            "<b>Auth:</b> JWT, RBAC, digital signature for NOC issuance"
        ),
        "buzzword": (
            "AI-powered risk scoring for priority-based inspection scheduling, "
            "Computer Vision for fire safety compliance detection from uploaded photos, "
            "Blockchain-based tamper-proof NOC certificate verification, "
            "Digital Twin of building fire safety systems, "
            "LLM-powered automated inspection report generation"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1622",
        "org": "Government of NCT of Delhi",
        "category": "Software",
        "description": "Online issuance of Caste and other certificates by Revenue Department need real-time monitoring",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, form wizard UI<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL (applications, citizen data), Redis<br/>"
            "<b>Workflow:</b> Multi-stage approval pipeline (Apply → Verify → Approve → Issue), "
            "SLA timers with auto-escalation, "
            "Django-viewflow / custom state machine<br/>"
            "<b>Document Verification:</b> Tesseract OCR for uploaded document reading, "
            "Aadhaar eKYC API, DigiLocker API for document fetch<br/>"
            "<b>Monitoring:</b> Real-time application status dashboard, "
            "processing time analytics, pending vs completed metrics, "
            "bottleneck identification by office/officer<br/>"
            "<b>Certificate Generation:</b> QR-coded digital certificate (cryptographic hash), "
            "ReportLab for PDF generation, digital signature (DSC/eSign API)<br/>"
            "<b>Mobile:</b> React Native / Flutter for citizen-facing app<br/>"
            "<b>Notifications:</b> SMS, email, WhatsApp Business API<br/>"
            "<b>Auth:</b> Aadhaar-based eKYC, JWT, RBAC"
        ),
        "buzzword": (
            "Blockchain-based verifiable credentials for tamper-proof certificates, "
            "AI-powered document fraud detection, "
            "Chatbot for application status tracking and guidance, "
            "Predictive SLA compliance scoring using historical data, "
            "W3C Verifiable Credentials standard compliance"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1617",
        "org": "Government of NCT of Delhi",
        "category": "Software",
        "description": "Dynamic route rationalization model based on machine learning/AI would be required based on real-time traffic and road parameters.",
        "tech_stack": (
            "<b>Frontend:</b> React.js, Leaflet.js / Mapbox GL JS for route visualization, "
            "HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (FastAPI / Django), Node.js<br/>"
            "<b>Database:</b> PostgreSQL + PostGIS (road network, stops), "
            "Redis (real-time cache), TimescaleDB (traffic time-series)<br/>"
            "<b>Routing:</b> OSRM / Valhalla / GraphHopper for route computation, "
            "OpenStreetMap road network data, "
            "Dijkstra / A* with dynamic edge weights<br/>"
            "<b>AI/ML:</b> XGBoost / LightGBM for travel time prediction, "
            "clustering (DBSCAN) for demand hotspot identification, "
            "genetic algorithm (DEAP) for multi-objective route optimization (cost, time, coverage)<br/>"
            "<b>Traffic Data:</b> Google Maps Directions API (live traffic), "
            "ITMS (Intelligent Traffic Management System) feeds, "
            "GTFS data for existing routes<br/>"
            "<b>Simulation:</b> SUMO (Simulation of Urban Mobility) for route testing<br/>"
            "<b>Analytics:</b> Route efficiency metrics, ridership coverage analysis, "
            "Plotly / D3.js dashboards<br/>"
            "<b>Deployment:</b> Docker, Nginx"
        ),
        "buzzword": (
            "Deep Reinforcement Learning for real-time adaptive routing, "
            "Digital Twin of Delhi transport network, "
            "Multi-Agent Simulation for emergent traffic patterns, "
            "Transformer-based traffic flow prediction, "
            "Quantum-inspired optimization for large-scale vehicle routing problems"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1607",
        "org": "Department of Science and Technology",
        "category": "Software",
        "description": "A smart AI based solution for traffic management on routes with heavy traffic from different directions, with real-time monitoring and adaptation of traffic light timings",
        "tech_stack": (
            "<b>Frontend:</b> React.js, Leaflet.js / Mapbox for junction map, "
            "HTML5, CSS3, JavaScript, D3.js for traffic flow animation<br/>"
            "<b>Backend:</b> Python (FastAPI), Node.js<br/>"
            "<b>Computer Vision:</b> YOLOv8 for vehicle detection and counting from CCTV feeds, "
            "OpenCV for video stream processing, "
            "vehicle classification (car, bus, truck, two-wheeler)<br/>"
            "<b>Traffic Signal Control:</b> Reinforcement Learning (Deep Q-Network / PPO) "
            "for adaptive signal timing optimization, "
            "SUMO simulator for RL training environment, "
            "Webster's formula as baseline<br/>"
            "<b>Communication:</b> RTSP for CCTV feeds, MQTT for signal controller commands, "
            "REST API for integration with traffic management center<br/>"
            "<b>Database:</b> PostgreSQL + TimescaleDB (traffic counts), Redis<br/>"
            "<b>Hardware Integration:</b> Traffic signal controller interface (NTCIP / serial protocol), "
            "Raspberry Pi / Jetson Nano at each junction for edge inference<br/>"
            "<b>Analytics:</b> Congestion index, average wait time, green wave analysis<br/>"
            "<b>Deployment:</b> Docker, edge deployment at intersections"
        ),
        "buzzword": (
            "Multi-Agent Reinforcement Learning (MARL) for coordinated signal control, "
            "V2I (Vehicle-to-Infrastructure) communication via 5G, "
            "Graph Neural Networks for city-wide traffic flow prediction, "
            "Digital Twin of intersections for simulation-based policy testing, "
            "Federated Learning across intersections for privacy-preserving model improvement"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1604",
        "org": "Bharat Electronics Limited (BEL)",
        "category": "Software",
        "description": "Conversational Image Recognition Chatbot",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, drag-and-drop image upload, "
            "chat interface with image preview<br/>"
            "<b>Backend:</b> Python (FastAPI / Flask)<br/>"
            "<b>Vision AI:</b> OpenAI GPT-4V / Google Gemini Vision API / "
            "open-source: LLaVA, InternVL (multimodal LLM), "
            "YOLOv8 for object detection, ResNet/EfficientNet for classification<br/>"
            "<b>NLP:</b> LangChain for conversation management, "
            "RAG for context-aware responses with image metadata, "
            "FAISS / ChromaDB for visual embeddings<br/>"
            "<b>Image Processing:</b> OpenCV, Pillow, CLIP (OpenAI) for image-text matching<br/>"
            "<b>Database:</b> PostgreSQL (conversations), MinIO (image storage), "
            "Redis (session cache)<br/>"
            "<b>Voice:</b> Whisper for speech-to-text, Web Speech API<br/>"
            "<b>Deployment:</b> Docker, GPU server (CUDA), Nginx"
        ),
        "buzzword": (
            "Vision-Language Foundation Model (GPT-4o / Gemini 1.5 Pro), "
            "Visual Grounding - point and ask about specific image regions, "
            "Agentic multimodal reasoning with tool-use, "
            "Real-time video stream understanding with temporal context, "
            "Neural image search across conversation history"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1600",
        "org": "AICTE, MIC- Student Innovation",
        "category": "Software",
        "description": "Student Innovation",
        "tech_stack": (
            "<b>Open-ended — Recommended Base Stack:</b><br/>"
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (FastAPI / Django) or Node.js (Express)<br/>"
            "<b>Database:</b> PostgreSQL / MongoDB, Redis<br/>"
            "<b>AI/ML:</b> scikit-learn, PyTorch / TensorFlow (if AI component needed)<br/>"
            "<b>Mobile:</b> Flutter / React Native (if mobile app required)<br/>"
            "<b>Cloud:</b> AWS / GCP / Azure free tier, Vercel for frontend<br/>"
            "<b>DevOps:</b> Docker, GitHub Actions CI/CD<br/>"
            "<b>Tools:</b> Figma (UI design), Git (version control), Postman (API testing)"
        ),
        "buzzword": (
            "Open-ended — choose buzzwords relevant to your specific innovation: "
            "GenAI, LLM, Blockchain, IoT, AR/VR, Digital Twin, Edge AI, "
            "Quantum Computing, Web3, Metaverse"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1569",
        "org": "Ministry of Jal Shakti",
        "category": "Hardware",
        "description": "Personalized testing kits for testing Residual Chlorine level at delivery points",
        "tech_stack": (
            "<b>Hardware:</b> DPD colorimetric method (DPD reagent tablets/drops), "
            "portable colorimeter (LED 515nm + photodiode), "
            "ESP32/Arduino Nano MCU, OLED display (SSD1306), "
            "3D-printed cuvette holder and enclosure, "
            "amperometric sensor alternative (bare platinum electrodes)<br/>"
            "<b>Optics:</b> TSL2591 lux sensor / OPT3001 for absorbance, Beer-Lambert law calibration<br/>"
            "<b>Mobile App:</b> Flutter / React Native, camera-based color analysis (OpenCV + color space matching), "
            "BLE for data transfer from device<br/>"
            "<b>Backend:</b> Python (FastAPI), PostgreSQL for test result logging, GPS tagging<br/>"
            "<b>Compliance:</b> IS 10500 standards comparison engine, WHO guideline thresholds<br/>"
            "<b>Calibration:</b> Known chlorine standard solutions, polynomial regression (NumPy)<br/>"
            "<b>Reports:</b> Auto-generated compliance PDF reports"
        ),
        "buzzword": (
            "IoT-enabled mesh network of chlorine sensors across water distribution, "
            "AI-based color gradient analysis using transfer learning, "
            "Blockchain-verified water quality certificates, "
            "Electrochemical impedance spectroscopy for advanced chlorine speciation, "
            "Cloud-connected predictive chlorine decay modeling"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1559",
        "org": "Ministry of Electronics and Information Technology",
        "category": "Hardware",
        "description": "Develop a functional solution that demonstrates the hardware enabled root of trust.",
        "tech_stack": (
            "<b>Hardware:</b> TPM 2.0 module (Infineon SLB9670 / STMicroelectronics), "
            "or HSM (Hardware Security Module), "
            "secure microcontroller (STM32L5 with TrustZone / NXP LPC55S69), "
            "Raspberry Pi with TPM HAT for demo<br/>"
            "<b>Secure Boot:</b> U-Boot with verified boot chain, "
            "certificate-based firmware signing (OpenSSL), "
            "hash chain verification at each boot stage<br/>"
            "<b>Software:</b> tpm2-tools (Linux TPM interface), "
            "tpm2-tss (TPM Software Stack), "
            "Python (tpm2-pytss) for scripting TPM operations<br/>"
            "<b>Cryptography:</b> RSA/ECDSA key generation within TPM, "
            "sealed storage (bind data to platform state via PCR), "
            "remote attestation protocol implementation<br/>"
            "<b>Demo Application:</b> Secure key storage, measured boot log viewer, "
            "firmware integrity verification tool<br/>"
            "<b>GUI:</b> PyQt5 / Electron.js for visualization of trust chain<br/>"
            "<b>Documentation:</b> TCG (Trusted Computing Group) specifications reference"
        ),
        "buzzword": (
            "DICE (Device Identifier Composition Engine) for IoT device attestation, "
            "Confidential Computing with Intel SGX / AMD SEV enclaves, "
            "Blockchain-anchored device identity registry, "
            "Post-quantum cryptography integration (CRYSTALS-Kyber), "
            "Formal verification of boot chain using model checking"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1558",
        "org": "Ministry of Culture",
        "category": "Hardware",
        "description": "AI-based automated defective exhibit identification system placed in a gallery.",
        "tech_stack": (
            "<b>Hardware:</b> Raspberry Pi 5 / NVIDIA Jetson Nano, "
            "high-resolution camera (RPi HQ Camera / USB industrial camera), "
            "motorized pan-tilt mount for automated scanning, "
            "LED lighting rig for consistent illumination, "
            "environmental sensors (DHT22 for temp/humidity, LDR for light levels)<br/>"
            "<b>Computer Vision:</b> OpenCV for image preprocessing, "
            "YOLOv8 / Detectron2 for defect detection (cracks, discoloration, chipping), "
            "anomaly detection (Autoencoders) for novel defects, "
            "image stitching for large exhibit panoramas<br/>"
            "<b>ML Framework:</b> PyTorch / TensorFlow, "
            "custom dataset: annotated exhibit defect images, "
            "transfer learning from ImageNet<br/>"
            "<b>Backend:</b> Python (FastAPI), PostgreSQL (defect logs, exhibit registry)<br/>"
            "<b>Dashboard:</b> React.js web dashboard, defect heatmap overlay on exhibit images<br/>"
            "<b>Alerts:</b> Email, SMS, dashboard notification on defect detection<br/>"
            "<b>Deployment:</b> Edge device at gallery, Docker on Jetson"
        ),
        "buzzword": (
            "Multispectral imaging for hidden damage detection (UV, IR), "
            "3D scanning (structured light) for surface deformation analysis, "
            "Vision Transformer for fine-grained defect classification, "
            "Digital Twin of gallery with virtual exhibit condition tracking, "
            "AR-based defect annotation for museum conservators"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1557",
        "org": "Ministry of Coal",
        "category": "Software+Hardware",
        "description": "Development of Tyre Maintenance and Operation App, including fitment of necessary IIoT related hardware in Dumpers",
        "tech_stack": (
            "<b>Hardware:</b> TPMS sensors (tire pressure + temperature), "
            "ESP32/STM32 MCU, CAN bus interface for OBD data, "
            "vibration sensor (ADXL345) for road condition, "
            "GPS module (NEO-6M), 4G/LoRa module for data transmission, "
            "ruggedized enclosure (IP67 for mining environment)<br/>"
            "<b>Mobile App:</b> Flutter / React Native (cross-platform), offline-first<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL + TimescaleDB (sensor time-series), Redis<br/>"
            "<b>IoT:</b> MQTT broker (Mosquitto), REST API for data ingestion<br/>"
            "<b>Analytics:</b> scikit-learn / XGBoost for tire wear prediction, "
            "remaining useful life (RUL) estimation, "
            "TKPH (Tonne Kilometres Per Hour) calculation engine, "
            "pandas, NumPy<br/>"
            "<b>Dashboard:</b> React.js, Chart.js, tire pressure/temp heatmap visualization<br/>"
            "<b>Alerts:</b> Low pressure, overheating, predicted blowout warnings<br/>"
            "<b>Deployment:</b> Docker, edge server at mine site"
        ),
        "buzzword": (
            "Digital Twin of dumper tire with physics-based wear model, "
            "Predictive Maintenance 4.0 with survival analysis, "
            "Computer Vision for visual tire damage assessment, "
            "Blockchain-based tire lifecycle tracking and warranty management, "
            "Federated Learning across mine sites for improved tire life prediction"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1544",
        "org": "Autodesk",
        "category": "Hardware",
        "description": "Students are supposed to use Fusion software to generate NC code with machine details & tool library for any industrial component.",
        "tech_stack": (
            "<b>CAD/CAM:</b> Autodesk Fusion 360 (mandatory - free educational license), "
            "SolidWorks / FreeCAD as supplementary design tools<br/>"
            "<b>CNC Programming:</b> Fusion 360 Manufacturing workspace, "
            "G-code / M-code generation, toolpath strategies (adaptive clearing, "
            "parallel, contour, bore, thread milling)<br/>"
            "<b>Tool Library:</b> Fusion 360 Tool Library (define cutter geometry, feeds, speeds), "
            "HSMAdvisor / Machinist Calculator for feeds/speeds optimization<br/>"
            "<b>Simulation:</b> Fusion 360 built-in toolpath simulation, "
            "collision detection, material removal verification<br/>"
            "<b>Post Processing:</b> Custom post processor (JavaScript-based in Fusion), "
            "machine-specific post (Fanuc, Haas, Siemens, Mazak)<br/>"
            "<b>Materials:</b> Aluminum, steel, titanium — material library with cutting parameters<br/>"
            "<b>Documentation:</b> Technical drawing (Fusion 360 Drawing workspace), "
            "setup sheets, tool lists<br/>"
            "<b>Hardware:</b> 3-axis / 5-axis CNC mill for physical validation (if available)"
        ),
        "buzzword": (
            "AI-powered toolpath optimization (Fusion Generative Design for manufacturing), "
            "Cloud-based multi-axis simulation, "
            "Topology-optimized fixtures via generative design, "
            "Digital Twin of CNC machine for virtual commissioning, "
            "ML-based adaptive feed rate optimization from spindle load data"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1543",
        "org": "Autodesk",
        "category": "Hardware",
        "description": "Research and redesign a conventional aerospace component commonly found in air vehicles and utilize Fusion software to reimagine its design.",
        "tech_stack": (
            "<b>CAD/CAM:</b> Autodesk Fusion 360 (mandatory), Generative Design workspace, "
            "Topology Optimization, Shape Optimization<br/>"
            "<b>Simulation:</b> Fusion 360 Simulation (FEA - static stress, modal, thermal), "
            "Ansys / SimScale (cloud FEA) for advanced validation<br/>"
            "<b>Generative Design:</b> Define preserve/obstacle geometries, load cases, "
            "materials (Al 7075, Ti-6Al-4V, Inconel 718), "
            "manufacturing constraints (additive, CNC, casting)<br/>"
            "<b>Additive Manufacturing:</b> Fusion 360 Additive Build workspace, "
            "support structure generation, build orientation optimization, "
            "SLM/DMLS process parameter awareness<br/>"
            "<b>Materials:</b> Aerospace-grade alloys, composites, "
            "Fusion material library + custom material cards<br/>"
            "<b>Documentation:</b> Technical report, weight reduction analysis, "
            "stress-to-weight ratio comparison (original vs redesigned), "
            "3D PDF export for presentation<br/>"
            "<b>3D Printing:</b> FDM prototype (PLA/ABS), SLA for high-detail, "
            "metal AM (if access available)"
        ),
        "buzzword": (
            "AI-driven generative design with multi-physics constraints, "
            "Lattice structure optimization for weight reduction, "
            "Digital Thread from design to manufacturing, "
            "Multi-material topology optimization, "
            "Biomimicry-inspired structural optimization"
        ),
    },
    {
        "year": "SIH 2024",
        "ps_no": "SIH1540",
        "org": "AICTE, MIC- Student Innovation",
        "category": "Hardware",
        "description": "Student Innovation",
        "tech_stack": (
            "<b>Open-ended — Recommended Base Stack:</b><br/>"
            "<b>Microcontroller:</b> Arduino Uno/Mega, ESP32 (Wi-Fi+BLE), Raspberry Pi<br/>"
            "<b>Sensors:</b> As per project needs (DHT22, ultrasonic, IR, IMU, etc.)<br/>"
            "<b>Communication:</b> Wi-Fi, BLE, LoRa, 4G module as needed<br/>"
            "<b>Firmware:</b> C/C++ (Arduino IDE / PlatformIO), MicroPython<br/>"
            "<b>CAD:</b> Fusion 360 / FreeCAD for enclosure design, 3D printing<br/>"
            "<b>Backend:</b> Python (Flask/FastAPI), Firebase for rapid prototyping<br/>"
            "<b>Dashboard:</b> React.js or Blynk IoT for quick visualization<br/>"
            "<b>PCB:</b> KiCad / EasyEDA for custom PCB design<br/>"
            "<b>Power:</b> LiPo batteries, solar panel, voltage regulators"
        ),
        "buzzword": (
            "Open-ended — choose based on your project: "
            "Edge AI, TinyML, Neuromorphic, Digital Twin, Swarm Robotics, "
            "Soft Robotics, Brain-Computer Interface, Quantum Sensing"
        ),
    },

    # ========================================================================
    # SIH 2023 (36 Statements)
    # ========================================================================
    {
        "year": "SIH 2023",
        "ps_no": "SIH1301",
        "org": "Ministry of power",
        "category": "Software",
        "description": "Language translator tool to convert English to Hindi (official Language) which can be used by all the government organizations websites officially.",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, WYSIWYG editor integration "
            "(TinyMCE/CKEditor with translation plugin)<br/>"
            "<b>Backend:</b> Python (FastAPI / Django), Node.js<br/>"
            "<b>Translation:</b> Bhashini API (Dhruva) for English→Hindi NMT, "
            "IndicTrans2 (AI4Bharat open-source model), "
            "fallback: Google Translate API / Azure Translator<br/>"
            "<b>NLP:</b> spaCy / Stanza for sentence segmentation, "
            "custom glossary for government terminology (domain-specific dictionary), "
            "post-editing interface for human review<br/>"
            "<b>CMS Integration:</b> WordPress plugin / Drupal module / "
            "JavaScript snippet for any website embedding<br/>"
            "<b>Caching:</b> Redis for translation caching (avoid re-translating same phrases)<br/>"
            "<b>Database:</b> PostgreSQL (translation memory, glossary)<br/>"
            "<b>API:</b> RESTful API with API key management for govt org onboarding<br/>"
            "<b>Deployment:</b> Docker, Nginx, NIC Cloud"
        ),
        "buzzword": (
            "Fine-tuned IndicTrans2 on government domain corpus, "
            "Adaptive Neural Machine Translation with user feedback loop, "
            "Transliteration-aware translation for proper nouns, "
            "Browser extension for auto-translation of any govt website, "
            "LLM-powered context-aware translation with document understanding"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1305",
        "org": "Government of Punjab",
        "category": "Software",
        "description": "The Employment Department has a digital platform www.pgrkam.com. Currently, there is no hand-holding mechanism to help the user navigate across multiple modules on the portal/app to search for answers.",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript, chat widget<br/>"
            "<b>Backend:</b> Python (FastAPI / Django), Node.js<br/>"
            "<b>Chatbot/Assistant:</b> LangChain + RAG with platform content as knowledge base, "
            "intent classification (Rasa / Dialogflow / custom BERT classifier), "
            "guided navigation flows (decision tree + NLU hybrid), "
            "Bhashini API for Punjabi + Hindi + English<br/>"
            "<b>Search:</b> Elasticsearch for full-text search across all modules, "
            "semantic search (sentence-transformers + FAISS) for natural language queries<br/>"
            "<b>Personalization:</b> User profile-based recommendations (collaborative filtering), "
            "session history tracking for contextual suggestions<br/>"
            "<b>Database:</b> PostgreSQL (user interactions, preferences), Redis<br/>"
            "<b>Voice:</b> Whisper / Bhashini ASR for voice-based navigation<br/>"
            "<b>Analytics:</b> User journey mapping, drop-off analysis, popular query tracking<br/>"
            "<b>Deployment:</b> Docker, Nginx"
        ),
        "buzzword": (
            "Agentic AI Navigator with multi-step task execution (auto-fill forms, search jobs), "
            "Visual Site Map AI that understands page relationships, "
            "Proactive push notifications based on user profile matching, "
            "LLM-powered career counseling chatbot, "
            "Voice-first interface with Punjabi dialect support"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1312",
        "org": "Ministry of coal",
        "category": "Software",
        "description": "Chatbot to respond to text queries pertaining to various Acts, Rules, and Regulations applicable to Mining industries",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, chat UI<br/>"
            "<b>Backend:</b> Python (FastAPI / Flask)<br/>"
            "<b>NLP/AI:</b> LangChain + RAG, FAISS / ChromaDB, "
            "sentence-transformers for embeddings, "
            "OpenAI / Gemini API / Llama 3 (Ollama) for generation, "
            "Bhashini API for Hindi support<br/>"
            "<b>Knowledge Base:</b> Mines Act 1952, MMDR Act 2015, Coal Mines Regulations 2017, "
            "DGMS circulars — PDF ingestion via PyMuPDF, chunking strategy<br/>"
            "<b>Citation:</b> Source attribution (section, rule, page) in responses<br/>"
            "<b>Database:</b> PostgreSQL (query logs), Redis (sessions)<br/>"
            "<b>Testing:</b> Ground-truth Q&A pairs for evaluation (BLEU, ROUGE, human eval)<br/>"
            "<b>Deployment:</b> Docker, Nginx, Gunicorn"
        ),
        "buzzword": (
            "Legal-domain LLM fine-tuned on Indian mining legislation, "
            "Knowledge Graph of Acts → Sections → Rules → Amendments, "
            "Multi-hop reasoning for complex regulatory queries, "
            "Hallucination detection with confidence scoring, "
            "Auto-updated knowledge base when new circulars are published"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1314",
        "org": "Ministry of coal",
        "category": "Software",
        "description": "Real-time visibility of Dumper load status to Shovel operator",
        "tech_stack": (
            "<b>Frontend:</b> React.js / custom HMI (Human-Machine Interface), "
            "HTML5, CSS3, JavaScript, real-time status indicators<br/>"
            "<b>Backend:</b> Python (FastAPI) / Node.js (Express) with WebSocket<br/>"
            "<b>IoT:</b> Load cell sensors on dumpers, ESP32/STM32 MCU, "
            "GPS modules (NEO-6M) for location, "
            "MQTT broker (Mosquitto) for real-time data streaming<br/>"
            "<b>Communication:</b> LoRaWAN for mine-site communication, "
            "4G/LTE fallback, mesh networking<br/>"
            "<b>Display:</b> Ruggedized tablet/display in shovel cabin, "
            "color-coded dumper status (empty/loading/full/in-transit)<br/>"
            "<b>Database:</b> PostgreSQL + TimescaleDB, InfluxDB alternative<br/>"
            "<b>Analytics:</b> Cycle time analysis, payload optimization, "
            "queue time at shovel, pandas + Chart.js<br/>"
            "<b>Alerts:</b> Overloading warning, proximity alerts<br/>"
            "<b>Deployment:</b> Edge server at mine site, Docker"
        ),
        "buzzword": (
            "Digital Twin of mine fleet for simulation-based dispatch optimization, "
            "Computer Vision for payload estimation from dumper body imaging, "
            "V2V (Vehicle-to-Vehicle) mesh communication, "
            "AI-based dynamic fleet dispatch optimization, "
            "AR HUD overlay for shovel operator showing dumper status"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1317",
        "org": "Ministry of coal",
        "category": "Software",
        "description": "Development of a Digital Platform for multi-modal visibility of coal transportation",
        "tech_stack": (
            "<b>Frontend:</b> React.js, Leaflet.js / Mapbox for multi-modal route visualization, "
            "HTML5, CSS3, JavaScript, D3.js for Sankey diagrams<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL + PostGIS (routes, terminals), "
            "TimescaleDB (time-series tracking data)<br/>"
            "<b>Data Integration:</b> Railway tracking (FOIS API), "
            "road transport (GPS tracker APIs), "
            "port/shipping data (vessel AIS data - MarineTraffic API), "
            "belt conveyor telemetry, "
            "manual entry for rail rake placement<br/>"
            "<b>GIS:</b> Route mapping (road, rail, waterway), terminal/depot locations, "
            "GeoPandas, PostGIS spatial queries<br/>"
            "<b>Analytics:</b> Transit time analysis, mode-wise throughput, "
            "bottleneck identification, pandas, Plotly dashboards<br/>"
            "<b>Notifications:</b> Delay alerts, ETA updates (SMS, email, push)<br/>"
            "<b>Auth:</b> JWT, RBAC (Ministry, Company, Transporter, Terminal)<br/>"
            "<b>Deployment:</b> Docker, Nginx, message queue (RabbitMQ/Kafka) for high-throughput data"
        ),
        "buzzword": (
            "Supply Chain Digital Twin for end-to-end coal logistics simulation, "
            "AI-based ETA prediction using multi-modal transit data, "
            "Blockchain-based consignment tracking for tamper-proof coal movement records, "
            "Satellite imagery for coal stockpile volume estimation, "
            "Graph-based optimal mode selection engine"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1319",
        "org": "Ministry of coal",
        "category": "Software",
        "description": "Forecasting and scheduling of railway rakes.",
        "tech_stack": (
            "<b>Frontend:</b> React.js, FullCalendar.js / Gantt chart for schedule visualization, "
            "HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (Django / FastAPI)<br/>"
            "<b>Database:</b> PostgreSQL (rake inventory, route data, demand), "
            "TimescaleDB (historical rake movement time-series)<br/>"
            "<b>Forecasting:</b> ARIMA / SARIMA, Prophet for seasonal demand, "
            "LSTM (PyTorch/TensorFlow) for complex temporal patterns, "
            "XGBoost for feature-based forecasting (production schedule, stock levels, weather)<br/>"
            "<b>Scheduling:</b> Google OR-Tools (job shop scheduling, constraint programming), "
            "PuLP for LP/ILP, "
            "genetic algorithm (DEAP) for multi-objective rake allocation<br/>"
            "<b>Data:</b> FOIS (Freight Operations Information System) integration, "
            "coal production forecasts, port/siding capacity constraints<br/>"
            "<b>Reporting:</b> Rake utilization metrics, turnaround time analysis, "
            "Chart.js / Plotly dashboards, PDF reports<br/>"
            "<b>Deployment:</b> Docker, Nginx"
        ),
        "buzzword": (
            "Deep Reinforcement Learning for dynamic rake rescheduling, "
            "Digital Twin of rail freight network, "
            "Quantum-inspired optimization for NP-hard scheduling, "
            "Multi-Agent System for decentralized rake coordination, "
            "Real-time disruption management using event-driven AI"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1321",
        "org": "Ministry of Chemicals and Fertilizers",
        "category": "Software",
        "description": "Compilation and Collection of optimum Level (variable) of data set from the Chemical and Petrochemical Industries in the country.",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Angular, HTML5, CSS3, JavaScript, "
            "data table with advanced filters (AG Grid), form builder<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL (structured industry data), "
            "Elasticsearch (search and discovery), MongoDB (semi-structured submissions)<br/>"
            "<b>Data Collection:</b> Dynamic form builder (react-jsonschema-form), "
            "Excel/CSV bulk upload (pandas + openpyxl), "
            "API-based data submission for automated systems<br/>"
            "<b>Data Quality:</b> pandas-profiling (ydata-profiling) for automated data quality reports, "
            "Great Expectations for data validation rules, "
            "fuzzy deduplication (RapidFuzz)<br/>"
            "<b>Analytics:</b> pandas, NumPy, Plotly / D3.js for industry dashboards, "
            "trend analysis, state-wise comparison<br/>"
            "<b>Reporting:</b> ReportLab, openpyxl for Excel exports, "
            "scheduled report generation (Celery)<br/>"
            "<b>Auth:</b> JWT, RBAC (Ministry, Industry, Analyst), API key management<br/>"
            "<b>Deployment:</b> Docker, Nginx"
        ),
        "buzzword": (
            "AI-powered data imputation for missing values, "
            "NLP-based automated variable identification from unstructured reports, "
            "Knowledge Graph of chemical industry value chains, "
            "Federated data collection preserving industry data privacy, "
            "LLM-powered natural language analytics query interface"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1329",
        "org": "Ministry of Information and Broadcasting",
        "category": "Software",
        "description": "360-degree feedback software for the Government of India related News Stories in Regional Media using AI/ML",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript, D3.js for analytics<br/>"
            "<b>Backend:</b> Python (Django / FastAPI)<br/>"
            "<b>Data Collection:</b> Web scraping (Scrapy / BeautifulSoup) for regional news portals, "
            "RSS feed aggregation, social media APIs (Twitter/X, Facebook Graph API), "
            "YouTube Data API for video news<br/>"
            "<b>NLP:</b> Multilingual NER (spaCy + Stanza) for entity extraction, "
            "sentiment analysis (IndicBERT / multilingual-BERT), "
            "topic modeling (LDA / BERTopic), "
            "text summarization (mT5 / IndicBART)<br/>"
            "<b>Translation:</b> Bhashini API / IndicTrans2 for 13 regional languages → English<br/>"
            "<b>Database:</b> PostgreSQL (articles, sentiment scores), Elasticsearch (search)<br/>"
            "<b>Analytics:</b> Sentiment trend over time, topic clusters, "
            "regional coverage heatmap, media outlet bias scoring<br/>"
            "<b>Reporting:</b> Auto-generated daily/weekly media perception reports (ReportLab)<br/>"
            "<b>Deployment:</b> Docker, Nginx, Celery for scheduled crawling"
        ),
        "buzzword": (
            "LLM-powered media narrative analysis and framing detection, "
            "Misinformation/fake news detection using claim verification models, "
            "Real-time media monitoring with streaming NLP pipeline (Apache Kafka), "
            "Multimodal analysis (image + text) of news stories, "
            "AI-generated counter-narrative suggestions"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1330",
        "org": "Ministry of Information and Broadcasting",
        "category": "Software",
        "description": "Text to Video of various PIB Press Releases using AI/ML/GANs in English and 13 Regional Languages.",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, video player (Video.js)<br/>"
            "<b>Backend:</b> Python (FastAPI / Django), Celery for async video generation<br/>"
            "<b>Text Processing:</b> NLP pipeline: summarization (T5/BART), "
            "key point extraction, script generation from press release<br/>"
            "<b>Translation:</b> Bhashini API / IndicTrans2 for 13 regional languages<br/>"
            "<b>Text-to-Speech:</b> Bhashini TTS / Google TTS / Coqui TTS for multilingual voice, "
            "SSML for intonation control<br/>"
            "<b>Video Generation:</b> FFmpeg for video composition, "
            "MoviePy for programmatic video editing, "
            "Remotion (React-based video) for template-based generation, "
            "stock footage/image overlay with Ken Burns effect<br/>"
            "<b>Avatars:</b> D-ID / SadTalker for talking-head avatar from text<br/>"
            "<b>Storage:</b> MinIO / S3 for video storage, CDN for delivery<br/>"
            "<b>Database:</b> PostgreSQL (press releases, generated videos)<br/>"
            "<b>Deployment:</b> Docker, GPU server for avatar/video generation"
        ),
        "buzzword": (
            "Diffusion-based video generation (Sora / Runway Gen-3), "
            "Neural Avatar with real-time lip sync and emotion, "
            "Generative Adversarial Networks for photorealistic scene generation, "
            "Voice cloning for consistent narrator across languages, "
            "Real-time text-to-video pipeline with streaming output"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1333",
        "org": "Ministry of Social Justice and Empowerment",
        "category": "Software",
        "description": "Udyog Saarthi App - (Progressive Web-based Application) for Adults undergoing Job coaching for opportunities under 4% reservation in NIEPMD and other Institutions.",
        "tech_stack": (
            "<b>Frontend:</b> React.js (PWA - service workers, manifest.json), "
            "HTML5, CSS3, JavaScript, responsive design, accessibility (WCAG 2.1 AA)<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL (user profiles, job listings, coaching logs), Redis<br/>"
            "<b>Features:</b> Job search and matching, coaching session scheduling, "
            "skill assessment quizzes, progress tracking, "
            "resume builder, employer portal for posting opportunities<br/>"
            "<b>Accessibility:</b> Screen reader support (ARIA labels), high contrast mode, "
            "text-to-speech integration, adjustable font sizes, keyboard navigation, "
            "sign language video support<br/>"
            "<b>Matching:</b> TF-IDF / sentence-transformers for skill-job matching, "
            "collaborative filtering for job recommendations<br/>"
            "<b>Notifications:</b> Push (service worker), SMS, email<br/>"
            "<b>Offline:</b> PWA with offline caching (Workbox)<br/>"
            "<b>Auth:</b> JWT, Aadhaar-based verification option<br/>"
            "<b>Deployment:</b> Vercel / Netlify (frontend), Docker (backend)"
        ),
        "buzzword": (
            "AI-powered personalized career path recommendation, "
            "NLP-based resume optimization for job descriptions, "
            "VR-based job simulation for experiential coaching, "
            "LLM chatbot for 24/7 career guidance, "
            "Predictive placement scoring using ML"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1348",
        "org": "Ministry of Railways",
        "category": "Software",
        "description": "Natural language translation engine for announcements and information dissemination at stations",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, admin panel for announcement management<br/>"
            "<b>Backend:</b> Python (FastAPI / Django)<br/>"
            "<b>Translation:</b> Bhashini API (Dhruva) for real-time NMT, "
            "IndicTrans2 (AI4Bharat) for offline/self-hosted translation, "
            "language detection (langdetect / fastText lid model)<br/>"
            "<b>Text-to-Speech:</b> Bhashini TTS / Google TTS / Coqui TTS for 22+ Indian languages, "
            "SSML for pronunciation and pace control<br/>"
            "<b>Speech-to-Text:</b> Whisper / Bhashini ASR for voice-based announcement input<br/>"
            "<b>Template Engine:</b> Pre-built announcement templates (train arrival/departure, delay, platform change) "
            "with variable slots, auto-translation of templates<br/>"
            "<b>Output:</b> Audio playback system (PA system integration via audio output), "
            "LED/LCD display text feed, mobile app notification<br/>"
            "<b>Database:</b> PostgreSQL (templates, translation memory), Redis (cache)<br/>"
            "<b>Deployment:</b> Docker, edge server at station, Nginx"
        ),
        "buzzword": (
            "Zero-shot cross-lingual transfer for unseen language pairs, "
            "Neural voice cloning for station-specific announcer voice, "
            "Streaming NMT for real-time simultaneous translation, "
            "Emotion-appropriate TTS for emergency vs routine announcements, "
            "Lip-sync video avatar for visual announcement displays"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1349",
        "org": "Ministry of Railways",
        "category": "Software",
        "description": "Using existing CCTV network for crowd management, crime prevention, and work monitoring using AI/ML",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, video grid dashboard<br/>"
            "<b>Backend:</b> Python (FastAPI / Django), Node.js<br/>"
            "<b>Video Processing:</b> OpenCV, FFmpeg, GStreamer, RTSP stream handling<br/>"
            "<b>Computer Vision:</b> YOLOv8 for person/object detection, "
            "DeepSORT / ByteTrack for multi-object tracking, "
            "crowd density estimation (CSRNet / MCNN), "
            "pose estimation (MediaPipe / OpenPose) for suspicious activity detection<br/>"
            "<b>Crime Prevention:</b> Anomaly detection (autoencoders on normal behavior patterns), "
            "abandoned object detection, loitering detection (dwell time thresholds), "
            "face recognition (ArcFace / FaceNet) for watchlist matching<br/>"
            "<b>Work Monitoring:</b> Zone-based personnel presence tracking, "
            "activity classification (cleaning, maintenance, idle)<br/>"
            "<b>Database:</b> PostgreSQL, TimescaleDB (event logs), MinIO (video clips)<br/>"
            "<b>Alerts:</b> Real-time notifications (WebSocket), SMS, siren trigger<br/>"
            "<b>Hardware:</b> NVIDIA Jetson Orin / GPU server for edge inference<br/>"
            "<b>Deployment:</b> Docker, Kubernetes for scale, CUDA"
        ),
        "buzzword": (
            "Vision Transformer for action recognition, "
            "Graph Neural Network for social group behavior analysis, "
            "Federated Learning across stations for privacy-preserving model improvement, "
            "Generative AI for synthetic training data (rare crime scenarios), "
            "Explainable AI for evidence-grade incident reporting"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1350",
        "org": "Government of Jammu and Kashmir",
        "category": "Software",
        "description": "Artificial Intelligence Driven Digitization of Cadastral Maps",
        "tech_stack": (
            "<b>Frontend:</b> React.js, Leaflet.js / OpenLayers for map display, "
            "HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (Django / FastAPI)<br/>"
            "<b>Image Processing:</b> OpenCV (binarization, deskewing, noise removal), "
            "Pillow for image manipulation, "
            "high-resolution scanning (600+ DPI recommended)<br/>"
            "<b>AI/ML:</b> U-Net / Mask R-CNN for parcel boundary segmentation, "
            "Tesseract / PaddleOCR for text extraction from maps (parcel numbers, names), "
            "YOLOv8 for symbol detection (landmarks, markers)<br/>"
            "<b>GIS:</b> GDAL for georeferencing (affine transformation, GCP-based rubber sheeting), "
            "PostGIS for vector parcel storage, "
            "GeoJSON / Shapefile export, coordinate transformation (pyproj)<br/>"
            "<b>Validation:</b> Topology checks (no gaps/overlaps), "
            "area comparison with revenue records<br/>"
            "<b>Database:</b> PostgreSQL + PostGIS<br/>"
            "<b>Deployment:</b> Docker, GPU server for segmentation inference"
        ),
        "buzzword": (
            "Foundation Models (SAM - Segment Anything) for zero-shot parcel boundary detection, "
            "GAN-based image enhancement for degraded old maps, "
            "Graph Neural Networks for parcel topology inference, "
            "Blockchain-based land record immutability, "
            "3D cadastre using LiDAR point cloud integration"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1351",
        "org": "Government of Jammu and Kashmir",
        "category": "Software",
        "description": "Digital Generator Monitoring - Diesel generators are widely used as backup power sources in industries, homes, and remote locations",
        "tech_stack": (
            "<b>IoT Hardware:</b> ESP32 / Arduino Mega MCU, "
            "current sensor (ACS712/SCT-013), voltage sensor (ZMPT101B), "
            "fuel level sensor (ultrasonic / float), RPM sensor (hall effect), "
            "temperature sensor (DS18B20 / thermocouple), "
            "vibration sensor (ADXL345), GPS module<br/>"
            "<b>Communication:</b> MQTT (Mosquitto broker), Wi-Fi/4G module<br/>"
            "<b>Frontend:</b> React.js, Chart.js / Grafana for real-time dashboards<br/>"
            "<b>Backend:</b> Python (FastAPI / Django), Node.js<br/>"
            "<b>Database:</b> PostgreSQL + TimescaleDB / InfluxDB<br/>"
            "<b>Analytics:</b> Fuel consumption rate calculation, efficiency metrics, "
            "runtime tracking, maintenance scheduling, "
            "anomaly detection (scikit-learn - Isolation Forest)<br/>"
            "<b>Alerts:</b> Overheating, low fuel, overload, maintenance due (SMS, email, push)<br/>"
            "<b>Mobile:</b> Flutter / React Native companion app<br/>"
            "<b>Deployment:</b> Edge server + cloud sync, Docker"
        ),
        "buzzword": (
            "Predictive Maintenance using remaining useful life (RUL) estimation, "
            "Digital Twin of generator for simulation and optimization, "
            "AI-based fuel theft detection from consumption anomalies, "
            "Federated Learning across generator fleet for improved models, "
            "Carbon footprint tracking and emission estimation"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1359",
        "org": "Ministry of Commerce and Industries",
        "category": "Software",
        "description": "Contact center knowledge management tool with decision tree",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Angular, HTML5, CSS3, JavaScript, "
            "decision tree visualizer (D3.js / react-decision-tree), "
            "rich text editor for knowledge articles<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL (knowledge articles, decision trees), "
            "Elasticsearch (full-text search across articles)<br/>"
            "<b>Decision Tree Builder:</b> Drag-and-drop tree builder UI (react-flow / GoJS), "
            "conditional logic engine (if-then-else with nested conditions), "
            "multi-path branching with endpoint resolutions<br/>"
            "<b>Knowledge Base:</b> Article CRUD with versioning, "
            "categorization and tagging, "
            "FAQ management, media embedding (images, PDFs)<br/>"
            "<b>Search:</b> Elasticsearch full-text + semantic search (sentence-transformers + FAISS)<br/>"
            "<b>Analytics:</b> Article usage metrics, decision tree path analysis, "
            "agent performance tracking, Chart.js dashboards<br/>"
            "<b>Auth:</b> JWT, RBAC (Admin, Supervisor, Agent)<br/>"
            "<b>Deployment:</b> Docker, Nginx"
        ),
        "buzzword": (
            "LLM-powered auto-answer suggestion from knowledge base, "
            "AI-generated decision trees from historical ticket resolution data, "
            "Conversational AI copilot for contact center agents, "
            "Sentiment analysis for call quality monitoring, "
            "Auto-updated knowledge base using NLP on resolved tickets"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1360",
        "org": "Ministry of Commerce and Industries",
        "category": "Software",
        "description": "Price comparison of GeM products with other e-marketplaces",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, "
            "comparison table UI, price chart (Chart.js / Plotly)<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Web Scraping:</b> Scrapy / Playwright / Selenium for Amazon, Flipkart, IndiaMart, "
            "GeM API (if available) for product catalog, "
            "rotating proxies, CAPTCHA handling<br/>"
            "<b>Product Matching:</b> TF-IDF + cosine similarity for product title matching, "
            "sentence-transformers for semantic matching, "
            "fuzzy matching (RapidFuzz) for brand/model normalization<br/>"
            "<b>Data Pipeline:</b> Apache Airflow / Celery for scheduled scraping jobs, "
            "pandas for data cleaning and normalization<br/>"
            "<b>Database:</b> PostgreSQL (product catalog, price history), "
            "Elasticsearch (product search)<br/>"
            "<b>Analytics:</b> Price trend analysis, average markup calculation, "
            "best-value ranking, category-wise comparison<br/>"
            "<b>Reporting:</b> Auto-generated comparison reports (ReportLab), Excel exports<br/>"
            "<b>Deployment:</b> Docker, Nginx, Celery workers"
        ),
        "buzzword": (
            "LLM-powered product attribute extraction from unstructured listings, "
            "CLIP-based visual product matching (image similarity), "
            "Real-time price monitoring with webhook alerts, "
            "AI-powered negotiation recommendation engine, "
            "Blockchain-based transparent price benchmarking"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1370",
        "org": "Government of Jharkhand",
        "category": "Software",
        "description": "Real time monitoring of infrastructure development",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, "
            "Leaflet.js / Mapbox for project location map, "
            "Gantt chart (dhtmlxGantt) for timeline view<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL + PostGIS (project locations), Redis<br/>"
            "<b>Features:</b> Project registration, milestone tracking, "
            "fund utilization monitoring, contractor management, "
            "geo-tagged photo/video progress upload, "
            "work order and bill management<br/>"
            "<b>Mobile:</b> Flutter / React Native for field engineers (offline + GPS auto-tag)<br/>"
            "<b>Computer Vision:</b> Image-based progress estimation (optional - CNN classifier for construction stage), "
            "before/after image comparison<br/>"
            "<b>Analytics:</b> Project health dashboard (SPI, CPI, delay analysis), "
            "district-wise progress heatmap, Chart.js / Plotly<br/>"
            "<b>Reporting:</b> Auto-generated progress reports (ReportLab), Excel exports<br/>"
            "<b>Notifications:</b> Deadline reminders, delay alerts (SMS, email, push)<br/>"
            "<b>Auth:</b> JWT, RBAC (State, District, Block, Contractor)<br/>"
            "<b>Deployment:</b> Docker, Nginx"
        ),
        "buzzword": (
            "Drone/satellite imagery-based progress verification, "
            "AI-powered delay prediction and risk scoring, "
            "Blockchain-based fund flow tracking, "
            "Digital Twin of infrastructure project, "
            "BIM (Building Information Modeling) integration for planned vs actual"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1377",
        "org": "Ministry of Power",
        "category": "Software",
        "description": "Creation of Live Digital Twins for power Projects and integration with all existing monitoring and database system for holistic real-time approach to construction, operation and maintenance.",
        "tech_stack": (
            "<b>Frontend:</b> React.js, Three.js / Cesium.js for 3D visualization, "
            "D3.js / Plotly for real-time charts, HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (FastAPI / Django), Node.js, WebSocket for real-time updates<br/>"
            "<b>3D/BIM:</b> IFC.js for BIM model rendering in browser, "
            "Revit/AutoCAD export to IFC format, "
            "Three.js for interactive 3D plant visualization<br/>"
            "<b>IoT Integration:</b> MQTT broker (Mosquitto), OPC-UA for SCADA/DCS data, "
            "Modbus TCP for legacy equipment<br/>"
            "<b>Database:</b> PostgreSQL (project data), TimescaleDB / InfluxDB (time-series sensor data), "
            "Redis (real-time cache)<br/>"
            "<b>Data Integration:</b> Apache Kafka for streaming data pipeline, "
            "ETL from existing monitoring systems (PI Historian, SCADA)<br/>"
            "<b>Analytics:</b> Predictive maintenance (scikit-learn, XGBoost), "
            "anomaly detection on sensor streams, "
            "KPI dashboards (availability, heat rate, PLF)<br/>"
            "<b>Simulation:</b> MATLAB/Simulink for plant process simulation, "
            "Python (SciPy) for simplified thermal models<br/>"
            "<b>Deployment:</b> Docker, Kubernetes, GPU for 3D rendering"
        ),
        "buzzword": (
            "Physics-Informed Neural Networks for real-time process prediction, "
            "Extended Reality (XR) with HoloLens for immersive plant inspection, "
            "Autonomous AI agents for self-healing plant operations, "
            "Blockchain-based equipment lifecycle tracking, "
            "Generative AI for automated maintenance procedure generation"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1391",
        "org": "Ministry of Environment",
        "category": "Software",
        "description": "Behavioural change monitoring software",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js (PWA), HTML5, CSS3, JavaScript, "
            "gamification UI (progress bars, badges, streaks)<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL (user activities, surveys), MongoDB (flexible behavior logs), Redis<br/>"
            "<b>Features:</b> Behavior tracking forms (daily habits, consumption patterns), "
            "survey builder (react-jsonschema-form), "
            "pledge/commitment system, community challenges, "
            "reward points system<br/>"
            "<b>Analytics:</b> Behavior change metrics (pre/post intervention), "
            "cohort analysis, trend visualization (Chart.js / Plotly), "
            "statistical significance testing (SciPy)<br/>"
            "<b>AI/ML:</b> Clustering (k-means) for behavioral segments, "
            "recommendation engine for personalized eco-tips, "
            "sentiment analysis on user feedback<br/>"
            "<b>Mobile:</b> PWA or React Native for daily logging<br/>"
            "<b>Notifications:</b> Push reminders, streak maintenance alerts<br/>"
            "<b>Auth:</b> JWT, social login, anonymous mode option<br/>"
            "<b>Deployment:</b> Docker, Nginx"
        ),
        "buzzword": (
            "Nudge AI for behavioral economics-based intervention optimization, "
            "LLM-powered personalized coaching messages, "
            "Social Network Analysis for behavior diffusion modeling, "
            "Digital Twin of community environmental footprint, "
            "Gamified carbon credit system with token rewards"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1392",
        "org": "Ministry of Environment",
        "category": "Software",
        "description": "E-Waste Facility Locator",
        "tech_stack": (
            "<b>Frontend:</b> React.js, Leaflet.js / Google Maps API for facility map, "
            "HTML5, CSS3, JavaScript, responsive mobile-first design<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL + PostGIS (facility locations, service areas)<br/>"
            "<b>GIS:</b> PostGIS spatial queries (nearest facility), "
            "driving distance/time (OSRM / Google Directions API), "
            "service area polygons (isochrone maps)<br/>"
            "<b>Data:</b> CPCB authorized recycler list, state pollution board data, "
            "user-contributed facility additions with admin verification<br/>"
            "<b>Features:</b> Search by location/pincode, filter by e-waste category, "
            "pickup request booking, facility details (contact, accepted items, hours), "
            "e-waste category guide (what goes where)<br/>"
            "<b>Mobile:</b> PWA or React Native<br/>"
            "<b>Notifications:</b> Pickup confirmation, collection drive alerts<br/>"
            "<b>Auth:</b> JWT (optional - for pickup booking), guest access for search<br/>"
            "<b>Deployment:</b> Docker, Nginx, Vercel for frontend"
        ),
        "buzzword": (
            "AI-based e-waste volume estimation from user-uploaded photos, "
            "Route optimization for collection vehicle dispatch, "
            "Blockchain-based e-waste recycling certificate verification, "
            "Gamified recycling rewards with carbon credit integration, "
            "Chatbot for e-waste disposal guidance"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1393",
        "org": "Ministry of Environment",
        "category": "Software",
        "description": "Water and Electricity Tracking App",
        "tech_stack": (
            "<b>Frontend:</b> React.js (PWA) / React Native, HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL (user consumption data, billing), Redis<br/>"
            "<b>Features:</b> Manual entry of meter readings (water + electricity), "
            "photo OCR of meter reading (Tesseract / PaddleOCR), "
            "bill upload and parsing, consumption trend charts (Chart.js), "
            "daily/weekly/monthly comparison, budget alerts, "
            "tips for reduction<br/>"
            "<b>Analytics:</b> Per-unit cost calculation, anomaly detection (unusual spikes), "
            "peer comparison (similar household size/area), "
            "carbon footprint estimation from electricity consumption<br/>"
            "<b>Gamification:</b> Conservation challenges, badges, community leaderboard<br/>"
            "<b>IoT (optional):</b> Smart meter integration via API, "
            "MQTT for real-time consumption data<br/>"
            "<b>Notifications:</b> Budget alerts, unusual consumption warnings (push, SMS)<br/>"
            "<b>Auth:</b> JWT, Firebase Auth<br/>"
            "<b>Deployment:</b> Docker, Nginx, Play Store / PWA"
        ),
        "buzzword": (
            "AI-powered consumption forecasting and bill prediction, "
            "Smart meter IoT integration for real-time tracking, "
            "Blockchain-based verifiable consumption reduction credits, "
            "LLM-powered energy saving recommendations, "
            "Digital Twin of household utility consumption"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1407",
        "org": "Ministry of Home Affairs",
        "category": "Software",
        "description": "Chatbot based helpdesk for govt employees and departments",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, embeddable chat widget<br/>"
            "<b>Backend:</b> Python (FastAPI / Flask), Node.js<br/>"
            "<b>NLP/AI:</b> LangChain + RAG (FAISS/ChromaDB), "
            "intent classification (BERT / custom classifier), "
            "entity extraction (spaCy), "
            "fallback to human agent routing<br/>"
            "<b>Knowledge Base:</b> HR policies, leave rules, IT support FAQs, "
            "department-specific SOPs, form downloads, "
            "document ingestion pipeline (PDF, DOCX)<br/>"
            "<b>Ticketing:</b> Integrated ticketing system for unresolved queries, "
            "ticket status tracking, SLA management<br/>"
            "<b>Database:</b> PostgreSQL (tickets, conversations), Redis (sessions), "
            "vector DB (ChromaDB/FAISS)<br/>"
            "<b>Analytics:</b> Query analytics, resolution rate, popular topics, "
            "agent workload distribution<br/>"
            "<b>Auth:</b> LDAP/AD integration for govt network SSO, JWT<br/>"
            "<b>Deployment:</b> Docker, NIC Cloud, Nginx"
        ),
        "buzzword": (
            "Agentic RAG with tool-use (auto-check leave balance, file IT ticket), "
            "Voice-enabled helpdesk with Whisper + TTS, "
            "Multi-lingual support with Bhashini, "
            "Self-learning chatbot with continuous fine-tuning on resolved tickets, "
            "Emotion-aware response escalation"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1410",
        "org": "Ministry of Home Affairs",
        "category": "Software",
        "description": "Augmented/ Virtual reality system for the live training of troops",
        "tech_stack": (
            "<b>Engine:</b> Unity 3D (C#) or Unreal Engine (C++) — primary development platform<br/>"
            "<b>AR:</b> ARCore (Android) / ARKit (iOS), Vuforia for marker-based AR, "
            "Microsoft Mixed Reality Toolkit (MRTK) for HoloLens<br/>"
            "<b>VR:</b> Oculus SDK / SteamVR / OpenXR for cross-platform VR, "
            "hand tracking (Oculus Quest hand tracking / Ultraleap)<br/>"
            "<b>3D Modeling:</b> Blender for environment and equipment models, "
            "terrain generation (World Machine / Gaia), "
            "military equipment 3D assets<br/>"
            "<b>Simulation:</b> Physics engine (Unity Physics / PhysX), "
            "AI-driven enemy behavior (behavior trees / NavMesh AI), "
            "ballistics simulation, terrain navigation<br/>"
            "<b>Networking:</b> Photon PUN / Mirror (Unity multiplayer) for multi-user training<br/>"
            "<b>Backend:</b> Node.js / Python for session management, analytics<br/>"
            "<b>Database:</b> PostgreSQL (training records, scores), Firebase<br/>"
            "<b>Hardware:</b> Meta Quest 3 / HTC Vive Pro 2, "
            "HoloLens 2 for AR scenarios<br/>"
            "<b>Analytics:</b> Performance scoring, decision-making assessment, after-action review"
        ),
        "buzzword": (
            "Procedural Content Generation for infinite scenario variation, "
            "AI-driven adaptive difficulty based on trainee performance, "
            "Haptic feedback integration for realistic weapon handling, "
            "Digital Twin of real terrain from satellite/drone imagery, "
            "Brain-Computer Interface for cognitive load monitoring during training"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1415",
        "org": "Ministry of Defence",
        "category": "Software",
        "description": "Development of motion amplification video techniques for vibration analysis",
        "tech_stack": (
            "<b>Video Processing:</b> OpenCV, FFmpeg for video I/O, "
            "Python (NumPy, SciPy) for signal processing<br/>"
            "<b>Motion Amplification:</b> Eulerian Video Magnification (EVM) algorithm implementation, "
            "phase-based motion amplification (complex steerable pyramid), "
            "Riesz pyramid for real-time processing<br/>"
            "<b>Signal Analysis:</b> FFT for frequency extraction from amplified motion, "
            "spectrogram generation, modal analysis (frequency, damping ratio), "
            "SciPy signal processing (butter, filtfilt for bandpass filtering)<br/>"
            "<b>AI/ML:</b> PyTorch (optional) - deep learning-based motion magnification "
            "(Learning-based Video Motion Magnification), "
            "anomaly detection on extracted vibration signatures<br/>"
            "<b>GUI:</b> PyQt5 / Streamlit for interactive analysis tool, "
            "ROI selection, frequency range selection, amplification factor control<br/>"
            "<b>Output:</b> Amplified video export, vibration spectrum plots (Matplotlib), "
            "frequency report generation<br/>"
            "<b>Camera:</b> High-speed camera recommended (120+ fps), "
            "standard camera for low-frequency vibrations<br/>"
            "<b>Deployment:</b> Desktop application, Docker for server version"
        ),
        "buzzword": (
            "Physics-Informed Neural Network for vibration mode shape estimation, "
            "Real-time motion amplification on edge devices (Jetson), "
            "Digital Twin integration for vibration-based structural health monitoring, "
            "Transformer-based temporal super-resolution for video magnification, "
            "AR overlay of amplified vibration on real structure"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1428",
        "org": "Ministry of Rural Development",
        "category": "Software",
        "description": "AR/VR based application which helps visualize the complete house virtually at an early stage, which can help in cost estimation, planning and completion of the house in time",
        "tech_stack": (
            "<b>Engine:</b> Unity 3D (C#) with AR Foundation (ARCore + ARKit), "
            "A-Frame / Three.js for web-based lightweight AR<br/>"
            "<b>3D Modeling:</b> Blender / SketchUp for house models, "
            "parametric house generation from PMAY-G approved designs, "
            "modular room/wall/roof components<br/>"
            "<b>AR:</b> ARCore (Android) ground plane detection, "
            "place 3D house model at real-world scale, "
            "walk-through capability, room-by-room visualization<br/>"
            "<b>Cost Estimation:</b> BOM (Bill of Materials) calculator linked to 3D model, "
            "SOR (Schedule of Rates) database integration, "
            "region-wise material cost database, "
            "auto-generated cost breakdown report<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL (house designs, material costs, project tracking)<br/>"
            "<b>Planning:</b> Construction phase timeline (Gantt chart), "
            "material procurement schedule, milestone tracking<br/>"
            "<b>Mobile:</b> React Native / Flutter with Unity embedding for AR, "
            "or standalone Unity Android/iOS app<br/>"
            "<b>Deployment:</b> Play Store, Docker for backend"
        ),
        "buzzword": (
            "BIM (Building Information Modeling) integration for precise quantity take-off, "
            "AI-powered construction progress prediction, "
            "Photogrammetry for as-built comparison, "
            "Generative AI for house design variation from constraints, "
            "Metaverse walkthrough for stakeholder review"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1429",
        "org": "Ministry of Rural Development",
        "category": "Software",
        "description": "Develop a solution to identify discrepancies in Quality Monitoring Data on OMMAS and generate reports that highlight areas where corrective action is Required.",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, data tables with conditional formatting<br/>"
            "<b>Backend:</b> Python (Django / FastAPI)<br/>"
            "<b>Database:</b> PostgreSQL (OMMAS data mirror, discrepancy logs)<br/>"
            "<b>Data Ingestion:</b> OMMAS API / database connector, "
            "CSV/Excel upload for offline data, "
            "pandas for data loading and cleaning<br/>"
            "<b>Discrepancy Detection:</b> Rule-based checks (missing fields, range violations, "
            "date inconsistencies, duplicate entries), "
            "statistical outlier detection (Z-score, IQR, Grubbs test), "
            "cross-validation between related data fields, "
            "scikit-learn (Isolation Forest) for anomaly detection<br/>"
            "<b>Reporting:</b> Auto-generated discrepancy reports (ReportLab / WeasyPrint), "
            "state/district/block level aggregation, "
            "severity classification (Critical/Major/Minor), "
            "corrective action recommendations<br/>"
            "<b>Dashboard:</b> Chart.js / Plotly for trend visualization, "
            "discrepancy heatmap by geography<br/>"
            "<b>Auth:</b> JWT, RBAC<br/>"
            "<b>Deployment:</b> Docker, Nginx, scheduled batch analysis (Celery/cron)"
        ),
        "buzzword": (
            "AI-powered root cause analysis for systematic data quality issues, "
            "NLP-based automated corrective action suggestion generation, "
            "Predictive data quality scoring using historical patterns, "
            "Blockchain-based data integrity verification chain, "
            "AutoML for adaptive anomaly detection thresholds"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1443",
        "org": "Autodesk Education Experience",
        "category": "Software",
        "description": "Students to use Autodesk Fusion 360 to research and to generate NC code with machine details and tool library for any industrial component.",
        "tech_stack": (
            "<b>CAD/CAM:</b> Autodesk Fusion 360 (mandatory), "
            "Manufacturing workspace for CAM operations<br/>"
            "<b>CNC Programming:</b> G-code generation via Fusion 360 toolpaths, "
            "2D (profile, pocket, drill) and 3D (adaptive, parallel, contour) strategies, "
            "tool library setup (end mills, drills, taps, inserts)<br/>"
            "<b>Post Processing:</b> Fusion 360 post processor (JavaScript), "
            "machine-specific posts (Fanuc, Haas, Siemens controllers)<br/>"
            "<b>Simulation:</b> Fusion 360 toolpath simulation (stock simulation), "
            "collision detection, tool engagement analysis<br/>"
            "<b>Material Library:</b> Cutting data for aluminum, steel, stainless, plastics, "
            "feed/speed calculations (SFM, IPT, chip load)<br/>"
            "<b>Documentation:</b> Setup sheet generation, tool list, "
            "technical drawings (Fusion Drawing workspace)<br/>"
            "<b>Validation:</b> Physical machining on CNC mill if available, "
            "verify G-code with NC viewer (NCViewer.com or CAMotics)"
        ),
        "buzzword": (
            "AI-assisted toolpath optimization for minimum cycle time, "
            "Cloud machining simulation with multi-axis kinematics, "
            "Generative Design for fixture and workholding, "
            "IoT-connected CNC for real-time machining parameter feedback, "
            "Digital Thread from CAD to quality inspection"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1449",
        "org": "National Technical Research Organisation, (NTRO)",
        "category": "Software",
        "description": "Design, develop and implement a software bill of materials (SBOM) generation tool that can generate the complete SBOM of custom-developed software.",
        "tech_stack": (
            "<b>Core:</b> Python (primary), Node.js (for JS ecosystem scanning)<br/>"
            "<b>SBOM Standards:</b> SPDX 2.3 / CycloneDX 1.5 format output (JSON, XML), "
            "NTIA minimum elements compliance<br/>"
            "<b>Dependency Scanning:</b> pip (requirements.txt, Pipfile, pyproject.toml), "
            "npm/yarn (package.json, package-lock.json), "
            "Maven (pom.xml), Gradle (build.gradle), "
            "Go (go.mod), Rust (Cargo.toml), "
            "C/C++ (CMakeLists.txt, conanfile), "
            "Docker (Dockerfile layer analysis)<br/>"
            "<b>Source Analysis:</b> Tree-sitter / AST parsing for import statement extraction, "
            "license detection (Scancode-toolkit), "
            "vulnerability cross-referencing (NVD / OSV database)<br/>"
            "<b>GUI:</b> React.js web dashboard for SBOM visualization (dependency tree graph - D3.js), "
            "vulnerability highlighting, license compliance checker<br/>"
            "<b>CLI:</b> Click / argparse for command-line usage, "
            "CI/CD integration (GitHub Actions / Jenkins plugin)<br/>"
            "<b>Database:</b> SQLite / PostgreSQL for SBOM history, diff tracking<br/>"
            "<b>Deployment:</b> pip installable package, Docker image, CLI binary"
        ),
        "buzzword": (
            "AI-powered transitive dependency risk scoring, "
            "Supply chain attack detection using anomaly analysis, "
            "Blockchain-based SBOM integrity and provenance, "
            "Binary SCA (Software Composition Analysis) for compiled artifacts, "
            "ML-based license compatibility prediction"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1450",
        "org": "National Technical Research Organisation, (NTRO)",
        "category": "Software",
        "description": "Develop and deploy a Large Language Model (LLM) based tool for generating human like responses to natural language inputs for network not connected over internet",
        "tech_stack": (
            "<b>LLM:</b> Open-source models: Llama 3 (8B/70B), Mistral 7B, Phi-3, Gemma, "
            "deployed locally via Ollama / llama.cpp / vLLM<br/>"
            "<b>Inference:</b> llama.cpp (C++ optimized CPU inference), "
            "GGUF quantized models (Q4_K_M / Q5_K_M for memory efficiency), "
            "ONNX Runtime for GPU inference, vLLM for batched serving<br/>"
            "<b>RAG (offline):</b> LangChain + FAISS (offline vector store), "
            "sentence-transformers (all-MiniLM-L6-v2) for local embeddings, "
            "document ingestion: PyMuPDF, python-docx<br/>"
            "<b>Frontend:</b> React.js / Streamlit / Gradio for chat interface<br/>"
            "<b>Backend:</b> Python (FastAPI)<br/>"
            "<b>Database:</b> SQLite (conversation logs), FAISS (vector store) — all local<br/>"
            "<b>Hardware:</b> Minimum: 16GB RAM CPU-only (7B Q4 model), "
            "Recommended: NVIDIA GPU (RTX 3090/4090) with 24GB VRAM for 70B models<br/>"
            "<b>Deployment:</b> Air-gapped deployment, Docker (pre-built image with model weights), "
            "USB-transferable package"
        ),
        "buzzword": (
            "Speculative decoding for faster inference on resource-constrained hardware, "
            "LoRA/QLoRA fine-tuning on domain-specific data, "
            "Mixture-of-Experts (MoE) architecture for efficient large models, "
            "Knowledge distillation to create smaller specialized models, "
            "On-device Retrieval-Augmented Generation with local knowledge graph"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1457",
        "org": "MathWorks India Private Limited",
        "category": "Software",
        "description": "Get Fit Faster with a High-Tech Tracker: Analyze Human Activity and GPS Data for Improved Results",
        "tech_stack": (
            "<b>Platform:</b> MATLAB (mandatory - MathWorks problem), Simulink<br/>"
            "<b>Data Sources:</b> Smartphone IMU (accelerometer, gyroscope), GPS, "
            "MATLAB Mobile app for sensor data collection<br/>"
            "<b>Signal Processing:</b> MATLAB Signal Processing Toolbox (FFT, filtering, windowing), "
            "Sensor Fusion and Tracking Toolbox<br/>"
            "<b>Activity Recognition:</b> MATLAB Classification Learner App, "
            "feature extraction (mean, std, RMS, frequency-domain features), "
            "classifiers: SVM, k-NN, Random Forest, LSTM via Deep Learning Toolbox<br/>"
            "<b>GPS Analysis:</b> MATLAB Mapping Toolbox for route visualization, "
            "speed/elevation profiling, distance calculation (Haversine), "
            "Kalman filter for GPS noise smoothing<br/>"
            "<b>Fitness Metrics:</b> Step counting (peak detection), calorie estimation, "
            "pace calculation, heart rate zone analysis (if wearable data available)<br/>"
            "<b>Visualization:</b> MATLAB plots, App Designer for GUI<br/>"
            "<b>Deployment:</b> MATLAB App Designer standalone, "
            "MATLAB Compiler for executable, ThingSpeak for cloud IoT"
        ),
        "buzzword": (
            "Deep Learning-based HAR (Human Activity Recognition) with Transformer models, "
            "Federated Learning across users for personalized fitness models, "
            "Digital Twin of human body for biomechanical analysis, "
            "Reinforcement Learning for adaptive training plan optimization, "
            "Wearable Edge AI for real-time activity classification"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1460",
        "org": "AICTE",
        "category": "Software",
        "description": "Integration of AI for Adaptive Learning for MCQ Selection in PARAKH",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (Django / FastAPI)<br/>"
            "<b>Database:</b> PostgreSQL (question bank, student responses, item parameters), Redis<br/>"
            "<b>Item Response Theory (IRT):</b> Python (pyirt / catsim) for 1PL/2PL/3PL IRT model estimation, "
            "item difficulty, discrimination, and guessing parameter calibration<br/>"
            "<b>Adaptive Testing:</b> Computerized Adaptive Testing (CAT) algorithm, "
            "maximum information criterion for next question selection, "
            "ability estimation (EAP / MLE)<br/>"
            "<b>AI/ML:</b> NLP for question quality analysis (readability, cognitive level classification - Bloom's taxonomy), "
            "auto-detection of flawed distractors (answer option analysis), "
            "scikit-learn for difficulty prediction from question text features<br/>"
            "<b>Question Bank:</b> Tagged by subject, topic, difficulty, cognitive level, "
            "version control for question edits<br/>"
            "<b>Reporting:</b> Item analysis reports, test reliability metrics (Cronbach's alpha), "
            "student ability distribution charts<br/>"
            "<b>Auth:</b> JWT, RBAC (Admin, Item Writer, Reviewer, Student)<br/>"
            "<b>Deployment:</b> Docker, Nginx"
        ),
        "buzzword": (
            "LLM-powered automatic MCQ generation from textbook content, "
            "Knowledge Tracing using Deep Learning (DKT), "
            "Transformer-based difficulty prediction from question semantics, "
            "Fairness-aware item selection (DIF - Differential Item Functioning analysis), "
            "Gamified adaptive assessment with engagement optimization"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1495",
        "org": "AICTE, MIC-Student Innovation",
        "category": "Software",
        "description": "Student Innovation",
        "tech_stack": (
            "<b>Open-ended — Same as SIH1600 (see above):</b><br/>"
            "<b>Frontend:</b> React.js / Next.js, HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (FastAPI / Django) or Node.js (Express)<br/>"
            "<b>Database:</b> PostgreSQL / MongoDB, Redis<br/>"
            "<b>AI/ML:</b> scikit-learn, PyTorch / TensorFlow (if AI component)<br/>"
            "<b>Mobile:</b> Flutter / React Native<br/>"
            "<b>Cloud:</b> AWS / GCP / Azure free tier<br/>"
            "<b>DevOps:</b> Docker, Git, GitHub Actions"
        ),
        "buzzword": (
            "Open-ended — choose based on your specific innovation"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1498",
        "org": "AICTE, MIC",
        "category": "Software",
        "description": "Develop a Proctored exam tool for shortlisting the candidates for the national and international level hackathons.",
        "tech_stack": (
            "<b>Frontend:</b> React.js, HTML5, CSS3, JavaScript, WebRTC for camera/screen capture<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js (Express), WebSocket<br/>"
            "<b>Database:</b> PostgreSQL (exam data, candidate profiles), Redis (session management)<br/>"
            "<b>Proctoring:</b> Face detection (MediaPipe / face-api.js) for presence verification, "
            "head pose estimation for gaze tracking, "
            "multiple face detection (alert on 2+ faces), "
            "tab switch / window blur detection (Page Visibility API), "
            "screen recording (MediaRecorder API), "
            "audio monitoring for voice detection<br/>"
            "<b>Anti-Cheating:</b> Browser lockdown mode (full-screen enforcement), "
            "clipboard blocking, right-click disable, "
            "AI-based suspicious behavior scoring (scikit-learn classifier)<br/>"
            "<b>Exam Engine:</b> MCQ, coding (integrate Judge0 for code execution), "
            "timer management, auto-submit, randomized question order<br/>"
            "<b>Code Editor:</b> Monaco Editor (VS Code in browser), "
            "multi-language support (Python, C++, Java, JavaScript)<br/>"
            "<b>Reporting:</b> Candidate score cards, proctoring incident reports, "
            "anomaly flagging for manual review<br/>"
            "<b>Auth:</b> JWT, Aadhaar/photo ID verification, OTP<br/>"
            "<b>Deployment:</b> Docker, Nginx, WebSocket server, CDN"
        ),
        "buzzword": (
            "AI-powered eye tracking using gaze estimation neural networks, "
            "Keystroke dynamics analysis for identity verification, "
            "LLM-based code plagiarism detection (semantic similarity), "
            "Deepfake detection for video proctoring integrity, "
            "Blockchain-based exam certificate and score immutability"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1506",
        "org": "Ministry of Ports, Shipping and Waterways",
        "category": "Software",
        "description": "Leveraging the power of deep learning to overcome the challenges of marine engineering and improve vessel operations",
        "tech_stack": (
            "<b>Frontend:</b> React.js, Leaflet.js / Mapbox for vessel tracking, "
            "HTML5, CSS3, JavaScript, D3.js for analytics<br/>"
            "<b>Backend:</b> Python (FastAPI / Django)<br/>"
            "<b>Data Sources:</b> AIS (Automatic Identification System) data (pyais), "
            "vessel performance logs (speed, fuel, RPM, draft), "
            "weather/ocean data (OpenWeatherMap API, Copernicus Marine Service)<br/>"
            "<b>Deep Learning:</b> PyTorch / TensorFlow, "
            "LSTM/GRU for fuel consumption prediction, "
            "CNN for engine fault pattern recognition from sensor data, "
            "time-series forecasting for ETA prediction, "
            "XGBoost / LightGBM for feature-based models<br/>"
            "<b>Applications:</b> Route optimization (A* with weather constraints), "
            "predictive maintenance (remaining useful life estimation), "
            "hull fouling detection from speed-power analysis, "
            "port congestion prediction<br/>"
            "<b>Database:</b> PostgreSQL + PostGIS, TimescaleDB<br/>"
            "<b>Visualization:</b> Plotly / D3.js for vessel performance dashboards<br/>"
            "<b>Deployment:</b> Docker, GPU server for model inference"
        ),
        "buzzword": (
            "Physics-Informed Neural Networks for hydrodynamic performance modeling, "
            "Digital Twin of vessel for real-time operational optimization, "
            "Reinforcement Learning for autonomous voyage planning, "
            "Satellite imagery analysis for maritime traffic pattern recognition, "
            "Federated Learning across shipping fleets for collaborative model improvement"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1515",
        "org": "Ministry of Housing and Urban Affairs",
        "category": "Software",
        "description": "Smart and Effective realtime Management of street parking",
        "tech_stack": (
            "<b>Frontend:</b> React.js / React Native (mobile), "
            "Leaflet.js / Mapbox for parking spot map, HTML5, CSS3, JavaScript<br/>"
            "<b>Backend:</b> Python (FastAPI / Django), Node.js, WebSocket for real-time updates<br/>"
            "<b>Database:</b> PostgreSQL + PostGIS (parking zones, spots), "
            "Redis (real-time occupancy cache), TimescaleDB (historical data)<br/>"
            "<b>Detection:</b> Computer Vision (YOLOv8) on existing CCTV for occupancy detection, "
            "OR IoT sensors (ultrasonic/magnetometer per spot), "
            "OR crowdsourced user check-in/check-out<br/>"
            "<b>Payment:</b> Razorpay / PayU integration, UPI, "
            "dynamic pricing engine based on demand<br/>"
            "<b>Features:</b> Spot reservation, navigation to spot (Google Maps SDK), "
            "violation detection (overstay/no-payment), "
            "enforcement officer mobile app<br/>"
            "<b>Analytics:</b> Occupancy rate trends, revenue analytics, "
            "peak hour analysis, zone-wise heatmaps<br/>"
            "<b>Notifications:</b> Spot availability alerts, parking expiry reminder<br/>"
            "<b>Auth:</b> JWT, Firebase Auth<br/>"
            "<b>Deployment:</b> Docker, Nginx, edge AI for CCTV processing"
        ),
        "buzzword": (
            "LiDAR-based 3D parking spot mapping, "
            "Deep Reinforcement Learning for dynamic pricing optimization, "
            "Digital Twin of urban parking ecosystem, "
            "Autonomous vehicle parking integration (V2I communication), "
            "Blockchain-based parking payment and violation records"
        ),
    },
    {
        "year": "SIH 2023",
        "ps_no": "SIH1516",
        "org": "Ministry of Housing and Urban Affairs",
        "category": "Software",
        "description": "Suggest an AI-based solution to enable ease of grievance lodging and tracking for citizens across multiple departments",
        "tech_stack": (
            "<b>Frontend:</b> React.js / Next.js (PWA), HTML5, CSS3, JavaScript, "
            "multi-step grievance form, status tracker UI<br/>"
            "<b>Backend:</b> Python (Django / FastAPI), Node.js<br/>"
            "<b>Database:</b> PostgreSQL (grievances, departments, status), "
            "Elasticsearch (grievance search), Redis<br/>"
            "<b>NLP/AI:</b> Text classification (BERT / IndicBERT) for auto-categorization to department, "
            "sentiment analysis for priority scoring, "
            "NER (spaCy) for location/entity extraction from complaint text, "
            "duplicate detection (sentence-transformers similarity)<br/>"
            "<b>Chatbot:</b> LangChain + RAG for guided grievance filing, "
            "Bhashini API for multilingual support<br/>"
            "<b>Workflow:</b> Multi-department routing engine, SLA tracking, "
            "escalation on SLA breach, inter-department transfer<br/>"
            "<b>Mobile:</b> React Native / Flutter<br/>"
            "<b>Notifications:</b> SMS, email, push for status updates<br/>"
            "<b>Analytics:</b> Department-wise resolution metrics, citizen satisfaction scoring, "
            "geographic grievance heatmap<br/>"
            "<b>Auth:</b> Aadhaar-based optional, JWT, guest filing option<br/>"
            "<b>Deployment:</b> Docker, Nginx, NIC Cloud"
        ),
        "buzzword": (
            "LLM-powered auto-drafting of grievance from voice input, "
            "Predictive resolution time estimation using historical patterns, "
            "Blockchain-based transparent grievance lifecycle tracking, "
            "AI-powered department recommendation with 95%+ accuracy, "
            "Citizen sentiment dashboard for policy makers"
        ),
    },
]


# ============================================================================
# PDF GENERATION
# ============================================================================

def build_pdf():
    output_path = r"d:\Testing\Research\SIH_Smart_Automation_TechStack_Analysis.pdf"
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        leftMargin=12*mm,
        rightMargin=12*mm,
        topMargin=15*mm,
        bottomMargin=15*mm,
        title="SIH Smart Automation - Tech Stack Analysis",
        author="SIH Research Team",
    )
    
    elements = []
    
    # Title
    elements.append(Paragraph(
        "SIH SMART AUTOMATION - COMPLETE TECH STACK ANALYSIS",
        title_style
    ))
    elements.append(Paragraph(
        "Comprehensive technology stack recommendations for all Smart Automation theme problem statements across SIH 2023, 2024, and 2025/2026. "
        "Each problem includes a standard competition-winning tech stack and a separate advanced/buzzword section.",
        subtitle_style
    ))
    elements.append(Spacer(1, 8))
    
    # Group by year
    year_groups = {}
    for ps in problem_statements:
        yr = ps["year"]
        if yr not in year_groups:
            year_groups[yr] = []
        year_groups[yr].append(ps)
    
    year_order = ["SIH 2025 / 2026", "SIH 2024", "SIH 2023"]
    
    for yr in year_order:
        if yr not in year_groups:
            continue
        
        ps_list = year_groups[yr]
        count = len(ps_list)
        
        # Year header
        elements.append(Paragraph(
            f"{yr} ({count} Statements)",
            year_title_style
        ))
        elements.append(Spacer(1, 4))
        
        # Table header
        header_row = [
            Paragraph("PS No.", header_style),
            Paragraph("Organization", header_style),
            Paragraph("Cat.", header_style),
            Paragraph("Problem Statement", header_style),
            Paragraph("Standard Tech Stack (Competition-Winning)", header_style),
            Paragraph("Advanced / Buzzword Tech", header_style),
        ]
        
        # Column widths for landscape A4 (~277mm usable)
        col_widths = [38, 58, 28, 130, 280, 220]
        
        table_data = [header_row]
        
        for ps in ps_list:
            row = [
                Paragraph(ps["ps_no"], cell_style_bold),
                Paragraph(ps["org"], cell_style),
                Paragraph(ps["category"], cell_style),
                Paragraph(ps["description"], cell_style),
                Paragraph(ps["tech_stack"], tech_style),
                Paragraph(ps["buzzword"], buzzword_style),
            ]
            table_data.append(row)
        
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        # Table styling
        style_commands = [
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), DARK_HEADER),
            ('TEXTCOLOR', (0, 0), (-1, 0), HEADER_TEXT),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('LINEBELOW', (0, 0), (-1, 0), 1.5, ACCENT_BLUE),
            
            # Padding
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ]
        
        # Alternating row colors
        for i in range(1, len(table_data)):
            bg = ROW_ALT_1 if i % 2 == 0 else ROW_ALT_2
            style_commands.append(('BACKGROUND', (0, i), (-1, i), bg))
            
            # Buzzword column with slight yellow tint
            style_commands.append(('BACKGROUND', (5, i), (5, i), HexColor("#fffef5") if i % 2 != 0 else HexColor("#fefcf0")))
        
        table.setStyle(TableStyle(style_commands))
        elements.append(table)
        elements.append(Spacer(1, 12))
        elements.append(PageBreak())
    
    # Footer page with legend
    elements.append(Paragraph("LEGEND & NOTES", title_style))
    elements.append(Spacer(1, 8))
    
    legend_data = [
        [Paragraph("<b>Column</b>", cell_style_bold), Paragraph("<b>Description</b>", cell_style_bold)],
        [Paragraph("PS No.", cell_style), Paragraph("Official SIH Problem Statement Number", cell_style)],
        [Paragraph("Organization", cell_style), Paragraph("Government ministry or organization that submitted the problem", cell_style)],
        [Paragraph("Cat.", cell_style), Paragraph("Category: Software, Hardware, or Software+Hardware", cell_style)],
        [Paragraph("Problem Statement", cell_style), Paragraph("Complete problem statement title/description from official SIH documents", cell_style)],
        [Paragraph("Standard Tech Stack", cell_style_bold), 
         Paragraph("The reliable, proven technology stack recommended for building a competition-winning solution. "
                    "Covers frontend, backend, database, AI/ML frameworks, specific algorithms, libraries, "
                    "hardware components, communication protocols, and deployment tools. "
                    "These are practical choices that work and can be demonstrated in a hackathon.", cell_style)],
        [Paragraph("Advanced / Buzzword Tech", cell_style_bold),
         Paragraph("Cutting-edge technologies and approaches that can be mentioned in presentations to impress judges, "
                    "or partially implemented as stretch goals. These are more research-oriented and may not be "
                    "fully implementable in a hackathon timeframe, but demonstrate technical depth and vision.", cell_style)],
    ]
    
    legend_table = Table(legend_data, colWidths=[120, 630])
    legend_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_HEADER),
        ('TEXTCOLOR', (0, 0), (-1, 0), HEADER_TEXT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, 1), (-1, -1), ROW_ALT_1),
    ]))
    elements.append(legend_table)
    
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        "<i>Generated for SIH Smart Automation Theme Research | All problem statements extracted from official SIH documents</i>",
        ParagraphStyle('FooterNote', parent=styles['Normal'], fontSize=8, textColor=HexColor("#6c757d"), alignment=TA_CENTER)
    ))
    
    # Build PDF
    doc.build(elements)
    print(f"\n[OK] PDF generated successfully at: {output_path}")
    print(f"   Total problem statements: {len(problem_statements)}")
    
    # Count by year
    for yr in year_order:
        if yr in year_groups:
            print(f"   {yr}: {len(year_groups[yr])} statements")


if __name__ == "__main__":
    build_pdf()
