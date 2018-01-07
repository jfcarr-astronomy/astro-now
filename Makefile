DB_SRC_URL = https://github.com/jfcarr-astronomy/HYG-Database-SQLite/raw/master/
DB_SRC_NAME = hygdata.db
DB_TGT_DIR = db/

default:
	@echo "Targets:"
	@echo " clean"
	@echo " getdb"

clean:
	-rm -f *.pyc
	-rm -rf __pycache__

getdb:
	wget $(DB_SRC_URL)$(DB_SRC_NAME)
	mv $(DB_SRC_NAME) $(DB_TGT_DIR)
