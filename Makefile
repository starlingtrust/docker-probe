
VERSION := "0.2.1"

.PHONY: build_image
build_image:
	@docker build --squash --tag probe:$(VERSION) .

.PHONY: destroy_image
destroy_image:
	@docker rmi --force probe:$(VERSION)

.PHONY: test_image
test_image:
	@docker run --hostname probe_test probe:$(VERSION) \
	  --show-memory \
	  --show-env \
	  --format yaml \
	  --to-stdout
