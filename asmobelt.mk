.PHONY: c add_path_comment
.PHONY: p prompt

c: add_path_comment

add_path_comment:
	asmobelt path-comment -d asmobelt/ || true

p: prompt

prompt:
	asmobelt py-concat -p asmobelt/ -o prompt_backend_app.txt || true
