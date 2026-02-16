import json
import os
import time
from datetime import datetime
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.align import Align
from rich.table import Table

STATS_FILE = os.path.join(os.path.dirname(__file__), "typing_history.json")


class StatsManager:
    def __init__(self):
        self.history = self._load()

    def _load(self):
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save(self):
        with open(STATS_FILE, "w") as f:
            json.dump(self.history, f, indent=2)

    def record(self, wpm, accuracy, chars_typed, elapsed, mode, time_limit):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "wpm": round(wpm, 1),
            "accuracy": round(accuracy, 1),
            "chars": chars_typed,
            "elapsed": round(elapsed, 1),
            "mode": mode,
            "time_limit": time_limit,
        }
        self.history.append(entry)
        self._save()

    def render_dashboard(self):
        if not self.history:
            return self._render_empty()

        entries = self.history
        wpms = [e["wpm"] for e in entries]
        accs = [e["accuracy"] for e in entries]

        total_tests = len(entries)
        avg_wpm = sum(wpms) / total_tests
        best_wpm = max(wpms)
        avg_acc = sum(accs) / total_tests
        best_acc = max(accs)
        total_chars = sum(e["chars"] for e in entries)
        total_time = sum(e["elapsed"] for e in entries)

        # Main Layout
        layout = Table.grid(padding=1, expand=True)
        
        # Title
        title = Text()
        title.append("\n")
        title.append("  ╔══════════════════════════════════════╗\n", style="bold cyan")
        title.append("  ║           YOUR STATS                 ║\n", style="bold cyan")
        title.append("  ╚══════════════════════════════════════╝\n", style="bold cyan")
        layout.add_row(Align.center(title))

        # Stats Grid
        stats_table = Table(box=None, padding=(0, 2), expand=True)
        stats_table.add_column("Metric", style="dim")
        stats_table.add_column("Value", style="bold white")
        stats_table.add_column("Metric", style="dim")
        stats_table.add_column("Value", style="bold white")

        stats_table.add_row("Tests Taken", str(total_tests), "Total Chars", f"{total_chars:,}")
        stats_table.add_row("Total Time", _fmt_time(total_time), "", "")
        stats_table.add_row("Avg WPM", f"{avg_wpm:.0f}", "Best WPM", f"{best_wpm:.0f}")
        stats_table.add_row("Avg Acc", f"{avg_acc:.1f}%", "Best Acc", f"{best_acc:.1f}%")
        
        layout.add_row(Panel(stats_table, title="Overview", border_style="blue"))

        # Combined WPM & Accuracy Bar Graph
        recent_wpms = wpms[-30:]
        recent_accs = accs[-30:]
        layout.add_row(Panel(
            render_bar_graph(recent_wpms, recent_accs),
            title="History",
            border_style="dim",
        ))

        # Recent Tests Table
        recent_table = Table(title="Recent Tests", box=None, padding=(0, 2), expand=True)
        recent_table.add_column("Date", style="dim")
        recent_table.add_column("WPM", style="bold white")
        recent_table.add_column("Acc", justify="right")
        recent_table.add_column("Mode", style="dim cyan")
        recent_table.add_column("Time", style="dim")

        recent = entries[-5:]
        for e in reversed(recent):
            ts = datetime.fromisoformat(e["timestamp"])
            date_str = ts.strftime("%b %d %H:%M")
            acc_style = "green" if e["accuracy"] >= 95 else "yellow" if e["accuracy"] >= 85 else "red"
            time_str = f"{e['time_limit']}s" if e["time_limit"] > 0 else f"{e['elapsed']:.0f}s"
            
            recent_table.add_row(
                date_str, 
                f"{e['wpm']:.0f}", 
                Text(f"{e['accuracy']:.0f}%", style=acc_style), 
                e["mode"],
                time_str
            )

        layout.add_row(Panel(recent_table, border_style="white"))

        layout.add_row(Align.center(Text("\nPress any key to go back", style="dim italic")))

        return Panel(
            layout,
            title="TYPEMASTER STATS",
            border_style="bright_cyan",
            padding=(1, 2),
        )

    def _render_empty(self):
        content = Text()
        content.append("\n\n")
        content.append("  No stats yet!\n\n", style="bold bright_yellow")
        content.append("  Take your first test to start tracking.\n\n", style="white")
        content.append("  Press any key to go back", style="dim italic")
        content.append("\n\n")

        return Panel(
            Align.center(content),
            title="TYPEMASTER STATS",
            border_style="bright_cyan",
            padding=(1, 2),
        )


def render_bar_graph(wpms, accs, height=8):
    """Render WPM and Accuracy as paired vertical bars on a single graph."""
    if not wpms:
        return Text("")

    n = len(wpms)

    # WPM scale (left axis)
    wpm_lo = max(0, min(wpms) - 10)
    wpm_hi = max(wpms) + 10
    wpm_range = wpm_hi - wpm_lo or 1

    # Accuracy scale (right axis, always 0-100)
    acc_range = 100

    # Bar heights (how many rows each bar fills, 1 to height)
    def bar_h(val, lo, rng):
        return max(1, round((val - lo) / rng * height))

    wpm_h = [bar_h(v, wpm_lo, wpm_range) for v in wpms]
    acc_h = [bar_h(v, 0, acc_range) for v in accs]

    result = Text()

    for row in range(height, 0, -1):
        # Left y-axis label (WPM)
        wpm_val = wpm_lo + (row / height) * wpm_range
        if row == height or row == 1 or row == height // 2:
            result.append(f"{wpm_val:>4.0f} ", style="green")
        else:
            result.append("     ", style="dim")

        result.append("│", style="dim")

        for col in range(n):
            # WPM bar
            if wpm_h[col] >= row:
                result.append("█", style="green")
            else:
                result.append(" ")
            # Accuracy bar
            if acc_h[col] >= row:
                result.append("█", style="yellow")
            else:
                result.append(" ")
            # Gap between pairs
            if col < n - 1:
                result.append(" ")

        result.append("│", style="dim")

        # Right y-axis label (Accuracy)
        acc_val = (row / height) * 100
        if row == height or row == 1 or row == height // 2:
            result.append(f" {acc_val:>3.0f}%", style="yellow")
        else:
            result.append("     ", style="dim")

        result.append("\n")

    # Bottom axis
    result.append("     └", style="dim")
    result.append("─" * (n * 3 - 1), style="dim")
    result.append("┘\n", style="dim")

    # Legend
    result.append("      ")
    result.append("█ WPM", style="bold green")
    result.append("   ")
    result.append("█ Accuracy", style="bold yellow")

    return result


def _fmt_time(seconds):
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        m = int(seconds // 60)
        s = int(seconds % 60)
        return f"{m}m {s}s"
    else:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        return f"{h}h {m}m"
