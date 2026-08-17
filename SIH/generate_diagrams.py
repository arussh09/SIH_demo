import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
output_dir = r"d:\Testing\Research\diagrams"
os.makedirs(output_dir, exist_ok=True)

# ---------------------------------------------------------
# 1. Tech Stack Frequency Chart
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
techs = ['React.js', 'Python', 'PostgreSQL', 'FastAPI', 'Docker', 'Django', 'Node.js', 'Redis', 'LLM / RAG', 'Blockchain', 'Digital Twin', 'React Native / Flutter', 'GIS / Leaflet', 'Bhashini / Multilingual', 'OpenCV / Vision', 'ESP32 / Microcontrollers']
counts = [120, 117, 90, 89, 82, 70, 49, 41, 35, 32, 31, 27, 24, 16, 15, 12]

# Reverse for horizontal bar plot
techs = techs[::-1]
counts = counts[::-1]

colors_list = ['#16213e' if c < 30 else '#0f3460' if c < 80 else '#e94560' for c in counts]
bars = ax.barh(techs, counts, color=colors_list, height=0.65, edgecolor='black', linewidth=0.5)

ax.set_title('Top Technology Mention Frequency in SIH Smart Automation Problem Statements', fontsize=11, fontweight='bold', pad=12, color='#1a1a2e')
ax.set_xlabel('Number of Mentions / Recommended Invocations', fontsize=9, fontweight='bold')
ax.grid(axis='x', linestyle='--', alpha=0.6)

# Add values on bars
for bar in bars:
    width = bar.get_width()
    ax.text(width + 1.5, bar.get_y() + bar.get_height()/2, f'{int(width)}', ha='left', va='center', fontsize=8, fontweight='bold', color='#1a1a2e')

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'tech_frequency.png'), bbox_inches='tight')
plt.close(fig)
print("Generated tech_frequency.png")

# ---------------------------------------------------------
# 2. Category Split Donut Chart
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 4.5), dpi=300)
categories = ['Software (74.8%)', 'Hardware (20.4%)', 'Software + Hardware / IIoT (4.8%)']
sizes = [77, 21, 5]
colors = ['#0f3460', '#e94560', '#f39c12']

wedges, texts, autotexts = ax.pie(sizes, labels=categories, colors=colors, autopct='%1.1f%%',
                                  startangle=140, pctdistance=0.75,
                                  textprops=dict(color="black", fontweight='bold', fontsize=8.5),
                                  wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(9)

ax.set_title('SIH Smart Automation Category Distribution', fontsize=11, fontweight='bold', pad=12, color='#1a1a2e')
plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'category_split.png'), bbox_inches='tight')
plt.close(fig)
print("Generated category_split.png")

# ---------------------------------------------------------
# 3. Top Sponsoring Ministries Bar Chart
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=300)
ministries = ['Ministry of Jal Shakti', 'National Technical Research Org (NTRO)', 'Ministry of Coal', 'Indian Space Research Org (ISRO)', 'State Governments (J&K, Kerala, Raj, Delhi)', 'Ministry of Electronics & IT (MeitY)', 'Ministry of Railways', 'Ministry of Earth Sciences (MoES)', 'AICTE / MIC']
ps_counts = [15, 12, 10, 8, 14, 7, 6, 5, 8]

# Sort
indices = np.argsort(ps_counts)
ministries = [ministries[i] for i in indices]
ps_counts = [ps_counts[i] for i in indices]

bars = ax.barh(ministries, ps_counts, color='#0f3460', height=0.6, edgecolor='#1a1a2e', linewidth=0.5)

ax.set_title('Problem Statement Count by Sponsoring Ministry / Body', fontsize=11, fontweight='bold', pad=12, color='#1a1a2e')
ax.set_xlabel('Number of Official Problem Statements', fontsize=9, fontweight='bold')
ax.grid(axis='x', linestyle='--', alpha=0.6)

for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.3, bar.get_y() + bar.get_height()/2, f'{int(width)}', ha='left', va='center', fontsize=8, fontweight='bold', color='#1a1a2e')

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'ministry_dist.png'), bbox_inches='tight')
plt.close(fig)
print("Generated ministry_dist.png")

# ---------------------------------------------------------
# 4. Universal Tech Stack Architecture Diagram
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
ax.axis('off')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# Main container
rect_bg = patches.Rectangle((2, 2), 96, 96, linewidth=1.5, edgecolor='#1a1a2e', facecolor='#f8f9fa')
ax.add_patch(rect_bg)

