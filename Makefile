default:
	@echo "Targets:"
	@echo " clean"

clean:
	-rm -f server *.pyc
	-rm -rf __pycache__
