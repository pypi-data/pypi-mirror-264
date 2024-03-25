from typing import List

from cuckoo.base import Observer
from cuckoo.handler.watcher_handler import WatcherHandler
from cuckoo.utils import DISPLAY_CONSOLE


class HandlerManager:
    @staticmethod
    def get_displays(display_items: List[dict]) -> List[Observer]:
        displays: List[Observer] = []
        for item in display_items:
            if DISPLAY_CONSOLE in item:
                displays.append(WatcherHandler())
        return displays