# Header
ax.text(50, 93, 'UNIVERSAL TECH STACK ARCHITECTURE FOR SMART AUTOMATION', ha='center', va='center', fontsize=11, fontweight='bold', color='#1a1a2e')

# Layers definition: (y_bottom, height, title, subtitle, color, border_color)
layers = [
    (74, 14, 'LAYER 1: PRESENTATION & CLIENT USER INTERFACES', 'Web: React.js / Next.js, TailwindCSS | Mobile: Flutter / React Native | Dashboards: Chart.js, D3.js', '#e8f4f8', '#0f3460'),
    (54, 15, 'LAYER 2: API GATEWAY & APPLICATION BUSINESS LOGIC', 'Primary Backend: Python (FastAPI / Django REST Framework) | Secondary: Node.js (Express)\nAsync Queue: Celery + Redis | WebSockets for Real-time Telemetry | JWT & OAuth2 Auth', '#d1ecf1', '#17a2b8'),
    (28, 21, 'LAYER 3: MODULAR INTELLIGENCE & DOMAIN ENGINES', '• AI/LLM & RAG Engine: PyTorch, LangChain, LlamaIndex, Ollama (Llama 3/Mistral), Bhashini Multilingual API, ChromaDB\n• Computer Vision Edge: OpenCV, YOLOv8/v9, ONNX Runtime, Tesseract OCR\n• IoT Telemetry & Hardware: ESP32/STM32 Microcontrollers, MQTT Broker (Mosquitto), FreeRTOS\n• GIS & Mapping Engine: PostGIS, Leaflet.js, Mapbox GL, ISRO Bhuvan Satellite APIs\n• Digital Twin & Simulation: WebXR, Three.js, Unity, Autodesk Fusion 360', '#fff3cd', '#ffc107'),
    (8, 15, 'LAYER 4: DATA STORAGE, PERSISTENCE & DEVOPS INFRASTRUCTURE', 'Relational DB: PostgreSQL | Cache/Queue: Redis | Object Storage: MinIO / AWS S3\nContainerization: Docker & Docker Compose | Web Server: Nginx | CI/CD: GitHub Actions', '#d4edda', '#28a745')
]

for y, h, title, content, bg_color, border_color in layers:
    box = patches.Rectangle((5, y), 90, h, linewidth=1.2, edgecolor=border_color, facecolor=bg_color)
    ax.add_patch(box)
    ax.text(8, y + h - 3.5, title, ha='left', va='center', fontsize=8.5, fontweight='bold', color='#1a1a2e')
    ax.text(8, y + (h/2) - 2.5, content, ha='left', va='top', fontsize=7.2, color='#2c3e50', wrap=True)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'tech_stack_arch.png'), bbox_inches='tight')
plt.close(fig)
print("Generated tech_stack_arch.png")

# ---------------------------------------------------------
# 5. Smart Automation Dataflow Workflow Diagram
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4), dpi=300)
ax.axis('off')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

ax.text(50, 90, 'END-TO-END SMART AUTOMATION SOLUTION DATAFLOW WORKFLOW', ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1a1a2e')

blocks = [
    (3, 25, 20, 50, '1. DATA INGESTION\n\n• IoT Sensors (IMU/CT)\n• CCTV / Camera Live\n• PDF/DOCX Documents\n• Satellite / GPS Feed', '#e8f4f8', '#0f3460'),
    (27, 25, 20, 50, '2. EDGE & GATEWAY\n\n• ESP32 / RPi / Jetson\n• MQTT / REST Gateway\n• Edge Preprocessing\n• Signal Filtering', '#d1ecf1', '#17a2b8'),
    (51, 25, 20, 50, '3. AI/ML ENGINE\n\n• YOLO Object Detection\n• LLM RAG + Vector DB\n• Bhashini Multilingual\n• Rule-based Logic', '#fff3cd', '#ffc107'),
    (75, 25, 22, 50, '4. ACTION & DISPATCH\n\n• React Web Dashboard\n• Mobile Push / SMS\n• Hardware Relay Actuation\n• Automated PDF Report', '#d4edda', '#28a745')
]

for x, y, w, h, text, bg, border in blocks:
    box = patches.Rectangle((x, y), w, h, linewidth=1.2, edgecolor=border, facecolor=bg)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#1a1a2e')

# Draw arrows between blocks
arrows = [(23.5, 50, 26.5, 50), (47.5, 50, 50.5, 50), (71.5, 50, 74.5, 50)]
for x1, y1, x2, y2 in arrows:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#1a1a2e", lw=2, mutation_scale=15))

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'system_workflow.png'), bbox_inches='tight')
plt.close(fig)
print("Generated system_workflow.png")
