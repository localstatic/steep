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

        self.on_btn_reset_clicked()
        
    def on_btn_start_clicked(self, widget = None, data = None):
        self.init_timer(self._ticks)

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
        
    def on_tea_selected(self, widget, data = None):
        if self.rb_blacktea.get_active():
            seconds = 5 * 60
        elif self.rb_greentea.get_active():
            seconds = 3 * 60
        elif self.rb_herbaltea.get_active():
            seconds = 7 * 60
        
        self.on_btn_stop_clicked()
        self.init_timer(seconds)
    
    def on_wnd_main_delete_event(self, widget, event, data=None):
        print "delete event"
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
        self.lbl_remaining.set_text(formatted_time_string)
        
    def tick(self):
        print "tick."
        self._remaining = self._remaining - 1
        self.update_timer_display()
        self.pb_progressbar.set_fraction(1 - float(self._remaining) / self._ticks)
        self.pb_progressbar.set_text(self.lbl_remaining.get_text())
        if self._remaining <= 0:
            print "done."
            #msgdlg = gtk.MessageDialog(self.wnd_main, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, 'Tea is ready.')
            #msgdlg.run()
            self.on_btn_stop_clicked()
        
    def main(self):
        gtk.main()

if __name__ == "__main__":
    obj = SteepTimer()
    obj.main()


