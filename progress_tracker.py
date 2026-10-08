"""
Tracker untuk progress batch: ETA, log per-file, statistik real-time.
"""
import time
from dataclasses import dataclass, field
from typing import Optional


def humanize_duration(seconds):
    if seconds is None or seconds < 0:
        return "—"
    if seconds < 1:
        return "< 1 detik"
    if seconds < 60:
        return f"{int(round(seconds))} detik"
    if seconds < 3600:
        m = int(seconds // 60)
        s = int(seconds % 60)
        return f"{m} menit {s} detik"
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    return f"{h} jam {m} menit"


@dataclass
class FileProgressEntry:
    name: str
    status: str           # 'ok' | 'error' | 'skipped'
    removed_count: int
    duration: float
    error: Optional[str] = None


@dataclass
class BatchProgress:
    total_files: int = 0
    current_index: int = 0
    current_name: str = ""
    start_time: float = 0.0
    end_time: float = 0.0
    total_removed: int = 0
    files_done: int = 0
    files_failed: int = 0
    files_skipped: int = 0
    log: list = field(default_factory=list)
    phase: str = "idle"      # 'idle' | 'scan' | 'clean' | 'done'
    start_notified: bool = False
    end_notified: bool = False

    def start_batch(self, total_files, phase="clean"):
        self.total_files = total_files
        self.current_index = 0
        self.start_time = time.time()
        self.end_time = 0.0
        self.total_removed = 0
        self.files_done = 0
        self.files_failed = 0
        self.files_skipped = 0
        self.log = []
        self.phase = phase
        self.start_notified = False
        self.end_notified = False

    # Alias untuk kompatibilitas
    def start(self, total_files, phase="clean"):
        self.start_batch(total_files, phase)

    def set_current(self, index, name):
        self.current_index = index
        self.current_name = name

    def add_result(self, name, status, removed_count=0, duration=0.0, error=None):
        entry = FileProgressEntry(
            name=name, status=status,
            removed_count=removed_count,
            duration=duration, error=error,
        )
        self.log.append(entry)
        if status == "ok":
            self.files_done += 1
            self.total_removed += removed_count
        elif status == "error":
            self.files_failed += 1
        else:
            self.files_skipped += 1

    def finish(self):
        self.end_time = time.time()
        self.phase = "done"

    @property
    def elapsed(self):
        if not self.start_time:
            return 0.0
        end = self.end_time if self.end_time else time.time()
        return end - self.start_time

    @property
    def processed(self):
        return len(self.log)

    @property
    def pct(self):
        if self.total_files == 0:
            return 0
        return int((self.processed / self.total_files) * 100)

    @property
    def avg_per_file(self):
        if self.processed == 0:
            return 0.0
        return self.elapsed / self.processed

    @property
    def eta(self):
        remaining = self.total_files - self.processed
        if remaining <= 0:
            return 0.0
        if self.avg_per_file <= 0:
            return None
        return self.avg_per_file * remaining

    def to_dict(self):
        return {
            "total_files": self.total_files,
            "processed": self.processed,
            "pct": self.pct,
            "elapsed": self.elapsed,
            "eta": self.eta,
            "avg_per_file": self.avg_per_file,
            "current_name": self.current_name,
            "current_index": self.current_index,
            "total_removed": self.total_removed,
            "files_done": self.files_done,
            "files_failed": self.files_failed,
            "files_skipped": self.files_skipped,
            "log": self.log,
            "phase": self.phase,
        }