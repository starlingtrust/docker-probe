
VERSION := $(shell git describe --abbrev=0 --tags)

.PHONY: build
build:
	@docker build --squash --tag probe:$(VERSION) .

.PHONY: destroy
destroy:
	@docker rmi --force probe:$(VERSION)

.PHONY: test
test:
	@docker run --hostname probe_test probe:$(VERSION) \
	  --show-memory \
	  --show-env \
	  --format yaml \
	  --to-stdout
