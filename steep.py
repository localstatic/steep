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
        self._ticks = 0
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

        self.on_tea_selected()
        self.reset_timer()
        
    def on_btn_start_clicked(self, widget = None, data = None):
        self.on_tea_selected()
        logging.debug("Starting.");
        self.update_timer_display()
        self._timer.start()

    def on_btn_stop_clicked(self, widget = None, data = None):
        if not self._timer.is_running():
            return
        
        logging.debug("Stopping.")
        self._timer.stop()
        self.update_timer_display()

    def reset_timer(self):
        logging.debug("Resetting.")
        self.on_btn_stop_clicked()
        self._remaining = self._ticks
        self.update_timer_display()
        
    def on_tea_selected(self, widget = None, data = None):
        self.on_btn_stop_clicked()

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
        self._ticks = seconds
        self._remaining = self._ticks
        self.pb_progressbar.set_fraction(0)
        self.update_timer_display()
        
    def update_timer_display(self):
        formatted_time_string = '%d:%02d' % (self._remaining / 60, self._remaining % 60)
        self.pb_progressbar.set_text(formatted_time_string)
        
        if 0 != self._ticks:
            self.pb_progressbar.set_fraction(float(self._remaining) / self._ticks)

    def tick(self):
        logging.debug("tick (" + str(self._remaining) + ").")
        self._remaining = self._remaining - 1
        self.update_timer_display()

        if self._remaining <= 0:
            logging.debug("done.")
            self.on_btn_stop_clicked()
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


