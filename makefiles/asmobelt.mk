# asmobelt.mk - Asmobelt CLI commands
ASMOBELT_TARGET_DIR ?= .
ASMOBELT_PROMPT_OUTPUT ?= prompt.txt

.PHONY: add-path-comment concat-py-files
.PHONY: asmobelt-format asmobelt-uuid git-branch-all git-cleanup git-cleanup-all git-pull-all
.PHONY: GPA GBA GCA
.PHONY: docker-builder-prune docker-container-prune docker-image-prune docker-size docker-stop-all docker-system-prune

add-path-comment:
	asmobelt add-path-comment -d $(ASMOBELT_TARGET_DIR) || true

concat-py-files:
	asmobelt concat-py-files -p $(ASMOBELT_TARGET_DIR) -o $(ASMOBELT_PROMPT_OUTPUT) || true

asmobelt-format:
	asmobelt format

asmobelt-uuid:
	asmobelt uuid

git-pull-all:
	asmobelt git-pull-all -d $(ASMOBELT_TARGET_DIR)

git-branch-all:
	asmobelt git-branch-all -d $(ASMOBELT_TARGET_DIR)

git-cleanup:
	asmobelt git-cleanup -d $(ASMOBELT_TARGET_DIR) $(if $(confirm),--confirm) $(if $(force),--force)

git-cleanup-all:
	asmobelt git-cleanup-all -d $(ASMOBELT_TARGET_DIR) $(if $(confirm),--confirm) $(if $(force),--force)

# Short aliases
GPA: git-pull-all
GBA: git-branch-all
GCA: git-cleanup-all

docker-builder-prune:
	asmobelt docker-builder-prune

docker-container-prune:
	asmobelt docker-container-prune

docker-image-prune:
	asmobelt docker-image-prune

docker-size:
	asmobelt docker-size

docker-stop-all:
	asmobelt docker-stop-all

docker-system-prune:
	asmobelt docker-system-prune
