from enum import Enum

# Segment analytics constants
USER = "unctl_user"
SEGMENT_WRITE_KEY = "qSQliHLwStBWT3nncdrN241UgdZdPM5H"

# Segment data collection for minimum time to send event
# to exclude accidental or discovering clicks
MIN_TRACK_RESOLVING_TIME = 10
EPILOG_HELP_DOCS = """For more information, check the documentation at:
    https://docs.unskript.com/unctl"""


class CheckProviders(str, Enum):
    AWS = "aws"
    K8S = "k8s"
    MySQL = "mysql"
