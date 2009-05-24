UIS=new_machine_ui.py main_ui.py
PYS=main.py dbhandler.py new_machine.py

all: uis calendar.db
	./main.py

uis: $(UIS)

clean:
	rm -f *pyc $(UIS) calendar.db *~

lint: uis
	pylint $(PYS)

%_ui.py: %.ui
	pyuic4 -o $@ $<

calendar.db: calendar.sql
	sqlite3 -init calendar.sql calendar.db .quit
