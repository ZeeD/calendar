%_ui.py: %.ui
	pyuic4 -o $@ $<
	
