# Pothole Detection & Municipal Work-Order Automation — Full Project Guide

Simple explanation of everything needed to build this project: the tech, the datasets, and other important things people usually forget.

---

## 1. What This Project Actually Is (In Simple Words)

- A phone app (running inside apps like delivery/driver apps) sits on a car/bike dashboard.
- It uses the **camera** and the **shake sensor (accelerometer)** to notice when the vehicle goes over a pothole.
- It saves the location (GPS) of the pothole.
- Many different vehicles report the same pothole from different times/angles.
- The system groups (clusters) all these reports together to confirm "yes, there really is a pothole here."
- Once confirmed, it automatically creates a repair ticket and sends it to the municipal corporation.
- Officers see everything on a live map (web dashboard) and manage repairs.

There are **4 main parts**: Mobile SDK → Backend Server → Clustering Logic → Web Dashboard + Government Integration.

---

## 2. Tech Stack (In Simple Words)

### A. Mobile Part (runs inside driver/delivery apps)

| What it does | Tool/Tech to use | Why |
|---|---|---|
| App code | Kotlin (Android) | Most delivery drivers in India use Android phones |
| Run in background | Android Foreground Service | Needed so camera/sensors keep working even when app is minimized |
| Read shake/motion | Android SensorManager (Accelerometer + Gyroscope) | Detects the "jolt" when wheel hits a pothole |
| Camera | CameraX (Android Jetpack library) | Easier and more stable way to use camera continuously |
| AI model on phone | TensorFlow Lite or ONNX Runtime Mobile (running a small YOLO model) | Detects pothole in camera frame, works without internet, doesn't drain battery |
| Make AI model small & fast | INT8 Quantization | Shrinks the AI model so cheap phones can run it smoothly |
| Use phone's AI chip | NNAPI (Android Neural Networks API) | Makes the AI model run faster using phone hardware |
| Store data when no internet | SQLite (Room database) | Saves pothole reports locally, sends later when internet is back |
| Location | Google Fused Location Provider | Better, more accurate GPS location |

### B. Backend Server (receives and processes all reports)

| What it does | Tool/Tech to use | Why |
|---|---|---|
| Main server | Node.js (NestJS) or Go | Handles thousands of pothole reports coming in every minute |
| Handle traffic spikes | Apache Kafka or AWS Kinesis | Rush hour = lots of reports at once; this prevents server crash |
| Database | PostgreSQL + PostGIS extension | PostGIS is a special add-on that understands maps/locations — **this is the most important database choice** |
| Store pothole photos | AWS S3 (or Google Cloud Storage) | Cheap, safe place to store millions of images |
| Background processing | Python + Celery, or Apache Spark (only if very large scale) | Runs the clustering/confirmation logic |

### C. Clustering Logic (the "confirm it's a real pothole" brain)

