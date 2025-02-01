""" Literally just a counter. """


class Counter:
    """A Counter."""

    def __init__(self) -> None:
        self.count: int = -1

    def c(self) -> int:
        """Increments the counter and returns that number"""
        self.count += 1
        return self.count


"""That's it. What more is there to add?"""
