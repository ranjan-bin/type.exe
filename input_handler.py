import sys
import tty
import termios
import select

class InputHandler:
    def __init__(self):
        self.fd = sys.stdin.fileno()
        try:
            self.old_settings = termios.tcgetattr(self.fd)
        except termios.error:
            self.old_settings = None

    def start(self):
        # Set cbreak mode (character-by-character input, no echo, but keeps output processing)
        # Using setraw() would disable OPOST, which breaks Rich's terminal rendering
        try:
            tty.setcbreak(sys.stdin.fileno())
        except termios.error:
            pass

    def stop(self):
        # Restore old settings
        if self.old_settings is not None:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

    def flush(self):
        """Discard any unread input sitting in the stdin buffer."""
        try:
            termios.tcflush(self.fd, termios.TCIFLUSH)
        except termios.error:
            pass

    def get_char(self):
        # Non-blocking check
        if select.select([sys.stdin], [], [], 0)[0]:
            ch = sys.stdin.read(1)
            return ch
        return None
