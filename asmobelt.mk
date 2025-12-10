.PHONY: path-comment
.PHONY: py-concat

path-comment:
	asmobelt path-comment -d backend/app/ || true

py-concat:
	asmobelt py-concat -p backend/app/ -o prompt_backend_app.txt || true
