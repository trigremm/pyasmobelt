.PHONY: add-path-comment
.PHONY: concat-py-files

add-path-comment:
	asmobelt add-path-comment -d backend/app/ || true

concat-py-files:
	asmobelt concat-py-files -p backend/app/ -o prompt_backend_app.txt || true
