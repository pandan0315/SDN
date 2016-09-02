app_task1:
	python -m compileall ./sdn/task1/
	PYTHONPATH=$(PWD)/sdn /home/click/pox/pox.py task1.controller

app_task2:
	python -m compileall ./sdn/task2/
	PYTHONPATH=$(PWD)/sdn /home/click/pox/pox.py task2.controller
app_task3:
	python -m compileall ./sdn/task3/
	PYTHONPATH=$(PWD)/sdn /home/click/pox/pox.py log.level -DEBUG task3.controller
clean:
	sudo killall controller
