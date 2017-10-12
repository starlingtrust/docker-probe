
VERSION := $(shell git describe --abbrev=0 --tags)

.PHONY: build
build:
	@docker build --tag probe:$(VERSION) .

.PHONY: destroy
destroy:
	@docker rmi --force probe:$(VERSION)

.PHONY: test
test:
	@docker run probe:$(VERSION) \
	  --show-memory \
	  --format yaml \
	  --to-stdout
