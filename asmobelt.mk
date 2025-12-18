.PHONY: add-path-comment
.PHONY: py-concat

add-path-comment:
	asmobelt add-path-comment -d backend/app/ || true

py-concat:
	asmobelt py-concat -p backend/app/ -o prompt_backend_app.txt || true
