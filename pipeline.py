import os
import json
import time
from typing import List, Dict
from pydantic import BaseModel, Field

class MockPerceptionSystem:
    def __init__(self):
        self.frame_stream = [
            {"frame_id": 1001, "timestamp": 17100001, "weather": "rainy", "detected_objects": ["car", "car", "pedestrian"], "bounding_boxes": [[10, 20, 50, 60], [30, 40, 70, 80], [100, 150, 120, 180]]},
            {"frame_id": 1002, "timestamp": 17100002, "weather": "rainy", "detected_objects": ["car", "pedestrian", "bicycle"], "bounding_boxes": [[12, 22, 52, 62], [102, 152, 122, 182], [200, 250, 240, 290]]},
            {"frame_id": 1003, "timestamp": 17100003, "weather": "clear", "detected_objects": ["car", "truck"], "bounding_boxes": [[15, 25, 55, 65], [400, 410, 480, 500]]}
        ]
    def get_next_frame(self) -> Dict:
        if self.frame_stream:
            return self.frame_stream.pop(0)
        return None

class BoundingBox(BaseModel):
    coordinates: List[int] = Field(..., description="X, Y coordinates of the object bounding box")

class CuratedMetadata(BaseModel):
    frame_id: int
    timestamp: int
    environment_condition: str
    vru_count: int = Field(..., description="Count of Vulnerable Road Users like pedestrians or cyclists")
    criticality_score: float = Field(..., description="Automated safety risk score based on proximity metrics")
    scenario_tag: str = Field(..., description="Automated semantic label for engineering retrieval")

class AutoCurationPipeline:
    def __init__(self):
        self.perception = MockPerceptionSystem()
        self.curated_database = []

    def evaluate_criticality(self, objects: List[str], boxes: List[List[int]], weather: str) -> float:
        score = 0.1
        if "pedestrian" in objects or "bicycle" in objects:
            score += 0.4
        if weather in ["rainy", "foggy", "snowy"]:
            score += 0.3
        if len(objects) > 2:
            score += 0.2
        return round(min(score, 1.0), 2)

    def generate_semantic_tag(self, objects: List[str], score: float) -> str:
        if score > 0.7:
            return "CRITICAL_CORNER_CASE_VRU_CLOSE_PROXIMITY"
        elif "pedestrian" in objects:
            return "SYSTEM_AUTONOMY_VRU_TRACKING"
        return "STANDARD_HIGHWAY_DRIVING"

    def process_stream(self):
        print(" Initializing AutoDrive Curation Pipeline...")
        print("--------------------------------------------------")
        while True:
            frame = self.perception.get_next_frame()
            if not frame:
                break
            start_time = time.time()
            vru_count = frame["detected_objects"].count("pedestrian") + frame["detected_objects"].count("bicycle")
            risk_score = self.evaluate_criticality(frame["detected_objects"], frame["bounding_boxes"], frame["weather"])
            tag = self.generate_semantic_tag(frame["detected_objects"], risk_score)
            metadata = CuratedMetadata(
                frame_id=frame["frame_id"],
                timestamp=frame["timestamp"],
                environment_condition=frame["weather"],
                vru_count=vru_count,
                criticality_score=risk_score,
                scenario_tag=tag
            )
            self.curated_database.append(metadata.model_dump())

            latency = (time.time() - start_time) * 1000
            print(f"Processed Frame ID: {metadata.frame_id} | Latency: {latency:.4f}ms")
            print(f"Tag assigned: {metadata.scenario_tag} [Risk Score: {metadata.criticality_score}]")
            print("--------------------------------------------------")
        with open("curated_driving_data.json", "w") as f:
            json.dump(self.curated_database, f, indent=4)
        print("Data Curation Complete. Metadata logs written to 'curated_driving_data.json'.")

if __name__ == "__main__":
    pipeline = AutoCurationPipeline()
    pipeline.process_stream()
