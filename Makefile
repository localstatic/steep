
default:
	@true

clean:
	rm -rf snapshot

snapshot: steep steep.py steep.glade timer.py COPYRIGHT
	mkdir snapshot
	cp -f steep snapshot/steep
	cp -f steep.py snapshot/steep.py
	cp -f steep.glade snapshot/steep.glade
	cp -f timer.py snapshot/timer.py
	cp -f COPYRIGHT snapshot/COPYRIGHT

