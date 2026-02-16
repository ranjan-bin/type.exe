import unittest
from game_engine import GameEngine
import time

class TestGameMechanics(unittest.TestCase):
    def test_wpm_calculation(self):
        engine = GameEngine()
        engine.start_time = time.time() - 60  # 1 minute ago
        engine.user_input = "word " * 60  # 60 words (assuming 5 chars per word + space)
        # Actually WPM def is usually chars/5. "word " is 5 chars.
        # So 300 chars.
        
        engine.update_stats()
        # 300 chars / 5 = 60 words.
        # 60 seconds = 1 minute.
        # WPM should be 60.
        
        self.assertAlmostEqual(engine.wpm, 60.0, delta=1.0)

    def test_accuracy_calculation(self):
        engine = GameEngine()
        engine.target_text = "hello world"
        engine.user_input = "hello wrrld"
        
        engine.update_stats()
        # hello w (7 chars match)
        # r (mismatch)
        # rld (3 chars match?) 
        # Wait, simple index comparison:
        # 0:h-h(y), 1:e-e(y), 2:l-l(y), 3:l-l(y), 4:o-o(y), 5: - (y), 6:w-w(y)
        # 7:o-r(n), 8:r-r(y), 9:l-l(y), 10:d-d(y)
        # Hits: 10. Length: 11.
        # Acc: 10/11 * 100 = 90.909...
        
        self.assertAlmostEqual(engine.accuracy, (10/11)*100, delta=0.1)

    def test_backspace(self):
        engine = GameEngine()
        engine.target_text = "abc"
        engine.user_input = "ab"
        engine.handle_input('d') # user writes 'abd'
        self.assertEqual(engine.user_input, "abd")
        
        engine.handle_input('\x7f') # Backspace
        self.assertEqual(engine.user_input, "ab")

if __name__ == '__main__':
    unittest.main()
