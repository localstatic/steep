#!/usr/bin/env python

import gtk
import gtk.glade
import gobject

#

import logging
import string
import thread
import time

#

import timer

class SteepMain:
    def __init__(self):
        logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.DEBUG)
        gobject.threads_init()
        self._seconds = 0
        self._remaining = 0
        self._timer = timer.Timer(1, self.tick)

        # set up UI via Glade
        
        wtree = gtk.glade.XML('steep.glade', 'wnd_main')
        wtree.signal_autoconnect(self)
        
        for w in wtree.get_widget_prefix(''):
            name = w.get_name()
            assert not hasattr(self, name)
            setattr(self, name, w)
            
        self.wnd_main.show()

        #

        self.on_tea_selected()
        self.reset_timer()
        
    def on_btn_startstop_clicked(self, widget = None, data = None):
        if self._timer.is_running():
            self.stop_timer()
        else:
            self.start_timer()
            
    def on_btn_exit_clicked(self, widget = None, data = None):
        gtk.main_quit()
        
    def on_tea_selected(self, widget = None, data = None):
        self.stop_timer()
        
        if self.rb_blacktea.get_active():
            seconds = 5 * 60
        elif self.rb_greentea.get_active():
            seconds = 3 * 60
        elif self.rb_herbaltea.get_active():
            seconds = 7 * 60
        
        self.init_timer(seconds)
    
    def on_wnd_main_delete_event(self, widget, event, data=None):
        return False

    def on_wnd_main_destroy(self, widget, data=None):
        gtk.main_quit()

    def init_timer(self, seconds):
        self._seconds = seconds
        self._remaining = self._seconds
        self.pb_progressbar.set_fraction(0)
        self.update_timer_display()
        
    def start_timer(self):
        if 0 == self._remaining:
            self.on_tea_selected()
            
        logging.debug("Starting.");
        self._started_at = time.time()
        self.update_timer_display()
        self.btn_startstop.set_label('Stop')
        self.vbox_timers_ui.set_sensitive(False)
        self._timer.start()

    def stop_timer(self):
        if not self._timer.is_running():
            return
        
        logging.debug("Stopping.")
        self._timer.stop()
        self.vbox_timers_ui.set_sensitive(True)
        self.update_timer_display()
        self.btn_startstop.set_label('Start')

    def reset_timer(self):
        logging.debug("Resetting.")
        self.stop_timer()
        self._remaining = self._seconds
        self.update_timer_display()
        
    def update_timer_display(self):
        remaining = int(self._remaining)
        elapsed_seconds = self._seconds - remaining
        total_time_string = '%d:%02d' % (elapsed_seconds / 60, elapsed_seconds % 60)
        remaining_time_string = '%d:%02d' % (remaining / 60, remaining % 60)
        self.pb_progressbar.set_text(total_time_string + ' / -' + remaining_time_string)
        
        if 0 != self._seconds and 0 < self._remaining:
            fraction = 1 - float(self._remaining) / self._seconds
        else:
            fraction = 0

        self.pb_progressbar.set_fraction(fraction)

    def tick(self):
        logging.debug("tick (" + str(self._remaining) + ").")
        self._remaining = self._seconds - (time.time() - self._started_at) 
        self.update_timer_display()

        if self._remaining <= 0:
            logging.debug("done.")
            self.stop_timer()
            gobject.idle_add(self.timer_elapsed)
            
    def timer_elapsed(self):
        dlg = gtk.MessageDialog(self.wnd_main, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, 'Tea is ready.')
        dlg.run()
        dlg.destroy()
        
    def main(self):
        gtk.main()

if __name__ == "__main__":
    obj = SteepMain()
    gtk.main()


