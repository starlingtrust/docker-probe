## Probe

**Probe** is a [Docker](https://www.docker.com/)ized lightweight utility that can be used to test Docker-based dataflow pipelines by acting as a dummy job.

**Probe** can also report on the (virtual) hardware and software environment found inside the Docker container it runs in. It can confirm that the containers have been set up with the right compute resources (CPU, memory and disk).

### Quickstart

For convenience a `Makefile` is provided to create a Docker image tagged with **Probe**'s version. It can also be used to destroy the image, or run it with a default report:

```
$ make create  # create a tagged image
$ make destroy # destroy the image
$ make test    # request a report from the probe
```

### Usage

`docker run <image> [options]` with `options` as such:

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
  --format {json,json-compact,yaml}
                        Format of the report (default: json)
  --to-stdout           Output the report on the standard output stream
  --to-stderr           Output the report on the standard error stream
  --to-file FILE        Output the report to a file
  --version             show program's version number and exit
```