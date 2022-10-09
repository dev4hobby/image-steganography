path := .

define Comment
	- Run `make help` to see all the available options.
endef

.PHONY: help
help: ## 도움말
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## 빌드
	python3 setup.py bdist_wheel
	cd dist && twine upload binjector*.whl

.PHONY: clean
clean: ## 빌드 파일 삭제
	pip uninstall binjector
	rm -rf build
	rm -rf dist