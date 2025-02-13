path := .

define Comment
	- Run `make help` to see all the available options.
endef

.PHONY: help
help: ## 도움말
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## 빌드
	poetry build
	pip install dist/*.whl

.PHONY: test
test: ## 테스트
	cd test && poetry run pytest --log-cli-level DEBUG

.PHONY: clean
clean: ## 빌드 파일 삭제
	rm -rf dist
	pip uninstall -y binjector
