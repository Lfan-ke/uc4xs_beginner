init:
	cd fifo_test && \
	picker export rtl/SyncFIFO.v --sname SyncFIFO -c \
       -w out/SyncFIFO.fst --lang python --sim verilator --rw 1 --tdir SyncFIFO \
	   --vflag "--trace" --internal internal.yaml

clean:
	rm -rf fifo_test/out/*
	rm -rf fifo_test/reports/*
	rm -rf fifo_test/SyncFIFO
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*_cache" -exec rm -rf {} +

wave:
	cd fifo_test && \
	gtkwave out/SyncFIFO.fst

test:
	cd fifo_test && \
	pytest -sv --toffee-report --report-name sync_fifo_report.html -n auto

firefox:
	firefox fifo_test/reports/sync_fifo_report.html
