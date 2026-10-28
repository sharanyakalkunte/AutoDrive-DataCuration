# AutoDrive-DataCuration: Edge Data Filtering and Metadata Curation for Autonomous Vehicles

## Problem Statement
Autonomous vehicle testing fleets generate petabytes of raw video and sensor data every single day. For major automotive manufacturers, uploading all of this raw footage to the cloud creates massive infrastructure overhead and storage costs. Furthermore, training AI perception models on hours of empty, uneventful highway driving is computationally inefficient. 

The primary engineering challenge is automated data curation: filtering through massive data lakes to instantly isolate high-value, rare, or safety-critical driving scenarios (often referred to as corner cases) without relying on slow, manual human video annotation.

This project provides a lightweight, event-driven streaming pipeline designed to process real-time vehicle telemetry data at the edge, calculate immediate scene criticality scores, and generate structured metadata catalogs.

## Production Scaling Strategy
The core processing loop uses a decoupled architecture, allowing it to scale from this local test environment to enterprise production environments:

* **Distributed Ingestion:** The `MockPerceptionSystem` generator can be swapped directly for a distributed data stream consumer. The pipeline's logic is fully compatible with distributed frameworks such as Apache Kafka or Apache Spark Streaming for handling high-throughput corporate data lakes.
  
* **Edge-Native Deployment:** Because the computational overhead of the processing engine is exceptionally low (< 0.2ms latency), the pipeline can run directly on a vehicle's edge-computing unit. This allows automated filtering and metadata tagging to happen inside the vehicle, minimizing expensive cross-network cloud transmission.

##  Pipeline Functionality
The application executes the following data management lifecycle:
1. **Telemetry Ingestion:** The pipeline monitors incoming descriptions from the vehicle's camera perception system (simulating the outputs of an edge model like YOLO). This includes frame identifiers, timestamps, environmental conditions, and lists of detected object classes along with their bounding box coordinate arrays.
2. **Criticality Assessment:** The system runs a deterministic rules matrix to evaluate situational safety risk. Detections involving Vulnerable Road Users (VRUs) such as pedestrians or cyclists, combined with degraded visibility states like rain, dynamically increase a calculated criticality score. 
3. **Semantic Tagging:** Frames that exceed a safety risk threshold (greater than 0.7) are automatically assigned high-priority catalog tags (`CRITICAL_CORNER_CASE_VRU_CLOSE_PROXIMITY`), separating them from routine driving frames.
4. **Strict Schema Validation:** The pipeline pipes the processed data through Pydantic v2 validation models. This enforces strict nested type-safety boundaries on incoming data, ensuring that variables are sanitized before being dumped into a relational storage file (`curated_driving_data.json`).

## Performance Indicators
* **Processing Latency:** Mean execution time per data frame is sub-millisecond (< 0.20 ms), matching the processing constraints required for active vehicle computing hubs.
* **Dependency Profile:** Designed with minimal cloud overhead, utilizing local data validation models to run fully self-contained.


##  Installation and Execution

Ensure you have Python 3 installed, then execute the following terminal setup:

```bash
# 1. Clone the repository
git clone https://github.com/sharanyakalkunte/AutoDrive-DataCuration
cd AutoDrive-DataCuration

# 2. Install the required schema validation dependencies
pip3 install -r requirements.txt

# 3. Execute the automated stream pipeline simulation
python3 pipeline.py
```
