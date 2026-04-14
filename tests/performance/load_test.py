import pytest
import time
import concurrent.futures
import requests
from typing import List, Dict


API_BASE_URL = "http://localhost:8000/api/v1"


class TestAPILoad:
    """Test API performance under load (Milestone 389)"""

    @pytest.fixture
    def sample_payload(self):
        return {
            "order_id": "ORD-001",
            "origin_lat": 52.52,
            "origin_lon": 13.405,
            "destination_lat": 48.1351,
            "destination_lon": 11.582,
            "scheduled_date": "2026-04-15",
            "scheduled_time": "14:00",
        }

    def make_request(self, endpoint: str, payload: dict = None) -> Dict:
        """Make a single API request"""
        start_time = time.time()
        try:
            if payload:
                response = requests.post(
                    f"{API_BASE_URL}{endpoint}", json=payload, timeout=30
                )
            else:
                response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=30)
            duration = time.time() - start_time
            return {
                "status": response.status_code,
                "duration": duration,
                "success": response.status_code < 400,
            }
        except Exception as e:
            return {
                "status": 0,
                "duration": time.time() - start_time,
                "success": False,
                "error": str(e),
            }

    @pytest.mark.performance
    def test_predict_endpoint_load(self, sample_payload):
        """Test /predict endpoint under load"""
        num_requests = 100
        max_workers = 50

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.make_request, "/predict", sample_payload)
                for _ in range(num_requests)
            ]
            results = [f.result() for f in futures]

        success_count = sum(1 for r in results if r["success"])
        durations = [r["duration"] for r in results if r["success"]]

        assert success_count >= num_requests * 0.95, (
            f"Success rate: {success_count / num_requests * 100}%"
        )

        if durations:
            avg_duration = sum(durations) / len(durations)
            p95 = sorted(durations)[int(len(durations) * 0.95)]
            print(f"Avg: {avg_duration:.3f}s, P95: {p95:.3f}s")

    @pytest.mark.performance
    def test_concurrent_requests(self, sample_payload):
        """Test concurrent request handling"""
        num_concurrent = 50

        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=num_concurrent
        ) as executor:
            futures = [
                executor.submit(self.make_request, "/predict", sample_payload)
                for _ in range(num_concurrent)
            ]
            results = [f.result() for f in futures]
        total_duration = time.time() - start_time

        success_count = sum(1 for r in results if r["success"])
        assert success_count >= num_concurrent * 0.9, (
            f"Success rate: {success_count / num_concurrent * 100}%"
        )
        print(
            f"Total duration for {num_concurrent} concurrent requests: {total_duration:.2f}s"
        )

    @pytest.mark.performance
    def test_sustained_load(self, sample_payload):
        """Test sustained load over time"""
        duration_seconds = 60
        requests_per_second = 10
        max_workers = 20

        start_time = time.time()
        results = []

        while time.time() - start_time < duration_seconds:
            batch_size = min(requests_per_second, max_workers)
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=batch_size
            ) as executor:
                futures = [
                    executor.submit(self.make_request, "/predict", sample_payload)
                    for _ in range(batch_size)
                ]
                results.extend([f.result() for f in futures])
            time.sleep(1)

        success_count = sum(1 for r in results if r["success"])
        print(f"Sustained load: {success_count}/{len(results)} successful")


class TestMLLoad:
    """Test ML model inference performance (Milestone 390)"""

    @pytest.mark.performance
    @pytest.mark.skip(reason="Requires ML service running")
    def test_model_inference_time(self):
        """Test model inference latency"""
        # Would test model inference time
        pass

    @pytest.mark.performance
    @pytest.mark.skip(reason="Requires ML service running")
    def test_batch_inference(self):
        """Test batch prediction performance"""
        pass
