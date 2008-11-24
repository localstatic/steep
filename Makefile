
default:
	@true

clean:
	@rm -rf snapshot
	@rm -f timer.pyc

snapshot: steep steep.py steep.glade steep.conf timer.py COPYRIGHT
	@echo "Creating snapshot in ./snapshot"
	@mkdir snapshot
	@cp -f steep snapshot/steep
	@cp -f steep.py snapshot/steep.py
	@cp -f steep.glade snapshot/steep.glade
	@cp -f steep.conf snapshot/steep.conf
	@cp -f timer.py snapshot/timer.py
	@cp -f COPYRIGHT snapshot/COPYRIGHT

