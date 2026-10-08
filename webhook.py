"""
Webhook notifier untuk Discord / Slack / generic.
Semua kegagalan senyap (tidak boleh menggagalkan batch).
"""
import time
import threading
import requests
from urllib.parse import urlparse


# ============================================================
# DETEKSI PLATFORM
# ============================================================
def detect_platform(url):
    if not url:
        return "generic"
    host = urlparse(url).netloc.lower()
    if "discord.com" in host or "discordapp.com" in host:
        return "discord"
    if "slack.com" in host or "hooks.slack.com" in host:
        return "slack"
    return "generic"


def mask_url(url):
    if not url:
        return ""
    try:
        p = urlparse(url)
        return f"{p.scheme}://{p.netloc}/…{p.path[-10:]}"
    except Exception:
        return "***"


# ============================================================
# PAYLOAD BUILDERS
# ============================================================
def _build_discord_payload(event, data):
    colors = {
        "start":    0x3B82F6,
        "progress": 0x8B5CF6,
        "file":     0x10B981,
        "done":     0x10B981,
        "error":    0xEF4444,
    }
    icons = {
        "start": "🚀", "progress": "⏳",
        "file": "✅", "done": "🎉", "error": "❌",
    }

    title = f"{icons.get(event, '•')} "

    if event == "start":
        title += "Batch Dimulai"
        fields = [
            {"name": "Total File", "value": str(data.get("total_files", 0)), "inline": True},
            {"name": "Mode", "value": data.get("mode", "Clean"), "inline": True},
        ]
    elif event == "file":
        title += f"File Selesai: {data.get('file_name', 'file')}"
        fields = [
            {"name": "Metadata Dihapus", "value": str(data.get("removed_count", 0)), "inline": True},
            {"name": "Durasi", "value": data.get("duration_str", "—"), "inline": True},
        ]
    elif event == "done":
        title += "Batch Selesai"
        fields = [
            {"name": "Total File", "value": str(data.get("total_files", 0)), "inline": True},
            {"name": "Metadata Dihapus", "value": str(data.get("total_removed", 0)), "inline": True},
            {"name": "Durasi", "value": data.get("duration_str", "—"), "inline": True},
            {"name": "Sukses", "value": str(data.get("files_done", 0)), "inline": True},
            {"name": "Gagal", "value": str(data.get("files_failed", 0)), "inline": True},
            {"name": "Skip", "value": str(data.get("files_skipped", 0)), "inline": True},
        ]
    elif event == "error":
        title += "Batch Gagal"
        fields = [
            {"name": "Pesan", "value": str(data.get("error", "—"))[:200], "inline": False},
        ]
    else:
        fields = []

    embed = {
        "title": title,
        "color": colors.get(event, 0x94A3B8),
        "fields": fields,
        "footer": {"text": "Metadata Remover"},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    return {"embeds": [embed]}


def _build_slack_payload(event, data):
    icons = {"start": "🚀", "done": "🎉", "file": "✅", "error": "❌"}
    icon = icons.get(event, "•")

    if event == "start":
        title = f"{icon} *Batch Dimulai*"
        text = f"Total: {data.get('total_files', 0)} file"
    elif event == "file":
        title = f"{icon} File: `{data.get('file_name', '')}`"
        text = f"{data.get('removed_count', 0)} metadata dihapus ({data.get('duration_str', '—')})"
    elif event == "done":
        title = f"{icon} *Batch Selesai*"
        text = (
            f"Total: {data.get('total_files', 0)} file · "
            f"{data.get('total_removed', 0)} metadata dihapus · "
            f"Durasi: {data.get('duration_str', '—')}"
        )
    else:
        title = f"{icon} Batch: {event}"
        text = str(data)[:300]

    return {"text": f"{title}\n{text}"}


def _build_generic_payload(event, data):
    return {
        "event": event,
        "source": "metadata_remover",
        "data": {k: v for k, v in data.items() if not k.startswith("_")},
        "timestamp": time.time(),
    }


def build_payload(url, event, data):
    platform = detect_platform(url)
    if platform == "discord":
        return _build_discord_payload(event, data)
    if platform == "slack":
        return _build_slack_payload(event, data)
    return _build_generic_payload(event, data)


# ============================================================
# SENDER
# ============================================================
def send_webhook_notification(webhook_url, event, data, timeout=5):
    """Kirim notifikasi ke webhook. Non-blocking, kegagalan senyap."""
    if not webhook_url or not webhook_url.strip():
        return (False, "no_url")

    def _worker():
        try:
            payload = build_payload(webhook_url, event, data)
            r = requests.post(webhook_url, json=payload, timeout=timeout)
            if r.status_code not in (200, 204):
                return
        except Exception:
            pass

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
    return (True, "sent")


def test_webhook(webhook_url):
    return send_webhook_notification(
        webhook_url, "start",
        {"total_files": 0, "mode": "Test Connection"},
    )


def validate_webhook_url(url):
    if not url or not url.strip():
        return True, None
    try:
        p = urlparse(url.strip())
        if p.scheme not in ("http", "https"):
            return False, "URL harus dimulai dengan http:// atau https://"
        if not p.netloc:
            return False, "URL tidak valid (host kosong)."
        return True, None
    except Exception as e:
        return False, f"URL tidak valid: {e}"