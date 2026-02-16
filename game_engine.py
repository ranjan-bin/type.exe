import time
from rich.live import Live
from rich.console import Console
from ui_renderer import UIRenderer
from content_generator import ContentGenerator

from input_handler import InputHandler

class GameEngine:
    def __init__(self, mode="code", time_limit=0, stats_manager=None):
        self.mode = mode
        self.time_limit = time_limit
        self.stats_manager = stats_manager
        self.console = Console()
        self.renderer = UIRenderer(mode)
        self.content_gen = ContentGenerator()
        self.input_handler = InputHandler()
        self.running = False

        # Game State
        self.target_text = ""
        self.user_input = ""
        self.start_time = 0
        self.wpm = 0.0
        self.accuracy = 100.0
        self.completed = False
        self.time_remaining = time_limit

    def run(self):
        self.running = True
        if self.time_limit > 0:
            self.target_text = self.content_gen.get_timed_content(self.mode)
        else:
            self.target_text = self.content_gen.get_snippet(self.mode)
        self.start_time = time.time()

        self.input_handler.start()
        try:
            with Live(self._render(), refresh_per_second=20, screen=True) as live:
                while self.running:
                    char = self.input_handler.get_char()
                    if char:
                        self.handle_input(char)

                    if not self.completed:
                        self.update_stats()

                    # Check time limit
                    if self.time_limit > 0:
                        elapsed = time.time() - self.start_time
                        self.time_remaining = max(0, self.time_limit - elapsed)
                        if self.time_remaining <= 0:
                            self.completed = True

                    live.update(self._render())

                    if self.completed:
                        elapsed = time.time() - self.start_time
                        self._show_results(live, elapsed)
                        break

                    time.sleep(0.01)
        finally:
            self.input_handler.stop()

    def _show_results(self, live, elapsed):
        # Save stats before showing results
        if self.stats_manager and len(self.user_input) > 0:
            self.stats_manager.record(
                self.wpm, self.accuracy,
                len(self.user_input), elapsed,
                self.mode, self.time_limit,
            )

        results = self.renderer.render_results(
            self.wpm, self.accuracy,
            len(self.user_input), elapsed, self.time_limit
        )
        live.update(results)
        live.refresh()
        # Cooldown: ignore all input for 1.5s so fast fingers don't dismiss results
        time.sleep(1.5)
        self.input_handler.flush()
        # Now wait for a deliberate keypress
        while True:
            char = self.input_handler.get_char()
            if char:
                break
            time.sleep(0.01)

    def _render(self):
        return self.renderer.render_screen(
            self.target_text, self.user_input,
            self.wpm, self.accuracy, self.time_remaining
        )

    def handle_input(self, char):
        if char == '\x03' or char == '\x1b':
            self.running = False
            return

        # Backspace: \x7f or \x08
        if char == '\x7f' or char == '\x08':
            if len(self.user_input) > 0:
                self.user_input = self.user_input[:-1]
            return

        # Translate carriage return to newline (Enter key may send \r)
        if char == '\r':
            char = '\n'

        # Normal typing
        if len(self.user_input) < len(self.target_text):
            self.user_input += char

        # Check completion (only in non-timed mode)
        if self.time_limit == 0 and self.user_input == self.target_text:
            self.completed = True

    def update_stats(self):
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            words = len(self.user_input) / 5
            self.wpm = (words / elapsed) * 60

        # Calculate accuracy
        if len(self.user_input) > 0:
            hits = 0
            for i, c in enumerate(self.user_input):
                 if i < len(self.target_text) and c == self.target_text[i]:
                     hits += 1
            self.accuracy = (hits / len(self.user_input)) * 100
        else:
            self.accuracy = 100.0
