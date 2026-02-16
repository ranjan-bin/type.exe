import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.console import Group
from input_handler import InputHandler


CONTENT_TYPES = [
    ("1", "code", "Code Snippets"),
    ("2", "paragraph", "Paragraphs"),
    ("3", "line", "Single Lines"),
    ("4", "logs", "Log Entries"),
    ("5", "shell", "Shell Commands"),
]

TEST_TYPES = [
    ("1", 0, "Completion (type the full text)"),
    ("2", 15, "15 seconds"),
    ("3", 30, "30 seconds"),
    ("4", 60, "60 seconds"),
]

MAIN_MENU = [
    ("1", "test", "Take a Test"),
    ("2", "stats", "View Stats"),
    ("3", "quit", "Quit"),
]


def show_main_menu(console, input_handler):
    """Returns 'test', 'stats', or None (quit)."""
    title = Text()
    title.append("╔══════════════════════════════════════╗\n", style="bold cyan")
    title.append("║           TYPEMASTER                 ║\n", style="bold cyan")
    title.append("╚══════════════════════════════════════╝\n", style="bold cyan")
    title.append("\n", style="white")
    for key, _, label in MAIN_MENU:
        title.append(f"  [{key}] ", style="bold yellow")
        title.append(f"{label}\n", style="white")
    title.append("\nPress ", style="dim")
    title.append("ESC", style="dim bold")
    title.append(" to quit", style="dim")

    panel = Panel(
        Align.center(title),
        border_style="cyan",
        padding=(1, 4),
    )

    result = _get_selection(console, input_handler, panel, {k: v for k, v, _ in MAIN_MENU})
    if result in (None, "quit"):
        return None
    return result


def pick_test_options(console, input_handler):
    """Returns (mode, time_limit) or (None, None) if cancelled."""
    mode = _pick_content_type(console, input_handler)
    if mode is None:
        return None, None

    time_limit = _pick_test_type(console, input_handler)
    if time_limit is None:
        return None, None

    return mode, time_limit


def show_stats_screen(console, input_handler, stats_manager):
    """Show the stats dashboard and wait for a keypress to return."""
    input_handler.start()
    try:
        input_handler.flush()
        console.clear()
        console.print(stats_manager.render_dashboard())
        while True:
            char = input_handler.get_char()
            if char:
                break
            time.sleep(0.01)
    finally:
        input_handler.stop()


def _pick_content_type(console, input_handler):
    title = Text()
    title.append("TYPEMASTER", style="bold cyan")
    title.append("\n\nPick a content type:\n\n", style="white")
    for key, _, label in CONTENT_TYPES:
        title.append(f"  [{key}] ", style="bold yellow")
        title.append(f"{label}\n", style="white")
    title.append("\nPress ", style="dim")
    title.append("ESC", style="dim bold")
    title.append(" to go back", style="dim")

    panel = Panel(
        Align.center(title),
        border_style="cyan",
        padding=(1, 4),
    )

    return _get_selection(console, input_handler, panel, {k: v for k, v, _ in CONTENT_TYPES})


def _pick_test_type(console, input_handler):
    title = Text()
    title.append("TYPEMASTER", style="bold cyan")
    title.append("\n\nPick a test type:\n\n", style="white")
    for key, _, label in TEST_TYPES:
        title.append(f"  [{key}] ", style="bold yellow")
        title.append(f"{label}\n", style="white")
    title.append("\nPress ", style="dim")
    title.append("ESC", style="dim bold")
    title.append(" to go back", style="dim")

    panel = Panel(
        Align.center(title),
        border_style="cyan",
        padding=(1, 4),
    )

    return _get_selection(console, input_handler, panel, {k: v for k, v, _ in TEST_TYPES})


def _get_selection(console, input_handler, panel, options):
    input_handler.start()
    try:
        input_handler.flush()
        console.clear()
        console.print(panel)
        while True:
            char = input_handler.get_char()
            if char is None:
                time.sleep(0.01)
                continue
            if char in ('\x1b', '\x03'):
                return None
            if char in options:
                return options[char]
    finally:
        input_handler.stop()
