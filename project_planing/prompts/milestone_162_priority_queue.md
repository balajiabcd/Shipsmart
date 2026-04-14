# Milestone #162: Build Priority Queue System

**Status:** COMPLETED

**Your Role:** AI/LLM Engineer

**Instructions:**
Create priority queue for handling multiple orders:

```python
# decision_engine/priority_queue.py

import heapq
from dataclasses import dataclass
from typing import List

@dataclass
class QueueItem:
    priority: int
    delivery_id: str
    timestamp: float
    context: dict
    
    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.timestamp < other.timestamp

class DeliveryPriorityQueue:
    def __init__(self):
        self.queue: List[QueueItem] = []
        self.handled = set()
    
    def enqueue(self, delivery_id: str, context: dict):
        priority = self._calculate_priority(delivery_id, context)
        item = QueueItem(
            priority=priority,
            delivery_id=delivery_id,
            timestamp=time.time(),
            context=context
        )
        heapq.heappush(self.queue, item)
    
    def _calculate_priority(self, delivery_id: str, context: dict) -> int:
        delay_prob = context.get("delay_probability", 0)
        priority = int((1 - delay_prob) * 100)
        
        if context.get("is_fragile"):
            priority -= 10
        if context.get("customer_tier") == "premium":
            priority -= 20
        if context.get("delivery_window_ends_soon"):
            priority -= 30
        
        return max(1, min(100, priority))
    
    def dequeue(self) -> QueueItem:
        while self.queue:
            item = heapq.heappop(self.queue)
            if item.delivery_id not in self.handled:
                return item
        return None
    
    def get_next_batch(self, batch_size: int = 50) -> List[QueueItem]:
        batch = []
        for _ in range(batch_size):
            item = self.dequeue()
            if item:
                batch.append(item)
                self.handled.add(item.delivery_id)
            else:
                break
        return batch
```

**Completed:**
- Created `src/decision_engine/priority_queue.py` with:
  - `QueueItem` dataclass
  - `DeliveryPriorityQueue` class
  - `_calculate_priority()` - Priority calculation
  - `dequeue()` - Get next item
  - `get_next_batch()` - Batch processing
  - `get_high_risk_deliveries()` - Risk filtering

**Next Milestone:** Proceed to #163 - Cost Benefit Analysis

---

## Section 3: Instructions for Next AI Agent

Proceed to Milestone #163: Create Cost-Benefit Analysis
- Calculate ROI for interventions
- Optimize decision-making