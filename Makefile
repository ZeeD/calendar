UIS=new_machine_ui.py main_ui.py

all: $(UIS)
	./main.py

clean:
	rm *pyc $(UIS)

%_ui.py: %.ui
	pyuic4 -o $@ $<
