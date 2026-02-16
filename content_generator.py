import random

class ContentGenerator:
    def __init__(self):
        self.code_snippets = [
            """def calculate_wpm(start_time, end_time, typed_chars):
    minutes = (end_time - start_time) / 60
    words = typed_chars / 5
    return words / minutes""",
            """class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)""",
            """const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello World!')
});"""
        ]
        
        self.log_snippets = [
            """[2024-05-20 10:00:01] INFO: Server started on port 8080
[2024-05-20 10:00:02] WARN: Low memory detected
[2024-05-20 10:00:03] DEBUG: User login attempt from 192.168.1.5
[2024-05-20 10:00:04] ERROR: Database connection failed
[2024-05-20 10:00:05] INFO: Retrying connection...""",
            """127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET /favicon.ico HTTP/1.0" 404 209"""
        ]
        
        self.shell_snippets = [
            "apt-get update && apt-get upgrade -y",
            "git commit -m 'Fix critical bug in production'",
            "docker run -d -p 80:80 nginx:latest",
            "kubectl get pods --all-namespaces"
        ]

        self.paragraph_snippets = [
            "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. How vexingly quick daft zebras jump.",
            "Programming is the art of telling another human what one wants the computer to do. Software is a great combination of artistry and engineering.",
            "In the middle of difficulty lies opportunity. The only way to do great work is to love what you do. Stay hungry, stay foolish.",
            "Technology is best when it brings people together. The advance of technology is based on making it fit in so that you do not even notice it.",
        ]

        self.line_snippets = [
            "The quick brown fox jumps over the lazy dog.",
            "To be or not to be, that is the question.",
            "All that glitters is not gold.",
            "A journey of a thousand miles begins with a single step.",
            "The only thing we have to fear is fear itself.",
            "In the beginning was the Word, and the Word was with God.",
            "It was the best of times, it was the worst of times.",
            "Not all those who wander are lost.",
        ]

    def get_timed_content(self, mode):
        """Get a long block of text for timed tests by joining multiple snippets."""
        snippets = {
            "code": self.code_snippets,
            "logs": self.log_snippets,
            "paragraph": self.paragraph_snippets,
            "line": self.line_snippets,
            "shell": self.shell_snippets,
        }
        pool = snippets.get(mode, self.paragraph_snippets)
        # Shuffle and join enough snippets so the user won't run out of text
        selected = []
        while len(" ".join(selected)) < 2000:
            selected.append(random.choice(pool))
        separator = "\n" if mode in ("code", "logs", "line", "shell") else " "
        return separator.join(selected)

    def get_snippet(self, mode):
        if mode == "code":
            return random.choice(self.code_snippets)
        elif mode == "logs":
            return random.choice(self.log_snippets)
        elif mode == "paragraph":
            return random.choice(self.paragraph_snippets)
        elif mode == "line":
            return random.choice(self.line_snippets)
        else:
            return random.choice(self.shell_snippets)
