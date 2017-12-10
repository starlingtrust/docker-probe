## Probe

[![Build Status](https://travis-ci.org/starlingtrust/docker-probe.svg)](https://travis-ci.org/starlingtrust/docker-probe)

**Probe** is a [Docker](https://www.docker.com/)ized lightweight command-line utility that can be used to test Docker-based dataflow pipelines by acting as a dummy job.

**Probe** can also report on the (virtual) hardware and software environment found inside the Docker container it runs inside of. **Probe** can export its report in JSON or YAML format, suitable for downstream parsing. This makes it possible to run integration tests for dataflow pipelines, confirming that jobs receive the resources (CPU, memory and disk) they requested to run.

### Quickstart

**Probe** is meant to run as a Docker container, and as such a `Dockerfile` is provided to create a Docker image. For convenience a `Makefile` is also provided to create an image tagged with **Probe**'s current version. It can also be used to destroy the image, or run it to produce a basic report:

```
$ make create   # create a tagged image
$ make destroy  # destroy the tagged image
$ make test     # run the image and display a report
```

### Usage

Run `docker run <image> [options]` with `options` as such:

```
usage: [-h] [--sleep SECONDS] [--show-memory] [--show-disks]
       [--show-content PATH] [--show-env]
       [--format {json,json-compact,yaml}] [--to-stdout]
       [--to-stderr] [--to-file FILE] [--version]

optional arguments:
  -h, --help            show this help message and exit
  --sleep SECONDS       Pause the job for a given amount of time (in seconds)
  --show-memory         Add information about virtual and swap memory
  --show-disks          Add information about disk partitions and usage
  --show-content PATH   Add information about files and directories in PATH
  --show-env            Add information about environment variables
  --show-args           Add information about command line arguments
  --format {json,json-compact,yaml}
                        Format of the report (default: json)
  --to-stdout           Output the report on the standard output stream
  --to-stderr           Output the report on the standard error stream
  --to-file FILE        Output the report to a file
  --version             show program's version number and exit
```
