import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Segoe UI fonts
pdfmetrics.registerFont(TTFont('SegoeUI', 'C:/Windows/Fonts/segoeui.ttf'))
pdfmetrics.registerFont(TTFont('SegoeUI-Bold', 'C:/Windows/Fonts/segoeuib.ttf'))
pdfmetrics.registerFont(TTFont('SegoeUI-Italic', 'C:/Windows/Fonts/segoeuii.ttf'))
pdfmetrics.registerFont(TTFont('SegoeUI-Semibold', 'C:/Windows/Fonts/seguisb.ttf'))
# Segoe UI Symbol carries the dingbat glyphs (checkmark / cross) that the
# regular Segoe UI family does not — without it these render as tofu boxes.
pdfmetrics.registerFont(TTFont('SegoeSymbol', 'C:/Windows/Fonts/seguisym.ttf'))

# Reusable inline glyph markup (rendered with the symbol font so it never tofus)
TICK = '<font name="SegoeSymbol" color="#15803D">\u2714</font>'
CROSS = '<font name="SegoeSymbol" color="#DC2626">\u2718</font>'
QUERY = '<font name="SegoeUI-Bold" color="#CA8A04">?</font>'

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print total page numbers
    along with running header and footer.
    """
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
        
        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.setFont('SegoeUI-Bold', 8)
            self.setFillColor(colors.HexColor('#0F172A'))
            self.drawString(36, 810, "SETU")
            self.setFont('SegoeUI', 8)
            self.setFillColor(colors.HexColor('#64748B'))
            self.drawString(64, 810, "|   System Architecture & Layer Specification")
            self.drawRightString(559, 810, "Passive Edge Sensing • Multi-Stage Gates • Municipal Intelligence")
            self.setStrokeColor(colors.HexColor('#E2E8F0'))
            self.setLineWidth(0.75)
            self.line(36, 804, 559, 804)

        # Running Footer (all pages)
        self.setFont('SegoeUI', 8)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(36, 26, "SETU Project — Automated Road Defect & Asset Intelligence Architecture")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 26, page_str)
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(0.75)
        self.line(36, 36, 559, 36)
        
        self.restoreState()


def create_system_architecture_pdf(output_path):
    # A4 is 595.27 x 841.89 pt. With 36pt margins, printable width = 523.27 pt
    content_width = 523

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=42,
        bottomMargin=42
    )

    # Styles
    c_primary = colors.HexColor('#0F172A')
    c_text = colors.HexColor('#334155')
    c_accent_l1 = colors.HexColor('#0D9488') # Teal
    c_accent_l2 = colors.HexColor('#2563EB') # Royal Blue
    c_accent_l3 = colors.HexColor('#7C3AED') # Purple
    c_accent_l4 = colors.HexColor('#0284C7') # Cyan
    c_accent_l5 = colors.HexColor('#E11D48') # Rose

    title_style = ParagraphStyle(
        'DocTitle',
        fontName='SegoeUI-Bold',
        fontSize=17,
        leading=21,
        textColor=colors.HexColor('#0F172A'),
        alignment=TA_LEFT
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        fontName='SegoeUI',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#475569'),
        alignment=TA_LEFT
    )

    layer_header_style = ParagraphStyle(
        'LayerHeader',
        fontName='SegoeUI-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.white
    )

    section_header_style = ParagraphStyle(
        'SectionHeader',
        fontName='SegoeUI-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=5,
        spaceAfter=3
    )

    subsection_title_style = ParagraphStyle(
        'SubSectionTitle',
        fontName='SegoeUI-Bold',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=4,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        fontName='SegoeUI',
        fontSize=8.5,
        leading=12,
        textColor=c_text
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        fontName='SegoeUI',
        fontSize=8.2,
        leading=11.6,
        textColor=c_text,
        leftIndent=11,
        firstLineIndent=-11,
        spaceAfter=2
    )

    compact_bullet_style = ParagraphStyle(
        'CompactBullet',
        fontName='SegoeUI',
        fontSize=8,
        leading=11,
        textColor=c_text,
        leftIndent=10,
        firstLineIndent=-10,
        spaceAfter=1.5
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        fontName='SegoeUI-Semibold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0F172A'),
        alignment=TA_CENTER
    )

    tech_box_style = ParagraphStyle(
        'TechBoxText',
        fontName='SegoeUI',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    def create_layer_banner(title_text, accent_color):
        p = Paragraph(f"<b>{title_text}</b>", layer_header_style)
        t = Table([[p]], colWidths=[content_width])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), accent_color),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROUNDEDCORNERS', [3, 3, 3, 3]),
        ]))
        return t

    def create_tech_box(tech_items, title="TECH USED IN THIS LAYER"):
        content = [Paragraph(f"<b>{title}:</b>", ParagraphStyle('TechTitle', fontName='SegoeUI-Bold', fontSize=8, leading=11, textColor=colors.HexColor('#0F172A')))]
        for item in tech_items:
            content.append(Paragraph(f"• {item}", tech_box_style))
        
        t = Table([[content]], colWidths=[content_width])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
            ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#CBD5E1')),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        return t

    # =============================================================
    # PAGE 1: HEADER & LAYER 1: MOBILE SDK (On-Device — The Edge)
    # =============================================================
    banner_data = [
        [Paragraph("<b>SETU — SYSTEM ARCHITECTURE SPECIFICATION</b>", title_style)],
        [Paragraph("5-Layer Engineering Pipeline: On-Device Edge Sensing, Server Clustering, Multi-Stage Verification, Municipal GIS Portal &amp; Active Feedback Loop", subtitle_style)]
    ]
    banner_table = Table(banner_data, colWidths=[content_width])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('PADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
        ('TOPPADDING', (0, 1), (-1, 1), 2),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 6))

    story.append(create_layer_banner("LAYER 1: MOBILE SDK (On-Device — The Edge)", c_accent_l1))
    story.append(Spacer(1, 4))

    # Measurements 2-column table for compact, crisp layout
    story.append(Paragraph("<b>MEASUREMENTS (Sampled Continuously):</b>", section_header_style))
    m_left = [
        "<b>3-Axis Accelerometer</b> (x, y, z) — 100 Hz",
        "<b>3-Axis Gyroscope</b> (x, y, z) — 100 Hz",
        "<b>Gravity Vector</b> (x, y, z) — 100 Hz / Continuous",
        "<b>Timestamp</b> (epoch milliseconds) — Per-event"
    ]
    m_right = [
        "<b>GPS Location</b> (lat, lon) — 1 Hz / Passive (host app)",
        "<b>GPS Accuracy</b> (metres) — 1 Hz",
        "<b>Vehicle Speed</b> (km/h) — 1 Hz",
        "<b>Vehicle Heading</b> (degrees) — 1 Hz"
    ]
    meas_rows = []
    for l, r in zip(m_left, m_right):
        meas_rows.append([
            Paragraph(f"• {l}", compact_bullet_style),
            Paragraph(f"• {r}", compact_bullet_style)
        ])
    meas_table = Table(meas_rows, colWidths=[260, 263])
    meas_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#F1F5F9')),
        ('PADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(meas_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>CALCULATIONS &amp; SIGNAL CLEANING (On-Device DSP):</b>", section_header_style))
    calculations = [
        ("Linear Resampling", "Normalize jittery Android sensor ticks to fixed 100 Hz grid"),
        ("Dynamic Acceleration", "Subtract gravity from raw accelerometer"),
        ("Vehicle-Frame Rotation", "Use gravity vector + heading to build rotation matrix, convert phone axes → vehicle vertical / longitudinal / lateral"),
        ("Total Shock Magnitude", "√(aX² + aY² + aZ²) — rotation-invariant fallback"),
        ("Band-Pass Filter", "Butterworth 0.5–30 Hz, isolate pothole energy band"),
        ("Per-Device Baseline", "Rolling mean (μ) and std dev (σ) over smoothest 20% of driving"),
        ("Normalized Shock", "Z-score: (a_vert − μ) / σ"),
        ("Peak Vertical Impact", "Maximum |a_vertical| in 2-second window"),
        ("Maximum Jerk", "max(|da/dt|) — rate of change of vertical acceleration"),
        ("Windowed RMS", "√(1/N × Σ z_i²) — sustained roughness measure"),
        ("Event Duration", "Consecutive samples above threshold × 10ms"),
        ("Cross-Axis Correlation", "Corr(a_vertical, a_lateral) — pothole roll vs bump pitch"),
        ("Threshold Gate", "if |z_norm| &lt; 3.0σ AND RMS &lt; r₀ → DROP (saves battery, kills ~99% of windows)"),
        ("Local AI Classification", "1D-CNN (~120 KB, INT8, LiteRT) classifies surviving windows into 6 classes: smooth_road / rough_road / POTHOLE / speed_bump / rumble_strip / non_road_event"),
        ("Local AI Confidence Score", "Softmax probability for the predicted class"),
        ("Road Segment Pass Count", "Silent passes over each road segment (the denominator)")
    ]
    for name, desc in calculations:
        story.append(Paragraph(f"• &nbsp; <b>{name}</b> — {desc}", compact_bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>INFORMATION SENT TO SERVER (Batched every 60s, gzipped JSON, ~200 bytes/event):</b>", section_header_style))
    payload_fields = [
        ("1. Hashed Device ID", "SHA-256(install_id + salt), no PII"),
        ("2. Vehicle Type", "two_wheeler / car / auto / bus"),
        ("3. Phone Category", "budget / midrange / flagship"),
        ("4. Device Baseline", "μ_dev, σ_dev (noise floor)"),
        ("5. Timestamp", "Epoch milliseconds"),
        ("6. Location", "(lat, lon) of defect"),
        ("7. GPS Accuracy", "68% conf. radius (m)"),
        ("8. Vehicle Speed", "km/h at moment of event"),
        ("9. Travel Direction", "Heading (0–360°)"),
        ("10. Defect Class", "pothole / rough_road"),
        ("11. Local AI Conf.", "0.0 to 1.0"),
        ("12. Vertical Force", "Peak vertical acc (m/s²)"),
        ("13. Impact Jerk", "Max jerk (m/s³)"),
        ("14. RMS Windowed", "Roughness score"),
        ("15. Event Duration", "Impact duration (ms)"),
        ("16. Pass Counts", "(segment_id, count) pairs")
    ]
    col1 = payload_fields[:8]
    col2 = payload_fields[8:]
    payload_rows = []
    for (n1, d1), (n2, d2) in zip(col1, col2):
        p1 = Paragraph(f"<b>{n1}</b>: {d1}", ParagraphStyle('P1', fontName='SegoeUI', fontSize=7.5, leading=10, textColor=c_text))
        p2 = Paragraph(f"<b>{n2}</b>: {d2}", ParagraphStyle('P2', fontName='SegoeUI', fontSize=7.5, leading=10, textColor=c_text))
        payload_rows.append([p1, p2])
    
    pay_table = Table(payload_rows, colWidths=[260, 263])
    pay_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FAFAFA')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#F1F5F9')),
        ('PADDING', (0, 0), (-1, -1), 2.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(pay_table)
    story.append(Spacer(1, 4))

    layer1_tech = [
        "<b>Kotlin + Android SDK (native)</b> (or Flutter fallback) &bull; <b>SensorManager</b> 100 Hz &bull; <b>TYPE_GRAVITY</b> orientation",
        "<b>FusedLocationProviderClient</b> GPS &bull; <b>LiteRT (TFLite)</b> on-device AI &bull; <b>Room SQLite</b> offline queue &bull; <b>WorkManager</b> upload"
    ]
    story.append(create_tech_box(layer1_tech))

    # =============================================================
    # PAGE 2: LAYER 2 (Part 1: Stages A to D)
    # =============================================================
    story.append(PageBreak())
    story.append(create_layer_banner("LAYER 2: BACKEND SERVER (Cloud — The Brain) — Part 1: Ingestion &amp; Clustering", c_accent_l2))
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>DATA RECEIVED:</b> All 16 telemetry fields from Layer 1 (batched from thousands of fleet and commuter devices).", body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>SERVER-SIDE PROCESSING (Stages A to D):</b>", section_header_style))

    stages_part1 = [
        ("Stage A — Ingestion &amp; Validation", [
            "<b>Payload Schema Validation</b>: Pydantic v2 rejects malformed or out-of-range data before touching the database.",
            "<b>Rate Limiting</b>: slowapi throttles excessive submissions per device hash to prevent spam or runaway loops.",
            "<b>Speed Gate</b>: Discard events where speed &lt; 5 km/h (walking/handling artifacts) or &gt; 150 km/h (erroneous spikes).",
            "<b>GPS Accuracy Gate</b>: Discard events where GPS accuracy radius &gt; 30m.",
            "<b>Timestamp Sanity</b>: Reject future timestamps or events older than 48 hours.",
            "<b>Duplicate Suppression</b>: Same device hash + same location (within 5m) + within 60 seconds → retain highest-confidence event only."
        ]),
        ("Stage B — Normalization &amp; Trust Scoring", [
            "<b>Speed-Normalized Impact</b>: <code>impact_norm = vertical_impact / √(speed)</code> — equalizes impact severity readings across varying vehicle speeds.",
            "<b>Device Trust Score</b>: <code>weight = f(phone_category, gps_accuracy, baseline_noise)</code> — flagship phones with tight GPS and low noise floor receive highest initial weighting.",
            "<b>Device Reputation</b>: Trust score increases when device reports align with confirmed defect clusters; drops when reports consistently land in rejected noise clusters."
        ]),
        ("Stage C — Geo-Processing", [
            "<b>Map Matching</b>: Snap raw GPS coordinates to nearest road centreline using self-hosted OSRM with OpenStreetMap data. Eliminates perpendicular GPS drift (~27–32m in dense urban corridors).",
            "<b>Road Segment Assignment</b>: Tag each event with its corresponding OSM Way ID and segment identifier.",
            "<b>Lane Determination</b>: Utilizes vehicle heading combined with road geometry to determine precise travel direction on divided dual-carriageways.",
            "<b>Ward / Zone Lookup</b>: Spatial join against municipal boundary polygons to tag the administrative ward responsible for maintenance.",
            "<b>H3 Hexagonal Indexing</b>: PostGIS spatial indexing for scalable multi-resolution spatial aggregation."
        ]),
        ("Stage D — DBSCAN Spatial Clustering", [
            "<b>Clustering</b>: PostGIS <code>ST_ClusterDBSCAN(geom, eps := 20, minpoints := 5)</code> on map-matched points. Groups events within 20m having ≥ 5 reports.",
            "<b>Distinct Device Requirement</b>: Cluster requires reports from ≥ 5 DISTINCT device hashes. 40 reports from 1 device ≈ 1 report, not 40. Per-device contribution capped at 3.",
            "<b>Inverse-Variance Weighted Centroid</b>: Confirmed location = Σ(wi × loci) / Σ(wi) where wi = 1/accuracy² — tighter GPS readings dominate the centroid calculation.",
            "<b>Confidence Ellipse</b>: Uncertainty reported as an error ellipse, displayed on the dashboard as a confidence-scaled circle.",
            "<b>Cluster Confidence Score</b>: <code>cluster_conf = 1 − ∏(1 − conf_i)</code> for all reports (e.g., 5 distinct devices at 85% confidence yield 99.99% aggregate cluster confidence).",
            "<b>Vehicle Diversity Bonus</b>: Clusters containing both two-wheelers and four-wheelers receive higher confidence scores, ruling out vehicle-specific suspension harmonics."
        ])
    ]

    for title, items in stages_part1:
        stage_flow = []
        stage_flow.append(Paragraph(f"<b>{title}</b>", subsection_title_style))
        for item in items:
            stage_flow.append(Paragraph(f"• &nbsp; {item}", bullet_style))
        story.append(KeepTogether(stage_flow))
        story.append(Spacer(1, 3))

    # =============================================================
    # PAGE 3: LAYER 2 (Part 2: Stages E to G, DB Schema & Tech Stack)
    # =============================================================
    story.append(PageBreak())
    story.append(create_layer_banner("LAYER 2: BACKEND SERVER (Cloud — The Brain) — Part 2: Analytics &amp; Infrastructure", c_accent_l2))
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>SERVER-SIDE PROCESSING (Stages E to G):</b>", section_header_style))

    stages_part2 = [
        ("Stage E — Defect Analysis", [
            "<b>Classification Consensus</b>: Majority vote across reports in cluster (e.g., 8 say 'pothole', 2 say 'rough_road' → confirmed POTHOLE).",
            "<b>Severity Score</b>: <code>severity = (0.4 × avg_impact_norm) + (0.3 × avg_jerk) + (0.2 × max_impact) + (0.1 × avg_duration)</code>.<br/>Categorized into: <b>LOW / MEDIUM / HIGH / CRITICAL</b>.",
            "<b>Defect Size Estimation</b>: <code>width_m ≈ avg_speed_m_s × avg_duration_s</code>.",
            "<b>Detection Rate</b>: <code>pothole_detections / total_passes_on_segment</code>. (50/500 = 10% = real defect; 3/10,000 = 0.03% = background noise).",
            "<b>Road Roughness Index</b>: Aggregates RMS roughness values per road segment across all devices over 30 days to build a continuous roughness heatmap."
        ]),
        ("Stage F — Temporal Intelligence", [
            "<b>New vs Known</b>: Checks if a confirmed defect already exists within 20m. If yes → updates existing record (attaches new telemetry evidence); if no → instantiates new cluster.",
            "<b>Trend Analysis</b>: Tracks severity progression over weeks (growing defect vs stabilized vs sudden drop to 0 indicating road resurfacing).",
            f"<b>Repair Verification ('Verified by Silence')</b>: When municipal contractors mark a pothole as 'repaired', SETU monitors passive telemetry. Zero detections from 100+ subsequent passes over 7 days &rarr; <b>repair confirmed</b> {TICK}. If detections resume &rarr; <b>repair failed</b>, ticket auto-reopened {CROSS}.",
            "<b>Seasonal Adjustment</b>: During monsoon months (June–September): automatically lowers minpoints threshold to accommodate rapid pothole formation and reduced traffic volumes."
        ]),
        ("Stage G — Infrastructure Learning", [
            "<b>Speed Bump Whitelisting</b>: Consistent detections at same location with low jerk + long duration + symmetric pitch → auto-tagged as speed bump. Future triggers auto-suppressed.",
            "<b>Railway Crossing / Expansion Joint Mapping</b>: Periodic multi-spike patterns at fixed locations are mapped as permanent roadway infrastructure.",
            "<b>Suppression Zones</b>: Persistent false-positive areas (steep driveways, parking ramps) receive down-weighting (×0.2) with escalating TTL: 3 days → 7 days → 30 days."
        ])
    ]

    for title, items in stages_part2:
        stage_flow = []
        stage_flow.append(Paragraph(f"<b>{title}</b>", subsection_title_style))
        for item in items:
            stage_flow.append(Paragraph(f"• &nbsp; {item}", bullet_style))
        story.append(KeepTogether(stage_flow))
        story.append(Spacer(1, 3))

    story.append(Paragraph("<b>DATA STORED (PostgreSQL + PostGIS):</b>", section_header_style))
    db_items = [
        "<b>Raw events table</b> — All incoming reports with full DSP and orientation metadata",
        "<b>Clusters table</b> — Confirmed defects with centroid, confidence ellipse, severity, status, and evidence count",
        "<b>Pass counts table</b> — Per-segment, per-device silent pass tracking (the denominator for statistical confidence)",
        "<b>Infrastructure whitelist</b> — Known speed bumps, railway crossings, bridge expansion joints",
        "<b>Device reputation table</b> — Rolling trust scores per device hash",
        "<b>Road segments table</b> — Roughness index, aggregate RMS, detection rate per OSM segment",
        "<b>Work orders table</b> — Municipal repair tickets with status, SLA clock, contractor assignment, and verification logs"
    ]
    for d in db_items:
        story.append(Paragraph(f"• &nbsp; {d}", bullet_style))
    story.append(Spacer(1, 4))

    layer2_tech = [
        "<b>Python 3.11+ / FastAPI</b> — Async API server &bull; <b>Pydantic v2</b> — Strict schema validation",
        "<b>PostgreSQL 16 + PostGIS 3</b> — Spatial database, DBSCAN, GiST spatial indexing &bull; <b>Redis 7</b> — Broker &amp; hot cache",
        "<b>Celery + Celery Beat</b> — Background task workers &amp; 5-minute clustering schedule &bull; <b>OSRM (Docker)</b> — Road map matching",
        "<b>scikit-learn</b> — DBSCAN, Random Forest baseline &bull; <b>SQLAlchemy 2.0 + Alembic</b> — ORM &amp; migrations",
        "<b>MinIO (dev) / S3 (prod)</b> — Video storage with pre-signed URLs &bull; <b>Docker Compose</b> &bull; <b>Deploy</b>: Railway / Render / Fly.io"
    ]
    story.append(create_tech_box(layer2_tech))

    # =============================================================
    # PAGE 4: LAYER 3 (Multi-Stage Ground Truth Verification)
    # =============================================================
    story.append(PageBreak())
    story.append(create_layer_banner("LAYER 3: MULTI-STAGE VERIFICATION (Ground-Truth Confirmation)", c_accent_l3))
    story.append(Spacer(1, 5))

    story.append(Paragraph(
        "The system enforces a <b>Cost-Gated Escalation Ladder</b> so that expensive resources (camera operation, video upload bandwidth, municipal contractor dispatch) are ONLY triggered when lower-cost statistical filters have already confirmed a candidate cluster.",
        body_style
    ))
    story.append(Spacer(1, 5))

    # Diagram Table
    ladder_data = [
        [Paragraph("<b>[Passive Sensor Cluster (Layer 2)]</b><br/><font size=7.5 color='#475569'>Continuous accelerometer &amp; gyroscope analytics identify candidate defect cluster</font>", code_style)],
        [Paragraph("↓ &nbsp; <i>(≥ 5 distinct devices flag candidate)</i>", ParagraphStyle('Arr', fontName='SegoeUI-Semibold', fontSize=8, leading=10, alignment=TA_CENTER, textColor=colors.HexColor('#7C3AED')))],
        [Paragraph("<b>[Step 1: Geofenced 1-Tap Rider Prompt]</b><br/><font size=7.5 color='#475569'>Queued prompt appears ONLY when safely stopped ~50–100m ahead (zero video/battery cost)</font>", code_style)],
        [Paragraph("↓ &nbsp; <i>(≥ 2 independent YES votes)</i>", ParagraphStyle('Arr2', fontName='SegoeUI-Semibold', fontSize=8, leading=10, alignment=TA_CENTER, textColor=colors.HexColor('#7C3AED')))],
        [Paragraph("<b>[Step 2: Gated Video Capture]</b><br/><font size=7.5 color='#475569'>5–8s buffered clip → On-device pre-filter → Server YOLOv11 Bounding Box &amp; Area Estimation</font>", code_style)],
        [Paragraph("↓ &nbsp; <i>(Vision Confirmed)</i>", ParagraphStyle('Arr3', fontName='SegoeUI-Semibold', fontSize=8, leading=10, alignment=TA_CENTER, textColor=colors.HexColor('#16A34A')))],
        [Paragraph("<b>[Status: CONFIRMED DEFECT] → Auto-escalates to Municipal Operations (Layer 4)</b>", ParagraphStyle('Conf', fontName='SegoeUI-Bold', fontSize=8.5, leading=12, alignment=TA_CENTER, textColor=colors.HexColor('#15803D')))]
    ]
    ladder_table = Table(ladder_data, colWidths=[content_width])
    ladder_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FAF5FF')),
        ('BACKGROUND', (0, 6), (-1, 6), colors.HexColor('#DCFCE7')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#D8B4FE')),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(ladder_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Step 1: Geofenced 1-Tap Human Verification (The Cheap Gate)</b>", subsection_title_style))
    step1_items = [
        "<b>When it triggers</b>: Backend identifies an unverified DBSCAN candidate cluster (≥ 5 distinct device pings).",
        "<b>Where it triggers</b>: Backend arms a 50–100m geofence around the candidate defect location.",
        f"<b>Safety Gate (Non-Negotiable)</b>: The app NEVER prompts a rider while moving. The prompt is queued and ONLY appears when the vehicle comes to a complete stop (speed &lt; 3 km/h for &gt; 5 s at a traffic signal or delivery drop-off):<br/>&nbsp;&nbsp;&nbsp;&nbsp;<i>\"You recently passed a bumpy spot on MG Road — was that a pothole?\"</i><br/>&nbsp;&nbsp;&nbsp;&nbsp;<b>[ {TICK} YES ] &nbsp;&nbsp;&nbsp;&nbsp; [ {CROSS} NO ] &nbsp;&nbsp;&nbsp;&nbsp; [ {QUERY} NOT SURE ]</b>",
        "<b>Limits</b>: Capped at ≤ 2 prompts per rider per day to prevent notification fatigue.",
        "<b>Outcome</b>: Filters out 85–90% of accidental sensor triggers (rough patches, manhole covers) without consuming video bandwidth or battery."
    ]
    for s in step1_items:
        story.append(Paragraph(f"• &nbsp; {s}", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Step 2: Gated Video Capture &amp; Vision Confirmation (The Expensive Gate)</b>", subsection_title_style))
    step2_items = [
        "<b>Trigger Condition</b>: ONLY fires after 2 independent riders vote YES on the 1-tap prompt (or distinct high-magnitude sensor spikes).",
        "<b>Camera Trigger</b>: Next opted-in rider approaching the location with a handlebar-mounted phone (detected via stable landscape gravity vector) receives a silent trigger to buffer a 5–8 second rear camera clip.",
        "<b>On-Device Pre-Filter</b>: Discards clip immediately if scene is underexposed, heavily blurred, or phone is detected inside a bag/pocket.",
        "<b>Cloud Vision Inference</b>: Uploaded clip is processed on the server by YOLOv11 → verifies pothole bounding box, calculates approximate surface area (m²), and generates a compressed visual evidence thumbnail for municipal engineers.",
        "<b>Privacy &amp; DPDP Compliance</b>: Raw video is permanently purged after 7 days; only the anonymized, cropped defect bounding box is retained in the database."
    ]
    for s in step2_items:
        story.append(Paragraph(f"• &nbsp; {s}", bullet_style))

    # =============================================================
    # PAGE 5: LAYER 4 & LAYER 5 (Dashboard & Model Feedback Loop)
    # =============================================================
    story.append(PageBreak())
    story.append(create_layer_banner("LAYER 4: MUNICIPAL WEB PORTAL (The Dashboard)", c_accent_l4))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>DATA RECEIVED FROM BACKEND:</b> Confirmed defects (coordinates, severity, classification, evidence count, unique devices, timestamps), road roughness heatmap data (per-segment RMS), ward-level aggregate metrics, work order status logs, live updates via WebSocket.", compact_bullet_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>DASHBOARD SCREENS:</b>", section_header_style))
    screens = [
        ("Screen 1 — Live GIS Map (The Main Screen)", [
            "<b>deck.gl Layers</b>: ScatterplotLayer (potholes as GREEN → YELLOW → ORANGE → RED dots), HeatmapLayer (roughness overlay), and PathLayer (road segment health).",
            "<b>Map Controls &amp; Dynamic Fly-To</b>: Google Maps / MapLibre basemap toggle. Filter by severity, ward, date, and repair status. Newly confirmed defects pulse dynamically and auto-center the viewport. Clicking a dot opens Defect Detail Drawer."
        ]),
        ("Screen 2 — Defect Detail (Slide-over Drawer)", [
            "<b>Evidence &amp; Metrics</b>: Video crop with bounding box, P1–P4 severity score, estimated surface area (m²), evidence summary (e.g. <i>\"47 reports from 31 vehicles • 6 rider confirmations • verified in 2 clips\"</i>).",
            "<b>Timeline &amp; Action Dispatch</b>: First Seen → Confirmed → Work Order Created → Assigned → Under Repair → Verified. One-click assignment to ward engineer or work order export."
        ]),
        ("Screen 3 — Ward Scorecard", [
            "<b>Comparative League Table</b>: Ward | Open Defects | P1 Critical | Avg Resolution Time | Failed Repairs | Road Quality Score. Drives gamified municipal accountability with 90-day trend sparklines."
        ]),
        ("Screen 4 — Analytics &amp; Reports", [
            "<b>Visualization Suite</b>: Defect trends over time (line charts), repair SLA by ward (bar charts), top 10 worst roads (ranked table), monsoon vs dry season analysis, hourly detection heatmaps. One-click PDF export."
        ]),
        ("Screen 5 — Work Order Management", [
            f"<b>Lifecycle Tracking</b>: Created → Assigned → Under Repair → Repair Claimed → <b>Verified</b> {TICK} / <b>Failed</b> {CROSS}. Real-time SLA countdown turns red if overdue. Auto-escalates unassigned critical defects &gt; 24 hrs."
        ])
    ]

    for title, items in screens:
        scr_flow = []
        scr_flow.append(Paragraph(f"<b>{title}</b>", subsection_title_style))
        for item in items:
            scr_flow.append(Paragraph(f"• &nbsp; {item}", compact_bullet_style))
        story.append(KeepTogether(scr_flow))
        story.append(Spacer(1, 2))

    layer4_tech = [
        "<b>React 18 + TypeScript + Vite</b> &bull; <b>deck.gl</b> (ScatterplotLayer, HeatmapLayer, PathLayer) &bull; <b>Google Maps JS / MapLibre GL</b>",
        "<b>Zustand</b> state &bull; <b>TanStack Query</b> caching &bull; <b>Tailwind CSS + shadcn/ui</b> &bull; <b>Recharts</b> &bull; <b>framer-motion</b> &bull; <b>WebSocket</b> sync"
    ]
    story.append(create_tech_box(layer4_tech, "TECH USED IN LAYER 4"))
    story.append(Spacer(1, 8))

    # Layer 5
    story.append(create_layer_banner("LAYER 5: MODEL IMPROVEMENT (Post-Launch Feedback Loop)", c_accent_l5))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>INITIAL MODEL BASELINE:</b> Initial model trained on public datasets. Expected baseline: <b>~70–78% single-device accuracy → ~85–90% after spatial clustering</b>.", compact_bullet_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>WHAT THE FEEDBACK LOOP PRODUCES:</b>", section_header_style))
    feedback_items = [
        "<b>Growing labelled dataset of REAL Indian road events</b> — The proprietary SETU-IND-1 dataset.",
        "<b>Vehicle-specific calibration profiles</b> — Activa vibrates differently from Pulsar from Swift.",
        "<b>Phone-specific noise profiles</b> — Budget Redmi vs mid-range vs flagship Samsung/iPhone.",
        "<b>Regional road pattern data</b> — Mumbai coastal roads ≠ Lucknow asphalt ≠ Bangalore ring roads.",
        "<b>Speed bump / infrastructure map</b> — Auto-built, auto-expanding permanent feature catalog.",
        "<b>Seasonal patterns</b> — Monsoon = more potholes, distinct vibration signatures on waterlogged roads."
    ]
    for f in feedback_items:
        story.append(Paragraph(f"• &nbsp; {f}", compact_bullet_style))
    story.append(Spacer(1, 3))

    layer5_tech = [
        "<b>Label Studio (self-hosted)</b> &bull; <b>MLflow / W&amp;B</b> experiment tracking &bull; <b>PyTorch</b> (1D-CNN retraining)",
        "<b>Ultralytics YOLO</b> (vision model) &bull; <b>Google Colab / Kaggle T4 GPU</b> &bull; <b>LiteRT converter</b> (INT8) &bull; <b>Remote model push</b>"
    ]
    story.append(create_tech_box(layer5_tech, "TECH USED IN LAYER 5"))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF at: {output_path}")

if __name__ == '__main__':
    target_path = os.path.join(os.path.dirname(__file__), "SETU_System_Architecture.pdf")
    create_system_architecture_pdf(target_path)
