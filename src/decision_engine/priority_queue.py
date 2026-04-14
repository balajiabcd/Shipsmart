import os
import heapq
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class QueueItem:
    priority: int
    delivery_id: str
    timestamp: float
    context: Dict = field(default_factory=dict)
    risk_level: str = "low"

    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.timestamp < other.timestamp


class DeliveryPriorityQueue:
    def __init__(self):
        self.queue: List[QueueItem] = []
        self.handled = set()

    def enqueue(self, delivery_id: str, context: Dict):
        """Add delivery to priority queue"""

        priority = self._calculate_priority(delivery_id, context)
        risk_level = self._classify_risk(context.get("delay_probability", 0))

        item = QueueItem(
            priority=priority,
            delivery_id=delivery_id,
            timestamp=datetime.now().timestamp(),
            context=context,
            risk_level=risk_level,
        )

        heapq.heappush(self.queue, item)
        logger.info(f"Enqueued {delivery_id} with priority {priority}")

    def _calculate_priority(self, delivery_id: str, context: Dict) -> int:
        """Calculate priority score (higher = more urgent)"""

        delay_prob = context.get("delay_probability", 0)

        priority = int((1 - delay_prob) * 100)

        if context.get("is_fragile", False):
            priority -= 10

        if context.get("customer_tier") == "premium":
            priority -= 20

        if context.get("delivery_window_ends_soon", False):
            priority -= 30

        if context.get("urgent", False):
            priority -= 25

        if context.get("is_holiday", False):
            priority -= 15

        return max(1, min(100, priority))

    def _classify_risk(self, prob: float) -> str:
        """Classify risk level"""

        if prob > 0.7:
            return "high"
        elif prob > 0.4:
            return "medium"
        else:
            return "low"

    def dequeue(self) -> Optional[QueueItem]:
        """Get next highest priority item"""

        while self.queue:
            item = heapq.heappop(self.queue)
            if item.delivery_id not in self.handled:
                return item
        return None

    def get_next_batch(self, batch_size: int = 50) -> List[QueueItem]:
        """Get batch of deliveries to process"""

        batch = []

        for _ in range(batch_size):
            item = self.dequeue()
            if item:
                batch.append(item)
                self.handled.add(item.delivery_id)
            else:
                break

        logger.info(f"Retrieved batch of {len(batch)} deliveries")
        return batch

    def peek(self) -> Optional[QueueItem]:
        """View next item without removing"""

        if self.queue:
            return self.queue[0]
        return None

    def get_high_risk_deliveries(self, min_delay_prob: float = 0.7) -> List[QueueItem]:
        """Get all high-risk deliveries"""

        high_risk = []

        for item in self.queue:
            if item.delivery_id not in self.handled:
                delay_prob = item.context.get("delay_probability", 0)
                if delay_prob >= min_delay_prob:
                    high_risk.append(item)

        return sorted(
            high_risk, key=lambda x: x.context.get("delay_probability", 0), reverse=True
        )

    def get_size(self) -> int:
        """Get queue size"""

        return len(self.queue)

    def is_empty(self) -> bool:
        """Check if queue is empty"""

        return len(self.queue) == 0

    def mark_handled(self, delivery_id: str):
        """Mark delivery as handled"""

        self.handled.add(delivery_id)
        logger.info(f"Marked {delivery_id} as handled")

    def unmark_handled(self, delivery_id: str):
        """Unmark delivery (for re-queueing)"""

        if delivery_id in self.handled:
            self.handled.remove(delivery_id)

    def clear(self):
        """Clear the queue"""

        self.queue.clear()
        self.handled.clear()
        logger.info("Cleared priority queue")


def create_priority_queue_from_predictions(
    predictions: List[Dict],
) -> DeliveryPriorityQueue:
    """Create priority queue from list of predictions"""

    queue = DeliveryPriorityQueue()

    for pred in predictions:
        delivery_id = pred.get("delivery_id", "unknown")
        queue.enqueue(delivery_id, pred)

    logger.info(f"Created queue with {queue.get_size()} deliveries")
    return queue
