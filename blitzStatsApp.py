#! python 3

import kivy
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from blitzStats import get_stats, record_stats, track_stats
import threading

kivy.require("1.11.1")


class MainScreen(GridLayout):

    username = ObjectProperty(None)
    server = StringProperty("asia")
    stats = ObjectProperty(None)
    record = ObjectProperty(None)
    update_timestamp = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_stats(self):
        output = get_stats(self.username.text, self.server)
        if len(output) > 1:
            self.stats.text = f"{output[1]}\nYour winrate is {'%.2f' % output[2]}%."
            self.update_timestamp.text = f"\n\nPlayer data last updated on {output[3]}"
            record_stats(output)
            self.record.text = track_stats(output[0])
        elif len(output) == 1:
            self.stats.text = output[0]

    def get_player_stats(self):
        self.stats.text = "Searching..."
        stats_thread = threading.Thread(target=self.show_stats)
        if stats_thread.is_alive():
            stats_thread.join()
        return stats_thread.start()


class BlitzStatsApp(App):

    def build(self):
        return MainScreen()


if __name__ == '__main__':
    BlitzStatsApp().run()
