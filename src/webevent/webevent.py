class WebEvent:
    """WebEvent represents a website download event
    """

    def __init__(self, url: str, status_code: int, response_time: float, match_found: bool, match: str):
        self.url = url
        self.status_code = int(status_code)
        self.response_time = float(response_time)
        self.match_found = bool(match_found)
        self.match = match

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __repr__(self):
        return str(self.to_tuple())

    def __str__(self):
        return (f"URL: {self.url}, "
                f"status code: {self.status_code}, "
                f"response time: {self.response_time}, "
                f"regexp match found: {self.match_found}, "
                f"regexp match: {self.match}")

    def to_tuple(self):
        return (
            self.url,
            self.status_code,
            self.response_time,
            self.match_found,
            self.match,
        )

    def encode(self) -> bytes:
        """Encode WebEvent to bytes, to be sent over a stream

        Returns:
            bytes: WebEvent as a stream of bytes
        """
        return f"{self.url},{self.status_code},{self.response_time},{self.match_found},{self.match}".encode("utf-8")

    @classmethod
    def decode(cls, encoded_bytes: bytes):
        """Decode bytes back to a WebEvent

        Args:
            encoded_bytes (bytes): pre-encoded WebEvent

        Returns:
            WebEvent: reconstructed object
        """
        return WebEvent(*encoded_bytes.decode("utf-8").split(","))

    @classmethod
    def db_fields(cls) -> tuple:
        """Tuple of field names to be used in a database table

        Returns:
            tuple: field names
        """
        return ("url", "status_code", "response_time", "match_found", "match")

    @classmethod
    def db_types(cls):
        """Tuple of field types to be used in a database table

        Returns:
            tuple: field types as strings
        """
        return ("varchar", "integer", "real", "bool", "varchar")
