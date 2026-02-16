import sys
from rich.console import Console
from game_engine import GameEngine
from menu import show_main_menu, pick_test_options, show_stats_screen
from input_handler import InputHandler
from stats import StatsManager

def main():
    console = Console()
    input_handler = InputHandler()
    stats_manager = StatsManager()

    try:
        while True:
            choice = show_main_menu(console, input_handler)

            if choice is None:
                console.clear()
                print("Bye!")
                break

            if choice == "test":
                mode, time_limit = pick_test_options(console, input_handler)
                if mode is None:
                    continue
                engine = GameEngine(mode=mode, time_limit=time_limit, stats_manager=stats_manager)
                engine.run()

            elif choice == "stats":
                show_stats_screen(console, input_handler, stats_manager)

    except KeyboardInterrupt:
        print("\nBye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
