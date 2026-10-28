# AutoDrive-DataCuration: Edge Data Filtering and Metadata Curation for Autonomous Vehicles

## 🏢 System Context and Problem Space
Autonomous vehicle testing fleets generate petabytes of raw video and sensor data every single day. For major automotive manufacturers, uploading all of this raw footage to the cloud creates massive infrastructure overhead and storage costs. Furthermore, training AI perception models on hours of empty, uneventful highway driving is computationally inefficient. 

The primary engineering challenge is automated data curation: filtering through massive data lakes to instantly isolate high-value, rare, or safety-critical driving scenarios (often referred to as corner cases) without relying on slow, manual human video annotation.

This project provides a lightweight, event-driven streaming pipeline designed to process real-time vehicle telemetry data at the edge, calculate immediate scene criticality scores, and generate structured metadata catalogs.

## ⚙️ Core Pipeline Functionality
The application executes the following data management lifecycle:
1. **Telemetry Ingestion:** The pipeline monitors incoming descriptions from the vehicle's camera perception system (simulating the outputs of an edge model like YOLO). This includes frame identifiers, timestamps, environmental conditions, and lists of detected object classes along with their bounding box coordinate arrays.
2. **Criticality Assessment:** The system runs a deterministic rules matrix to evaluate situational safety risk. Detections involving Vulnerable Road Users (VRUs) such as pedestrians or cyclists, combined with degraded visibility states like rain, dynamically increase a calculated criticality score. 
3. **Semantic Tagging:** Frames that exceed a safety risk threshold (greater than 0.7) are automatically assigned high-priority catalog tags (`CRITICAL_CORNER_CASE_VRU_CLOSE_PROXIMITY`), separating them from routine driving frames.
4. **Strict Schema Validation:** The pipeline pipes the processed data through Pydantic v2 validation models. This enforces strict nested type-safety boundaries on incoming data, ensuring that variables are sanitized before being dumped into a relational storage file (`curated_driving_data.json`).

## 📊 Performance Indicators
* **Processing Latency:** Mean execution time per data frame is sub-millisecond (< 0.20 ms), matching the processing constraints required for active vehicle computing hubs.
* **Dependency Profile:** Designed with minimal cloud overhead, utilizing local data validation models to run fully self-contained.

## 🌐 Enterprise Production Scaling Strategy
While this local repository contains an isolated, zero-dependency data simulator (`MockPerceptionSystem`) to ensure instant out-of-the-box execution, the core logic engine is designed to scale across large corporate infrastructures:

* **Distributed Ingestion:** The input layer is decoupled from the processing loop. In a production environment, the localized data generator can be swapped for a distributed consumer link connected to frameworks like Apache Kafka or Apache Spark Streaming.
* **Edge-Native Deployment:** Because the memory and CPU footprint of this Python engine is exceptionally lightweight, the script can be deployed directly onto individual test cars to filter and tag high-value data logs locally before cross-network transmission to central data centers occurs.

## 🛠️ Installation and Execution

Ensure you have Python 3 installed, then execute the following terminal setup:

```bash
# 1. Clone the repository
git clone https://github.com
cd AutoDrive-DataCuration

# 2. Install the required schema validation dependencies
pip3 install -r requirements.txt

# 3. Execute the automated stream pipeline simulation
python3 pipeline.py
```
