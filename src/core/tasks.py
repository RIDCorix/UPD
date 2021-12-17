from typing import Tuple

class Task:
    def run(self, *args, **kwargs):
        pass

    def get_progress_info() -> Tuple[float, float]:
        pass

    def get_progress(self) -> float:
        current, all = self.get_progress_info
        return current / all
