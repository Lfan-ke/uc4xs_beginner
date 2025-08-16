init:
	cd fifo_test && \
	picker export rtl/SyncFIFO.v --sname SyncFIFO \
       -w out/SyncFIFO.fst --lang python --sim verilator --rw 1

clean:
	rm -rf fifo_test/out/*
	rm -rf fifo_test/SyncFIFO

test:
	cd fifo_test && \
	python test_smoke.py

wave:
	cd fifo_test && \
	gtkwave out/SyncFIFO.fst

unit:
	cd fifo_test && \
	pytest -v -s
