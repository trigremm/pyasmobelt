.PHONY: f format
.PHONY: c add_path_comment
.PHONY: p prompt

f: format

format:
	autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive .
	isort --force-single-line-imports --line-length 120 .
	black --line-length 120 .

c: add_path_comment

add_path_comment:
	asmobelt path-comment -d asmobelt/ || true

p: prompt

prompt:
	asmobelt py-concat -p asmobelt/ -o prompt_backend_app.txt || true

