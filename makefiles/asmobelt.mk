# asmobelt.mk - Asmobelt CLI commands
ASMOBELT_TARGET_DIR ?= .
ASMOBELT_PROMPT_OUTPUT ?= prompt.txt

.PHONY: add-path-comment concat-py-files

add-path-comment:
	asmobelt add-path-comment -d $(ASMOBELT_TARGET_DIR) || true

concat-py-files:
	asmobelt concat-py-files -p $(ASMOBELT_TARGET_DIR) -o $(ASMOBELT_PROMPT_OUTPUT) || true
