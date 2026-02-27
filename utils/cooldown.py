import time
from typing import Dict

class CooldownManager:
    def __init__(self) -> None:
        self._cooldowns: Dict[int, float] = {}

    def is_on_cooldown(self, chat_id: int, cooldown_seconds: int) -> bool:
        current_time = time.monotonic()
        last_time = self._cooldowns.get(chat_id, 0.0)
        
        return (current_time - last_time) < cooldown_seconds

    def set_cooldown(self, chat_id: int) -> None:
        self._cooldowns[chat_id] = time.monotonic()

    def check_and_set(self, chat_id: int, cooldown_seconds: int) -> bool:
        if self.is_on_cooldown(chat_id, cooldown_seconds):
            return False
            
        self.set_cooldown(chat_id)
        return True

cooldown_manager = CooldownManager()