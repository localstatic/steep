#!/usr/bin/env python

import gtk
import gtk.glade
import gobject
import logging
import string
import thread
import time
import ConfigParser

import timer

class Steep:
    def __init__(self):
        logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.debug)

        # Read config & do any relevant setup
        self._config_values = self.read_config()
        #logging.debug(self._config_values)
        
        #
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
      
        # set up tree view with timers from the config file
        cell = gtk.CellRendererText()
        col = gtk.TreeViewColumn('Name', cell)
        col.add_attribute(cell, 'text', 0)
        self.tv_timers.append_column(col)
        
        cell = gtk.CellRendererText()
        col = gtk.TreeViewColumn('Duration', cell)
        col.set_cell_data_func(cell, self.render_timer_duration, None)
        self.tv_timers.append_column(col)
        
        store = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT)

        for t in self._config_values['timers']:
            timer_values = self._config_values['timers'][t]
            store.append((timer_values['label'], int(timer_values['duration'])))
            
        self.tv_timers.set_model(store)
        self.tv_timers.columns_autosize()

        #
        self.wnd_main.show()
        self.reset_timer()
    
    def render_timer_duration(self, column, cell, model, iter, user_data):
        cell.set_property('text', self.get_seconds_time_display_string(model.get_value(iter, 1)))
    
    def read_config(self):
        config = ConfigParser.ConfigParser()
        config.read('steep.conf')

        config_values = dict(config.items('options'))
        sections = config.sections()
        
        if len(sections) > 0:
            config_values['timers'] = {}
            for sect in sections:
                if sect.startswith('timer.'):
                    items = config.items(sect)
                    sect_items = {}
                    
                    for name, value in items:
                        sect_items[name] = value
                    
                    config_values['timers'][sect.replace('timer.', '')] = sect_items 
                
        return config_values
            
    def on_btn_startstop_clicked(self, widget = None, data = None):
        if self._timer.is_running():
            self.stop_timer()
        else:
            self.start_timer()
            
    def on_btn_exit_clicked(self, widget = None, data = None):
        gtk.main_quit()
        
    def on_tv_row_activated(self, treeview, view_column, unused):
        model, iter = treeview.get_selection().get_selected()
        
        seconds = model.get_value(iter, 1)
        
        self.stop_timer()
        self.init_timer(seconds)

        self.start_timer()

    def on_tv_timers_changed(self, treeview = None):
        if None == treeview:
            treeview = self.tv_timers
        
        model, iter = treeview.get_selection().get_selected()
        
        if None == iter:
            iter = model.get_iter_first()
        
        seconds = model.get_value(iter, 1)
        
        self.stop_timer()
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
            self.on_tv_timers_changed()
            
        #logging.debug("Starting.");
        self._started_at = time.time()
        self.update_timer_display()
        self.btn_startstop.set_label('Stop')
        self.vbox_timers_ui.set_sensitive(False)
        self._timer.start()

    def stop_timer(self):
        if not self._timer.is_running():
            return
        
        #logging.debug("Stopping.")
        self._timer.stop()
        self.vbox_timers_ui.set_sensitive(True)
        self.update_timer_display()
        self.btn_startstop.set_label('Start')

    def reset_timer(self):
        #logging.debug("Resetting.")
        self.stop_timer()
        self._remaining = self._seconds
        self.update_timer_display()
        
    def get_seconds_time_display_string(self, seconds):
        return '%d:%02d' % (seconds / 60, seconds % 60)
        
    def update_timer_display(self):
        remaining = int(self._remaining)
        elapsed_seconds = self._seconds - remaining
        total_time_string = self.get_seconds_time_display_string(elapsed_seconds)
        remaining_time_string = self.get_seconds_time_display_string(remaining)
        self.pb_progressbar.set_text(total_time_string + ' / -' + remaining_time_string)
        
        if 0 != self._seconds and 0 < self._remaining:
            fraction = 1 - float(self._remaining) / self._seconds
        else:
            fraction = 0

        self.pb_progressbar.set_fraction(fraction)

    def tick(self):
        #logging.debug("tick (" + str(self._remaining) + ").")
        self._remaining = self._seconds - (time.time() - self._started_at) 
        self.update_timer_display()

        if self._remaining <= 0:
            #logging.debug("done.")
            self.stop_timer()
            gobject.idle_add(self.timer_elapsed)
            
    def timer_elapsed(self):
        finished_message = self._config_values['finished_message'] or 'Done.'
        dlg = gtk.MessageDialog(self.wnd_main, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, finished_message)
        dlg.run()
        dlg.destroy()
        
    def main(self):
        gtk.main()

if __name__ == "__main__":
    obj = Steep()
    gtk.main()


