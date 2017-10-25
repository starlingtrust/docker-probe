
import contextlib
import uuid
import warnings

import docker

__all__ = (
    "docker_client",
    "docker_container",
    "docker_volume")

class docker_context (contextlib.ExitStack):
    pass

@contextlib.contextmanager
def docker_client(**client_kwargs):
    client_kwargs.setdefault("version", "auto")
    client = docker.from_env(**client_kwargs)
    client.ping()
    yield client

@contextlib.contextmanager
def docker_container(client, image, command = None, **container_kwargs):
    container = None
    container_kwargs.setdefault("detach", False)

    # by default, we remove the container automatically
    if (container_kwargs["detach"]):
        container_kwargs.setdefault("auto_remove", True)
    else:
        container_kwargs.setdefault("remove", True)

    try:
        # run the container, pulling the image if needed
        container = client.containers.run(image, command, **container_kwargs)
        yield container
    finally:
        # silencing of nagging ResourceWarning messages, see
        # https://github.com/requests/requests/issues/1882
        warnings.filterwarnings(category = ResourceWarning,
            action = "ignore", message = "unclosed")

        # stop and remove the container, if detached
        if (container is not None) and (container_kwargs["detach"]):
            container.stop()
            container.remove(force = True)

@contextlib.contextmanager
def docker_volume(client, name = None, driver = "local", **volume_kwargs):
    volume = None
    if (name is None):
        name = uuid.uuid4().hex

    try:
        volume = client.volumes.create(
            name, driver = driver, driver_opts = volume_kwargs)

        yield volume
    finally:
        if (volume is not None):
            volume.remove(force = True)
