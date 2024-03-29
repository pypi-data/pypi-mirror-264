"""
This module is responsible for creating panels for the chatbox and other components. 
It uses the rich library to create panels.
"""
from typing import Any
from rich.panel import Panel
from rich.console import Console
from rich.columns import Columns
from rich.align import Align
from rich.text import Text
from rich.status import Status


class PanelBase:
    """This class is responsible for creating panels for the chatbox and other components."""

    def __init__(self, title, width=50) -> None:
        self.title: str = title
        self.width: int = width
        self.console = Console()
        self._queue = Queue()

    def _create_base_panel(self) -> Panel:
        """Create a base panel for the chatbox."""
        chatboxes = self._queue.queue
        return Panel(
            Columns(chatboxes), title=self.title, expand=True,
            border_style="cyan", padding=(1, 1), title_align="center"
        )

    def _cache_content(self, content: Panel) -> None:
        """Cache the content of the chatbox."""
        self._queue.enqueue(content)

    def create_chatbox(self, title: str, content: str, width=100, is_ai=True) -> Panel:
        """Create a chatbox panel."""
        content = Text(content, overflow="fold")
        if not is_ai:
            chatbox: Panel = Panel.fit(content, width=width,
                                       title=title, border_style="blue", title_align="left")
            aligned_chatbox: Align = Align.left(chatbox, width=50)
        else:
            chatbox = Panel.fit(content, width=width,
                                title=title, border_style="green", title_align="right")
            aligned_chatbox = Align.right(chatbox, width=50)

        self._cache_content(aligned_chatbox)
        return chatbox

    def print_stdout(self) -> None:
        """Print the panel."""
        if self._queue.size() > 0:
            self.console.print(self._create_base_panel())

    def create_status(self, text: str, spinner: str) -> Status:
        """Create a status panel."""
        return Status(text, spinner=spinner)


class Queue:
    """A simple Queue class."""

    def __init__(self) -> None:
        self.queue = []

    def enqueue(self, item) -> None:
        """Add an item to the end of the queue."""
        self.queue.append(item)

    def dequeue(self) -> Any | None:
        """Remove an item from the front of the queue."""
        if not self.is_empty():
            return self.queue.pop(0)
        return None

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self.queue) == 0

    def size(self) -> int:
        """Get the size of the queue."""
        return len(self.queue)


if __name__ == "__main__":
    panel = PanelBase("Chat Panel", width=70)

    while True:
        user = panel.console.input("User: ")
        panel.create_chatbox("User", user, is_ai=False)
        panel.console.clear()
        panel.print_stdout()
        ai = panel.console.input("AI: ")
        panel.create_chatbox("AI", ai)
        panel.console.clear()

        panel.print_stdout()
