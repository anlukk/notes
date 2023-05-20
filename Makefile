run: env/bin/python solien_web/settings.py solien/manage.py
	./env/bin/python noted/manage.py runserver --settings=solien_web.settings

setdb: env/bin/python solien_web/settings.py solien/manage.py
	./env/bin/python solien/manage.py makemigrate --settings=solien_web.settings

shell: env/bin/python /solien_web/settings.py /manage.py
	./env/bin/python /manage.py shell --settings=solien_web.settings

clear_migrations:
	find solien/ -type d -name migrations -exec rm -v -rf {} +
	

clear_pycache:
	find solien/ -type d -name __pycache__ -exec rm -v -rf {} +

clear: clear_migrations clear_pycache

