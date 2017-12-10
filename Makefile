
IMAGE_NAME := "probe"
IMAGE_VERSION := "0.4.0"

REGISTRY_HOSTNAME ?= "docker.io"
REGISTRY_USERNAME ?= "$(USER)"

LOCAL_IMAGE := "$(IMAGE_NAME)"
REMOTE_IMAGE := "$(REGISTRY_HOSTNAME)/$(REGISTRY_USERNAME)/$(IMAGE_NAME)"

.PHONY: build_image
build_image:
	@docker build --rm \
	  --tag $(LOCAL_IMAGE):$(IMAGE_VERSION) \
	  --tag $(LOCAL_IMAGE):latest .

.PHONY: destroy_image
destroy_image:
	-@docker rmi --force \
	  $(LOCAL_IMAGE):$(IMAGE_VERSION) \
	  $(LOCAL_IMAGE):latest

.PHONY: push_image
push_image: build_image
	@docker tag $(LOCAL_IMAGE):$(IMAGE_VERSION) $(REMOTE_IMAGE):$(IMAGE_VERSION)
	@docker tag $(LOCAL_IMAGE):latest $(REMOTE_IMAGE):latest
	@docker push $(REMOTE_IMAGE):$(IMAGE_VERSION)
	@docker push $(REMOTE_IMAGE):latest

.PHONY: test_image
test_image: build_image
	@python -B ./test_units.py
