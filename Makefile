
VERSION := "0.2.2"

.PHONY: build_image
build_image:
	@docker build --squash --tag probe:$(VERSION) --tag probe:latest .

.PHONY: destroy_image
destroy_image:
	@docker rmi --force probe:$(VERSION) probe:latest

.PHONY: test_image
test_image:
	@docker run --hostname probe_test probe:$(VERSION) \
	  --show-memory \
	  --show-env \
	  --format yaml \
	  --to-stdout
