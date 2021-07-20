import time
import os

# Set the timezone to German timezone with respect to DST
def setTimeZone():
    """
    set the timezone to German Timezone with respect to DST. If not on windows remove time.tzset() as it is not part of
    time module in windows python

    Note: UTC-01UTC-02. This seems backwards as Germany's timezone is UTC+01 normally and UTC+02 during DST. This is how
    the time module in python requires +01 and +02 to be written as in the documentation
    """
    os.environ['TZ'] = "UTC-01UTC-02,M3.5.0,M10.5.0"
    time.tzset()