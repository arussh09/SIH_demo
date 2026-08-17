import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.setStrokeColor(HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(40, 750, 572, 750)
            self.drawString(40, 755, "SETU Mobile App & On-Device AI — Technical Specification")
            self.drawRightString(572, 755, "Edge AI & Sensing Architecture")

        # Footer (all pages)
        self.setStrokeColor(HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(40, 36, 572, 36)
        self.drawString(40, 25, "SETU: Crowdsourced Road Defect Intelligence for India")
        self.drawRightString(572, 25, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename="app.pdf"):
    # Margins 40pt to fit content cleanly into 2 high-density pages
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Color Palette
    c_primary = HexColor("#0F172A")    # Slate 900
    c_secondary = HexColor("#1E40AF")  # Blue 800
    c_accent = HexColor("#0369A1")     # Sky 700
    c_dark = HexColor("#334155")       # Slate 700
    c_light_bg = HexColor("#F8FAFC")   # Slate 50
    c_card_bg = HexColor("#F1F5F9")    # Slate 100
    c_border = HexColor("#CBD5E1")     # Slate 300
    c_code_bg = HexColor("#0F172A")    # Dark theme code box
    c_code_text = HexColor("#E2E8F0")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=c_secondary
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13.5,
        textColor=c_secondary,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=c_dark
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=11,
        textColor=HexColor("#1E3A8A")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=HexColor("#FFFFFF")
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.2,
        textColor=c_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=c_primary
    )

    code_line_style = ParagraphStyle(
        'CodeLine',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.8,
        leading=8.5,
        textColor=c_code_text
    )

    story = []

    # ================= PAGE 1 =================
    # Title Block
    story.append(Paragraph("SETU: Primary Mobile App & On-Device AI Architecture", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Technical Specification: Edge Sensor Ingestion, DSP Math, Feature Extraction & Cloud Payloads", subtitle_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.2, color=c_secondary, spaceBefore=0, spaceAfter=5))

    # Executive Callout
    overview_text = (
        "<b>Architectural Role (Layer 1 Edge SDK):</b> The SETU primary application runs as an ultra-lightweight (~200 KB SDK) "
        "inside gig-worker host apps (Swiggy, Zomato, Ola, Rapido). It utilizes a strictly <i>edge-first, battery-protective</i> "
        "design: deterministic Digital Signal Processing (DSP) and hard statistical gating eliminate <b>~99% of regular driving windows</b> "
        "on the CPU. A quantized 120 KB LiteRT/TFLite 1D-CNN runs only on candidate shock events to classify road defects, uploading "
        "rich metadata every 60 seconds while keeping battery drain &lt; 2%/hr and mobile data &lt; 1 MB/day."
    )
    callout_data = [[Paragraph(overview_text, callout_style)]]
    callout_table = Table(callout_data, colWidths=[532])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 0.75, HexColor("#93C5FD")),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 4))

    # Section 1
    story.append(Paragraph("1. Direct Hardware & Sensor Measurements (Sampled Continuously)", h1_style))
    story.append(Paragraph("The app interfaces directly with device hardware via Android <code>SensorManager</code> and <code>FusedLocationProviderClient</code>:", body_style))
    story.append(Spacer(1, 2))

    meas_table_data = [
        [Paragraph("Hardware Channel", table_header_style), Paragraph("Sampling Rate", table_header_style), Paragraph("Physics & Purpose Measured", table_header_style)],
        [Paragraph("<b>3-Axis Accelerometer</b> (aX, aY, aZ)", table_cell_bold), Paragraph("100 Hz (~10 ms)", table_cell_style), Paragraph("Measures linear acceleration and kinetic impact forces across X, Y, and Z axes.", table_cell_style)],
        [Paragraph("<b>3-Axis Gyroscope</b> (gX, gY, gZ)", table_cell_bold), Paragraph("100 Hz (~10 ms)", table_cell_style), Paragraph("Measures angular velocity (roll, pitch, yaw rates); detects single-wheel roll asymmetry when hitting a pothole.", table_cell_style)],
        [Paragraph("<b>Gravity Vector</b> (gx, gy, gz)", table_cell_bold), Paragraph("100 Hz / Continuous", table_cell_style), Paragraph("Measures static gravitational field direction to calculate real-world 'down' and device orientation.", table_cell_style)],
        [Paragraph("<b>GPS Coordinates</b> (Lat, Lon)", table_cell_bold), Paragraph("1 Hz / Passive Fix", table_cell_style), Paragraph("Geographic location of the vehicle, reusing host app's background GPS fixes to preserve battery.", table_cell_style)],
        [Paragraph("<b>GPS Accuracy Radius</b> (m)", table_cell_bold), Paragraph("1 Hz", table_cell_style), Paragraph("Horizontal uncertainty radius (68% confidence in metres) for inverse-variance weighting.", table_cell_style)],
        [Paragraph("<b>Speed & Heading (Bearing)</b>", table_cell_bold), Paragraph("1 Hz", table_cell_style), Paragraph("Speed (km/h) and direction (0–360°), essential for speed-adaptive scaling and geofence timing.", table_cell_style)],
        [Paragraph("<b>High-Res Timestamps</b>", table_cell_bold), Paragraph("Per-event (ns / ms)", table_cell_style), Paragraph("Elapsed realtime monotonic clock mapped to epoch milliseconds to prevent clock drift.", table_cell_style)],
    ]
    t_meas = Table(meas_table_data, colWidths=[140, 85, 307])
    t_meas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#FFFFFF"), c_light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_meas)
    story.append(Spacer(1, 4))

    # Section 2
    story.append(Paragraph("2. Deterministic Signal Processing (DSP) & Mathematical Calculations", h1_style))
    story.append(Paragraph("Before running any AI, the phone's CPU executes deterministic mathematical transformations over a <b>2.0-second sliding window</b> (50% overlap, 200 samples/axis):", body_style))
    story.append(Spacer(1, 2))

    calc_table_data = [
        [Paragraph("Processing Step", table_header_style), Paragraph("Formula / Transformation", table_header_style), Paragraph("Engineering Objective", table_header_style)],
        [Paragraph("<b>1. Linear Resampling</b>", table_cell_bold), Paragraph("<code>LinearInterpolate(t, 100Hz)</code>", table_cell_style), Paragraph("Normalizes jittery Android sensor ticks onto a fixed 100 Hz grid, preventing frequency distortion.", table_cell_style)],
        [Paragraph("<b>2. Gravity Removal</b>", table_cell_bold), Paragraph("a<sub>dyn</sub> = a<sub>total</sub> − g", table_cell_style), Paragraph("Subtracts constant 9.81 m/s² gravity vector so only dynamic road shocks remain.", table_cell_style)],
        [Paragraph("<b>3. Coordinate Rotation</b>", table_cell_bold), Paragraph("R<sub>gravity,heading</sub> · [aX, aY, aZ]<sup>T</sup>", table_cell_style), Paragraph("Converts arbitrary phone orientation into vehicle frame: a<sub>vertical</sub>, a<sub>longitudinal</sub>, a<sub>lateral</sub>.", table_cell_style)],
        [Paragraph("<b>4. Total Shock Mag.</b>", table_cell_bold), Paragraph("a<sub>mag</sub> = √(aX² + aY² + aZ²)", table_cell_style), Paragraph("Rotation-invariant kinetic shock magnitude; stable even if phone shifts during riding.", table_cell_style)],
        [Paragraph("<b>5. Band-Pass Filter</b>", table_cell_bold), Paragraph("Butterworth (0.5 – 30 Hz)", table_cell_style), Paragraph("Strips low-frequency chassis drift (&lt;0.5 Hz) and engine hum (&gt;30 Hz), isolating 3–20 Hz pothole energy.", table_cell_style)],
        [Paragraph("<b>6. Self-Calibration</b>", table_cell_bold), Paragraph("z<sub>norm</sub> = (a<sub>vert</sub> − μ<sub>dev</sub>) / σ<sub>dev</sub>", table_cell_style), Paragraph("Calculates rolling baseline noise floor (μ, σ) over smoothest 20% of driving to equalize soft vs. stiff vehicles.", table_cell_style)],
        [Paragraph("<b>7. Maximum Jerk</b>", table_cell_bold), Paragraph("jerk<sub>max</sub> = max(|dz/dt|)", table_cell_style), Paragraph("Rate of change of vertical acceleration (m/s³); speed-stable metric separating true potholes from bumps.", table_cell_style)],
        [Paragraph("<b>8. Windowed RMS</b>", table_cell_bold), Paragraph("RMS = √( (1/N) ∑ z<sub>i</sub>² )", table_cell_style), Paragraph("Root Mean Square over 2-second window to gauge continuous surface roughness.", table_cell_style)],
        [Paragraph("<b>9. Cross-Axis Corr</b>", table_cell_bold), Paragraph("Corr(a<sub>vertical</sub>, a<sub>lateral</sub>)", table_cell_style), Paragraph("Differentiates single-wheel pothole drop (roll asymmetry) from two-wheel speed bump hits (symmetrical pitch).", table_cell_style)],
        [Paragraph("<b>10. Threshold Gate</b>", table_cell_bold), Paragraph("if |z<sub>norm</sub>| &lt; 3.0 and RMS &lt; r0: DROP", table_cell_style), Paragraph("<b>The Battery Saver:</b> Hard rule-based gate dropping 99% of windows; model runs only ~5 times/minute.", table_cell_style)],
    ]
    t_calc = Table(calc_table_data, colWidths=[110, 155, 267])
    t_calc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#FFFFFF"), c_light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_calc)

    # ================= PAGE 2 =================
    story.append(PageBreak())

    # Section 3
    story.append(Paragraph("3. On-Device AI Classification & Decision Engine (LiteRT / 1D-CNN)", h1_style))
    story.append(Paragraph("Candidate windows surviving the threshold gate are processed locally by an INT8-quantised 1D-CNN (~120 KB) running on LiteRT:", body_style))
    story.append(Spacer(1, 2))

    ai_classes_data = [
        [Paragraph("Class Index & Name", table_header_style), Paragraph("Physical Waveform Signature & Characteristics", table_header_style), Paragraph("Action / Routing", table_header_style)],
        [Paragraph("<b>Class 0: smooth_road</b>", table_cell_bold), Paragraph("Minimal vertical variance, smooth laminar vibration floor.", table_cell_style), Paragraph("Drop locally (no upload)", table_cell_style)],
        [Paragraph("<b>Class 1: rough_road</b>", table_cell_bold), Paragraph("Sustained high-frequency vibration, elevated windowed RMS, no distinct crater.", table_cell_style), Paragraph("Queue event (if τ ≥ 0.8)", table_cell_style)],
        [Paragraph("<b>Class 2: POTHOLE</b>", table_cell_bold), Paragraph("Sharp drop-then-rebound vertical signature + high jerk + single-wheel roll asymmetry.", table_cell_style), Paragraph("Queue event (if τ ≥ 0.8)", table_cell_style)],
        [Paragraph("<b>Class 3: speed_bump</b>", table_cell_bold), Paragraph("Symmetrical upward pitch spike, dual-wheel compression, low roll correlation.", table_cell_style), Paragraph("Drop locally (False Positive)", table_cell_style)],
        [Paragraph("<b>Class 4: rumble_strip / joint</b>", table_cell_bold), Paragraph("Periodic multi-peak spikes (expansion joint, railway crossing, manhole cover).", table_cell_style), Paragraph("Drop locally (False Positive)", table_cell_style)],
        [Paragraph("<b>Class 5: non_road_event</b>", table_cell_bold), Paragraph("Phone drop off mount, pocket movement, door slam, sudden foot-braking.", table_cell_style), Paragraph("Drop locally (False Positive)", table_cell_style)],
    ]
    t_ai = Table(ai_classes_data, colWidths=[130, 272, 130])
    t_ai.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#0369A1")),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#FFFFFF"), c_light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_ai)
    story.append(Spacer(1, 4))

    # Section 4
    story.append(Paragraph("4. Exact Information Sent to the Cloud Backend (Payload Contract)", h1_style))
    story.append(Paragraph("When anomalies pass the AI confidence threshold (τ ≥ 0.8), the app batches them into gzipped JSON uploaded every 60s:", body_style))
    story.append(Spacer(1, 2))

    lines = [
        '// POST /v1/events (Batched, Gzipped JSON)',
        '{',
        '  "sdk_version": "0.4.1",',
        '  "device": {',
        '    "id_hash": "sha256(install_id + salt)",       // Salt-hashed device ID (No PII / GDPR-compliant)',
        '    "model_class": "android_midrange",           // Generalized device tier (reduces fingerprinting)',
        '    "vehicle_class": "two_wheeler",              // two_wheeler | car | auto | bus',
        '    "calibration": { "noise_floor_z": 0.42, "samples": 60000 } // Baseline noise floor calibration',
        '  },',
        '  "events": [',
        '    {',
        '      "ts": 1786512345678,                       // Anomaly epoch timestamp in milliseconds',
        '      "lat": 26.84671, "lon": 80.94623,          // GPS coordinates of the detected defect',
        '      "gps_accuracy_m": 6.4,                     // 68% confidence error radius (metres)',
        '      "speed_kmph": 34.2, "heading_deg": 271.5,  // Instantaneous speed and compass bearing',
        '      "label": "pothole",                        // 6-class AI output (pothole | rough_road)',
        '      "confidence": 0.87,                        // AI model softmax confidence probability',
        '      "peak_z": 18.4,                            // Peak vertical acceleration (m/s² in vehicle frame)',
        '      "jerk_max": 220.5,                         // Maximum shock jerk (m/s³)',
        '      "rms_window": 4.9,                         // Windowed Root Mean Square roughness',
        '      "duration_ms": 180                         // Impact shock duration in milliseconds',
        '    }',
        '  ],',
        '  "passes": [',
        '    { "segment_id": "osm:way/1234", "count": 12 } // The Denominator: silent passes over road segment',
        '  ]',
        '}'
    ]
    code_elements = [Paragraph(f"<code>{line.replace(' ', '&nbsp;')}</code>", code_line_style) for line in lines]
    code_table = Table([[code_elements]], colWidths=[532])
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_code_bg),
        ('BOX', (0, 0), (-1, -1), 0.75, HexColor("#475569")),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(code_table)
    story.append(Spacer(1, 4))

    # Gated Payloads
    gated_text = (
        "<b>Additional Server-Command Payloads (Triggered via Response ACK):</b><br/>"
        "• <b>Mode 2 (Human Confirmation Vote):</b> <code>{ cmd_id: 'c_1b7d', answer: 'yes'|'no'|'not_sure', ts: 1786512999000, device_id_hash: '...' }</code> — One-tap verification prompt displayed strictly when vehicle is stopped (speed &lt; 3 km/h for &gt; 5s).<br/>"
        "• <b>Mode 3 (Gated Visual Proof):</b> 5–8 second 720p rear-camera video clip uploaded directly to pre-signed S3 URL only at confirmed candidate geofences (60–80m speed-adaptive radius) when phone is in a stable mount. Local video deleted immediately upon HTTP 200 and checksum verification."
    )
    story.append(Paragraph(gated_text, body_style))
    story.append(Spacer(1, 4))

    # Section 5
    story.append(Paragraph("5. Edge Performance, Privacy & Telemetry Budgets", h1_style))
    budget_data = [
        [Paragraph("Performance Metric", table_header_style), Paragraph("Hard Budget", table_header_style), Paragraph("Enforcement & Architectural Mechanism", table_header_style)],
        [Paragraph("<b>Battery Consumption</b>", table_cell_bold), Paragraph("&lt; 2% / hour", table_cell_style), Paragraph("Threshold gate drops 99% of windows; reuses host GPS stream; no camera in normal mode.", table_cell_style)],
        [Paragraph("<b>Mobile Data Transfer</b>", table_cell_bold), Paragraph("&lt; 1 MB / day", table_cell_style), Paragraph("Batched gzipped JSON (~200 bytes/event); only uploads high-confidence positives (τ ≥ 0.8).", table_cell_style)],
        [Paragraph("<b>CPU & Memory Footprint</b>", table_cell_bold), Paragraph("&lt; 3% CPU / &lt; 5 MB RAM", table_cell_style), Paragraph("120 KB INT8 LiteRT model executed single-threaded via XNNPACK; circular in-memory buffer.", table_cell_style)],
        [Paragraph("<b>Offline Resilience</b>", table_cell_bold), Paragraph("100% Offline-First", table_cell_style), Paragraph("Events queue locally in Room SQLite database; WorkManager retries upload with exponential backoff.", table_cell_style)],
        [Paragraph("<b>Privacy (DPDP Act 2023)</b>", table_cell_bold), Paragraph("Zero PII / Salted Hashes", table_cell_style), Paragraph("No continuous GPS tracking (only discrete defect points); salted SHA-256 device hashing; instant erasure API.", table_cell_style)],
    ]
    t_budget = Table(budget_data, colWidths=[120, 95, 317])
    t_budget.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#FFFFFF"), c_light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_budget)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == '__main__':
    build_pdf("app.pdf")