| What it does | Tool/Tech to use | Why |
|---|---|---|
| Group nearby reports into one confirmed pothole | **DBSCAN algorithm** (via scikit-learn or PostGIS's ST_ClusterDBSCAN) | DBSCAN finds groups of reports close together in location automatically, and ignores single random reports (reduces false alarms) |
| Alternative if pothole density varies a lot (highway vs city) | HDBSCAN | Handles uneven spacing better than plain DBSCAN |
| Supporting tools | GeoPandas, Shapely (Python libraries for map math) | Standard tools for location-based calculations |

### D. Web Dashboard (for municipal officers)

| What it does | Tool/Tech to use | Why |
|---|---|---|
| Website framework | React + TypeScript | Standard, modern way to build web apps |
| Map display | MapLibre GL JS (free) or Mapbox (paid) + Deck.gl | Shows potholes on a live map, Deck.gl handles thousands of map points smoothly |
| Live updates without refresh | WebSockets (Socket.IO) | New potholes/tickets show up instantly on screen |
| Login/access control | Keycloak (free, self-hosted) or AWS Cognito | Different officers get different access levels |
| Design/UI components | Ant Design or shadcn/ui + Tailwind CSS | Ready-made buttons, tables, forms — faster to build |
| Charts/reports | Recharts | Shows resolution-time graphs, ward-wise stats |
| Local language support | react-i18next | Hindi + regional languages — important for adoption by officers |

### E. Government Integration (turning confirmed potholes into actual repair work)

| What it does | Tool/Tech to use | Why |
|---|---|---|
| Ticket workflow (Created → Assigned → Fixed → Verified) | Temporal or Camunda (workflow engine) | Keeps track of ticket status properly, handles delays/escalation |
| SMS alerts to officers | Twilio or AWS SNS | Many officers won't check a dashboard daily; SMS is more reliable |
| WhatsApp updates | WhatsApp Business API | Very commonly used and trusted in India for this kind of update |
| Connect to each city's own system | Custom-built adapter per city (REST/SOAP), or auto-email/PDF ticket as backup | Most Indian municipalities don't have a shared open system — expect to build this one city at a time |

### F. Infrastructure (running everything reliably)

| What it does | Tool/Tech to use | Why |
|---|---|---|
| Cloud hosting | AWS (or Azure) | Common in Indian government-approved cloud vendors |
| Running many services | Kubernetes (EKS) | Auto-scales up during rush hour traffic |
| Automatic testing/deployment | GitHub Actions | Every code change is tested/deployed automatically |
| Monitoring for crashes | Prometheus + Grafana (server), Sentry (mobile app) | Alerts you when something breaks |
| Tracking AI model versions | MLflow | Keeps track of which AI model version is live, helps roll back if new version is worse |
| Remote on/off switch for features | LaunchDarkly (or free alternative) | Since your SDK lives inside other people's apps (Swiggy/Zomato), you need to disable features remotely without an app update |

---

## 3. Where to Get Datasets (In Simple Words)

### A. Pothole Photos (for training the camera AI model)

| Dataset Name | What's in it | Link |
|---|---|---|
| **RDD2022** | 47,420 road photos, 55,000+ marked potholes/cracks, from 6 countries **including India** — best starting dataset | github.com/sekilab/RoadDamageDetector |
| **Indian Roads Pothole Dataset (Springer, 2024)** | 10,000 labeled photos + 364 videos, captured on actual Indian roads using phone cameras — closest match to your exact use case | Search: "Development and Evaluation of a Comprehensive Dataset for Pothole Depth Estimation of Indian Roads" (Springer) |
| **HRP4K** | 6,003 images, 7,217 marked potholes, ready-to-use YOLO format | nature.com/articles/s41597-026-07317-w |
| **Pothole-600** | Stereo camera images (has depth info) — useful later for judging pothole severity/size | sites.google.com/view/pothole-600/dataset |
| **Kaggle Pothole Datasets** | Several smaller sets (400–3,000 images) — good for quick first tests | Search "pothole" on kaggle.com/datasets |

**Note:** These give you a good starting AI model. You will still need to improve it later using your own real collected data, because Indian road conditions, camera angles, and lighting will differ from these datasets.

### B. Accelerometer + Gyroscope Data (for the shake-sensor AI model)

There is **no single big ready-made dataset** for this like RDD2022 is for photos. But here's what's available:

| Source | What's in it | Link |
|---|---|---|
| **Nericell (Microsoft Research India, 2008)** | The original research project for this exact idea — detects potholes using accelerometer, done in Bangalore, India. Solves the "phone mounted at a random angle" problem. **Read this first.** | research.microsoft.com/en-us/projects/nericell |
| **aswathselvam/Potholes (GitHub)** | Real working code + data format: `timestamp, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z` at 50 readings/second | github.com/aswathselvam/Potholes |
| **sagxam/Pothole-Project (GitHub)** | Code that tells apart potholes vs. speed bumps using accelerometer+gyroscope — solves one of your biggest false-alarm problems | github.com/sagxam/Pothole-Project |
| **"Harnessing Smartphone Sensors for Road Safety" (Nature, 2024)** | A proper research dataset with accelerometer, gyroscope, GPS, and more, built for road safety | nature.com/articles/s41597-024-04193-0 |

**Important:** You will most likely need to **collect your own data** by driving over known potholes with a phone recording sensor data, because:
- Two-wheelers, cars, and autos all shake differently — one setting won't work for all.
- No existing free dataset has camera + accelerometer + GPS all recorded together, which is exactly what your system needs.

### C. Official Indian Government Data

| Source | What's in it | Link |
|---|---|---|
| **data.gov.in** | India's open government data portal — search for road/accident related datasets | data.gov.in |
| **MoRTH Road Accident Reports** | Yearly official reports on road accidents, includes pothole-caused accidents | Search "Road Accidents in India" report, morth.nic.in |
| **Parliament records (sansad.in)** | Official numbers: 9,438 deaths from potholes (2020–2024) — good for your project's problem statement/pitch | sansad.in |
| **Bharatmaps (bharatmaps.gov.in)** | Official government map data — roads, admin boundaries | bharatmaps.gov.in/bharatmaps |

### D. Map/Location Data (roads, ward boundaries)

| Source | What's in it | Link |
|---|---|---|
| **OpenStreetMap (via Geofabrik)** | Free, detailed road maps for every Indian city | download.geofabrik.de/asia/india.html |
| **datameet/Municipal_Spatial_Data** | Community-made ward boundary maps for some Indian cities | github.com/datameet/Municipal_Spatial_Data |
| **datta07/INDIAN-SHAPEFILES** | State, district, and constituency boundary files | github.com/datta07/INDIAN-SHAPEFILES |

**Warning:** These community-made ward boundaries are "good enough to show on a map" but NOT official/legal-accuracy. For real government use, you'll eventually need to ask each municipal corporation directly for their official ward boundary files.

---

## 4. Other Important Things Needed (Often Forgotten)

### A. Privacy & Legal (Very Important — Not Optional)

- Your camera is recording continuously in public — it WILL capture faces, license plates, and people's houses by accident.
- India's **DPDP Act 2023** (data protection law) requires you to handle this properly.
- **Fix:** Blur faces and license plates directly on the phone before any image ever leaves the device. Don't send raw video anywhere.
- You need a clear, simple privacy policy that drivers agree to before the SDK starts recording.

### B. Getting Real Users (The Actual Hard Part)

- Building the tech is not the hardest part — getting Swiggy, Zomato, Ola, or similar apps to install your SDK inside their driver app is the hardest part.
- This needs business partnerships, not just code.
- Alternative: start with your own simple app for volunteer drivers/citizens first, prove it works in one city, THEN pitch to bigger delivery companies.

### C. False Alarms Problem

- Speed bumps, manholes, broken road joints, and already-repaired potholes can trick the sensors/camera.
- You need a lot of "negative examples" (photos/sensor data of things that look like potholes but aren't) to train the AI to avoid false alarms.
- Municipalities will stop trusting your system fast if it sends too many wrong tickets.

### D. Every City Is Different (Integration Problem)

- Most Indian municipal corporations do NOT have a modern software system to receive tickets automatically.
- You will likely need to build a different small connector for each city (or just send an email/PDF ticket as a fallback for cities with no system at all).
- Some cities already have a "Smart City" command center (called ICCC) — your long-term goal should be feeding data INTO their existing dashboard, not making officers use two separate dashboards.

### E. Team Roles You'll Need

| Role | What they do |
|---|---|
| Android Developer | Builds the mobile SDK |
| ML/AI Engineer | Builds and trains the pothole detection models (camera + sensor) |
| Backend Developer | Builds the server, database, APIs |
| Frontend Developer | Builds the web dashboard for officers |
| DevOps Engineer | Sets up cloud servers, keeps everything running |
| GIS/Map Specialist | Handles all the location/mapping logic (DBSCAN tuning, map data) |
| Government Liaison / Business Person | Talks to municipal corporations, handles partnerships and approvals |
| Legal/Privacy Advisor | Makes sure you follow India's data protection laws |

### F. Suggested Order to Build This (Simple Roadmap)

1. **Start small:** Build just the camera-based pothole detector first (easier to test, use existing photo datasets).
2. **Add sensors:** Add accelerometer+gyroscope detection on top, to reduce battery use and false alarms.
3. **Pick ONE city** for a pilot test — don't try to launch nationally at once.
4. **Build the clustering + dashboard** to confirm potholes and show them on a map.
5. **Manually contact that one city's municipal office** to test the ticket workflow (even if it's just emails at first).
6. **Once proven in one city**, then approach bigger delivery apps (Swiggy/Zomato/Ola) to embed your SDK.
7. **Scale up** to more cities one at a time, building new connectors as needed.

### G. Government Schemes to Mention (For Pitching)

- **Smart Cities Mission** — most relevant; many cities already have command centers (ICCC) you could plug into.
- **PMGSY** — focused on rural roads; note that rural roads have less traffic, so you'll need fewer confirming reports before marking a pothole as "confirmed" compared to busy city roads.
- **Bharat NCAP** — vehicle safety ratings; connection here is more about the "road safety" story than a direct technical integration.

---

## 5. Quick Summary Table (Everything At a Glance)

| Category | Main Tools Needed |
|---|---|
| Mobile App | Kotlin, CameraX, TensorFlow Lite, SensorManager, SQLite |
| Backend | Node.js/Go, PostgreSQL+PostGIS, Kafka, AWS S3 |
| AI/Clustering | YOLO (small model), DBSCAN, scikit-learn, GeoPandas |
| Web Dashboard | React, MapLibre/Mapbox, Deck.gl, WebSockets |
| Government Integration | Temporal/Camunda, Twilio, WhatsApp Business API |
| Infrastructure | AWS, Kubernetes, GitHub Actions, Prometheus/Grafana |
| Datasets | RDD2022, Indian Roads Pothole Dataset, Nericell research, OpenStreetMap |
| Non-Tech Needs | Privacy/legal compliance (DPDP Act), business partnerships, per-city integration, own field data collection |

---

*This file is a working reference — update it as decisions are made or new datasets/tools are found.*
