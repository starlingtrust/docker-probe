
.PHONY: build
build:
	@docker build --tag probe .

.PHONY: destroy
destroy:
	@docker rmi --force probe

.PHONY: test
test:
	@docker run probe \
	  --show-memory \
	  --format yaml \
	  --to-stdout
