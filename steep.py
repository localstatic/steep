#!/usr/bin/env python

import gtk
import gtk.glade
import gobject

#

import string
import thread
import time

#

import timer

class SteepTimer:
    def __init__(self):
        gobject.threads_init()
        self._ticks = 5
        self._remaining = 0
        self._timer = timer.Timer(1, self.tick)

        # set up UI via Glade
        
        wtree = gtk.glade.XML('steep.glade')
        wtree.signal_autoconnect(self)
        
        for w in wtree.get_widget_prefix(''):
            name = w.get_name()
            assert not hasattr(self, name)
            setattr(self, name, w)
            
        self.wnd_main.show()

        #
        
        self.on_btn_reset_clicked()
        
    def on_btn_start_clicked(self, widget = None, data = None):
        self._remaining = self._ticks
        print "Starting."
        self.update_timer_display()
        self._timer.start()

    def on_btn_stop_clicked(self, widget = None, data = None):
        print "Stopping."
        self._timer.stop()
        self.update_timer_display()

    def on_btn_reset_clicked(self, widget = None, data = None):
        print "Resetting."
        self.on_btn_stop_clicked()
        self._remaining = self._ticks
        self.update_timer_display()
        
    def update_timer_display(self):
        self.lbl_remaining.set_text(str(self._remaining))
        
    def tick(self):
        print "tick."
        self._remaining = self._remaining - 1
        self.update_timer_display()
        
        if self._remaining <= 0:
            print "done."
            self.on_btn_stop_clicked()
        
    def on_wnd_main_delete_event(self, widget, event, data=None):
        print "delete event"
        return False

    def on_wnd_main_destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    obj = SteepTimer()
    obj.main()


