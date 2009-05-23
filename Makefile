UIS=new_machine_ui.py main_ui.py

all: $(UIS) calendar.db
	./main.py

clean:
	rm *pyc $(UIS) calendar.db *~ 2>/dev/null ; true

%_ui.py: %.ui
	pyuic4 -o $@ $<

calendar.db: calendar.sql
	sqlite3 -init calendar.sql calendar.db .quit
