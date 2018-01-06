DBSRCURL = https://github.com/jfcarr-astronomy/HYG-Database-SQLite/blob/master/
DBSRCNAME = hygdata.db
DBTGTDIR = db/

default:
	@echo "Targets:"
	@echo " clean"
	@echo " getdb"

clean:
	-rm -f *.pyc
	-rm -rf __pycache__

getdb:
	wget $(DBSRCURL)$(DBSRCNAME)
	mv $(DBSRCNAME) $(DBTGTDIR)
