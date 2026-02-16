from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.align import Align
from rich.table import Table
from rich.columns import Columns

class UIRenderer:
    def __init__(self, mode):
        self.mode = mode

    def render_screen(self, target_text, user_input, wpm, accuracy, time_remaining=0):
        if self.mode == "code":
            return self.render_code_mode(target_text, user_input, wpm, accuracy, time_remaining)
        elif self.mode == "logs":
            return self.render_logs_mode(target_text, user_input, wpm, accuracy, time_remaining)
        elif self.mode == "paragraph":
            return self.render_paragraph_mode(target_text, user_input, wpm, accuracy, time_remaining)
        elif self.mode == "line":
            return self.render_line_mode(target_text, user_input, wpm, accuracy, time_remaining)
        else:
            return self.render_shell_mode(target_text, user_input, wpm, accuracy, time_remaining)

    def _build_typed_content(self, target_text, user_input, correct_style="green", error_style="white on red", remaining_style="dim white"):
        content = Text()
        min_len = min(len(target_text), len(user_input))

        for i in range(min_len):
            if user_input[i] == target_text[i]:
                content.append(target_text[i], style=correct_style)
            else:
                content.append(target_text[i], style=error_style)

        if len(user_input) < len(target_text):
            content.append(target_text[min_len], style="reverse blink")
            content.append(target_text[min_len+1:], style=remaining_style)

        return content

    def _timer_text(self, time_remaining):
        if time_remaining > 0:
            return f" | Time: {time_remaining:.0f}s"
        return ""

    def render_code_mode(self, target_text, user_input, wpm, accuracy, time_remaining):
        content = self._build_typed_content(target_text, user_input)
        timer = self._timer_text(time_remaining)
        status = f" NORMAL  | main.py | python | WPM: {wpm:3.0f} | ACC: {accuracy:3.0f}%{timer} | Ln {len(user_input)//50 + 1}, Col {len(user_input)%50}"

        return Panel(
            Group(
                content,
                Align.right(Text(status, style="bold black on blue"))
            ),
            title="vim: /src/backend/engine.py",
            border_style="blue",
            padding=(1, 2)
        )

    def render_logs_mode(self, target_text, user_input, wpm, accuracy, time_remaining):
        content = self._build_typed_content(target_text, user_input, correct_style="grey70", error_style="red", remaining_style="dim grey30")
        timer = self._timer_text(time_remaining)

        return Panel(
            content,
            title="tail -f /var/log/syslog",
            border_style="green",
            subtitle=f"WPM: {wpm:.0f} | ACC: {accuracy:.0f}%{timer}"
        )

    def render_shell_mode(self, target_text, user_input, wpm, accuracy, time_remaining):
        content = Text()
        content.append("$ ", style="bold green")

        typed = self._build_typed_content(target_text, user_input, correct_style="white")
        content.append_text(typed)
        timer = self._timer_text(time_remaining)

        return Panel(
            content,
            title="user@server:~$",
            border_style="yellow",
            subtitle=f"WPM: {wpm:.0f} | ACC: {accuracy:.0f}%{timer}"
        )

    def render_paragraph_mode(self, target_text, user_input, wpm, accuracy, time_remaining):
        content = self._build_typed_content(target_text, user_input)
        timer = self._timer_text(time_remaining)
        status = f"WPM: {wpm:.0f} | ACC: {accuracy:.0f}%{timer} | {len(user_input)}/{len(target_text)} chars"

        return Panel(
            Group(
                content,
                Text(""),
                Align.center(Text(status, style="bold cyan"))
            ),
            title="Type the Paragraph",
            border_style="cyan",
            padding=(1, 2)
        )

    def render_line_mode(self, target_text, user_input, wpm, accuracy, time_remaining):
        content = self._build_typed_content(target_text, user_input)
        timer = self._timer_text(time_remaining)

        return Panel(
            Align.center(content),
            title="Type the Line",
            border_style="magenta",
            subtitle=f"WPM: {wpm:.0f} | ACC: {accuracy:.0f}%{timer}",
            padding=(1, 2)
        )

    def render_results(self, wpm, accuracy, chars_typed, elapsed, time_limit):
        rank, rank_style, bar_fill = self._get_rank(wpm, accuracy)

        bar_len = 40
        filled = min(bar_len, int((wpm / 150) * bar_len))
        bar = "█" * filled + "░" * (bar_len - filled)

        # Build the results display
        content = Text()
        content.append("\n")
        content.append("  ╔══════════════════════════════════════╗\n", style="bold yellow")
        content.append("  ║         RACE COMPLETE!               ║\n", style="bold yellow")
        content.append("  ╚══════════════════════════════════════╝\n", style="bold yellow")
        content.append("\n")

        # Rank display
        content.append("  Your Rank:  ", style="white")
        content.append(f"{rank}\n\n", style=f"bold {rank_style}")

        # Stats table
        content.append("  Speed       ", style="dim")
        content.append(f"{wpm:.0f} WPM\n", style="bold white")
        content.append("              ", style="dim")
        content.append(f"{bar}\n\n", style=rank_style)

        content.append("  Accuracy    ", style="dim")
        acc_style = "green" if accuracy >= 95 else "yellow" if accuracy >= 85 else "red"
        content.append(f"{accuracy:.1f}%\n", style=f"bold {acc_style}")

        # Accuracy bar
        acc_bar_filled = min(bar_len, int((accuracy / 100) * bar_len))
        acc_bar = "█" * acc_bar_filled + "░" * (bar_len - acc_bar_filled)
        content.append("              ", style="dim")
        content.append(f"{acc_bar}\n\n", style=acc_style)

        content.append("  Characters  ", style="dim")
        content.append(f"{chars_typed}\n", style="bold white")

        content.append("  Time        ", style="dim")
        if time_limit > 0:
            content.append(f"{time_limit}s (timed)\n", style="bold white")
        else:
            content.append(f"{elapsed:.1f}s\n", style="bold white")

        content.append("\n")
        content.append("  Press any key to exit", style="dim italic")
        content.append("\n")

        return Panel(
            content,
            title="RESULTS",
            border_style=rank_style,
            padding=(1, 2)
        )

    def _get_rank(self, wpm, accuracy):
        score = wpm * (accuracy / 100)
        if score >= 100:
            return "LEGENDARY", "bright_magenta", 1.0
        elif score >= 70:
            return "SPEED DEMON", "bright_red", 0.85
        elif score >= 50:
            return "SWIFT TYPER", "bright_yellow", 0.7
        elif score >= 30:
            return "STEADY HANDS", "bright_green", 0.5
        elif score >= 15:
            return "WARMING UP", "bright_cyan", 0.3
        else:
            return "BEGINNER", "white", 0.15
