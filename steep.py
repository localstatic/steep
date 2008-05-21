#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gobject

#

import string
import thread
import time

#

import timer

class steeptimer:
    def __init__(self):
        gobject.threads_init()
        self._ticks_remaining = 5
        self._timer = timer.Timer(1, self.tick)
        self.build_ui()

    def start(self, widget = None, data = None):
        self._ticks_remaining = 5
        print "Starting."
        self.lblTimerTime.set_text(str(self._ticks_remaining))
        self._timer.start()

    def stop(self, widget = None, data = None):
        print "Stopping."
        self._timer.stop()
        self.lblTimerTime.set_text(str(self._ticks_remaining))

    def reset(self, widget = None, data = None):
        print "Resetting."
        self._ticks_remaining = 5
        self.lblTimerTime.set_text(str(self._ticks_remaining))
        
    def tick(self):
        print "tick."
        self._ticks_remaining = self._ticks_remaining - 1
        self.lblTimerTime.set_text(str(self._ticks_remaining))
        
        if self._ticks_remaining <= 0:
            print "done."
            self.stop()
        
    def main(self):
        gtk.main()

    def say_something(self, widget, data):
        print "%s" % data

    def delete_event(self, widget, event, data=None):
        print "delete event"
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def build_ui(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

        self.label1 = gtk.Label("Placeholder Label")
        self.separator1 = gtk.HSeparator()

        self.btnStart = gtk.Button("Start")
        self.btnStart.connect("clicked", self.start, "Starting timer.")
        
        self.btnStop = gtk.Button("Stop")
        self.btnStop.connect("clicked", self.stop, "Stopping timer.")

        self.btnReset = gtk.Button("Reset")
        self.btnReset.connect("clicked", self.reset, "Resetting timer.")

        self.btnQuit = gtk.Button("Quit")
        self.btnQuit.connect("clicked", self.say_something, "Quitting.")
        self.btnQuit.connect_object("clicked", gtk.Widget.destroy, self.window)

        self.boxTimerUI = gtk.HBox(True, 0)
    
        self.boxTimerButtons = gtk.VBox(True, 0)
        self.boxTimerButtons.pack_start(self.btnStart, False)
        self.boxTimerButtons.pack_start(self.btnStop, False)
        self.boxTimerButtons.pack_start(self.btnReset, False)
        
        self.lblTimerTime = gtk.Label("0:00")    
        
        self.boxTimerUI.pack_start(self.lblTimerTime, False)
        self.boxTimerUI.pack_start(self.boxTimerButtons, False, False)

        self.vboxMain = gtk.VBox(True, 0)
        self.vboxMain.pack_start(self.boxTimerUI, True, True)
        self.vboxMain.pack_start(self.label1, True, False)
        self.vboxMain.pack_start(self.separator1, False, True)
        self.vboxMain.pack_end(self.btnQuit, True, False)

        self.window.add(self.vboxMain)

        self.label1.show()
        self.separator1.show()

        self.btnStart.show()
        self.btnStop.show()
        self.btnReset.show()

        self.btnQuit.show()
        
        self.lblTimerTime.show()
        self.boxTimerButtons.show()
        self.boxTimerUI.show()
        self.vboxMain.show()

        self.window.show()

if __name__ == "__main__":
    obj = steeptimer()
    obj.main()


