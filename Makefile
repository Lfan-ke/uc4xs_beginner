PYTEST_OPTS := -s -v --toffee-report --report-name cache_ut_report.html -n auto
MILL_CMD := mill --no-server -d
VERILATOR_OPTS := --trace
PICKER_CMD := picker export
GTKWAVE := gtkwave
BROWSER := firefox

BASE_DIR := cache-ut
BUILD_DIR := build
WAVOUT_DIR := wavout
OUT_DIR := out
REPORT_DIR := reports
CACHE_MODULE := Cache
TARGET_DIRS := $(addprefix $(BASE_DIR)/, $(BUILD_DIR) $(WAVOUT_DIR) $(REPORT_DIR))

.PHONY: all test build clean init wave report

all: test

test:
	@echo "[INFO] Running tests with pytest..."
	cd cache-ut && pytest $(PYTEST_OPTS) || (echo "[ERROR] Tests failed"; exit 1)

$(BASE_DIR)/$(BUILD_DIR)/Cache.v: $(BASE_DIR)/$(BUILD_DIR)
	@echo "[INFO] Generating Cache RTL..."
	@echo $(shell cd cache-ut && mill --version)
	@cd cache-ut && $(MILL_CMD) ut.runMain ut_nutshell.CacheMain --target-dir $(BUILD_DIR) --output-file $(CACHE_MODULE) || (echo "[ERROR] RTL generation failed"; exit 1)

build: $(BASE_DIR)/$(BUILD_DIR)/Cache.v

init: $(BASE_DIR)/$(BUILD_DIR)/Cache.v $(BASE_DIR)/$(WAVOUT_DIR) $(BASE_DIR)/$(REPORT_DIR)
	@echo "[INFO] Initializing simulation environment..."
	cd cache-ut && \
		VERILATOR_COVERAGE_OUTPUT=./reports/ \
		$(PICKER_CMD) build/Cache.v \
		--sname Cache \
		-c \
		-w $(WAVOUT_DIR)/Cache.fst \
		--lang python \
		--sim verilator \
		--rw 1 \
		--tdir $(CACHE_MODULE) \
		--vflag "$(VERILATOR_OPTS)" || (echo "[ERROR] Picker export failed"; exit 1)

clean:
	@echo "[INFO] Make cleaning..."
	@rm -rf $(addprefix $(BASE_DIR)/, $(OUT_DIR)/* $(BUILD_DIR)/* $(REPORT_DIR)/* $(CACHE_MODULE) $(WAVOUT_DIR)/*)
	@find . -name "__pycache__" -exec rm -rf {} +
	@find . -name "*_cache" -exec rm -rf {} +
	@find . -name "V*_coverage.*" -exec rm -rf {} +

wave:
	@echo "[INFO] Opening waveform viewer..."
	@cd cache-ut && $(GTKWAVE) $(WAVOUT_DIR)/Cache.fst

report:
	@echo "[INFO] Opening test report..."
	@$(BROWSER) $(BASE_DIR)/$(REPORT_DIR)/cache_ut_report.html

$(BASE_DIR)/$(BUILD_DIR)/Cache.v: | $(BASE_DIR)/$(BUILD_DIR)

$(TARGET_DIRS):
	@mkdir -p $@

.PHONY: | $(TARGET_DIRS)
