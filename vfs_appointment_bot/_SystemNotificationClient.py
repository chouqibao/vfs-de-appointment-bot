import os
import platform


class _SystemNotificationClient:

    def __init__(self):
        self._system = platform.system()

    def show_notification(self, title, text):
        if self._system == 'Darwin':
            os.system("""
                  osascript -e 'display notification "{}" with title "{}"'
                  """.format(text, title))
        elif self._system == 'Windows':
            pass
        elif self._system == 'Linux':
            pass
        else:
            pass
