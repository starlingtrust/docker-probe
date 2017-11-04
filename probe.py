#!/usr/bin/env python

import argparse
import datetime
import platform
import psutil
import pwd
import grp
import time
import json
import yaml
import os
import sys

__version__ = "0.3.1"

parser = argparse.ArgumentParser()

parser.add_argument("--sleep", type = int,  metavar = "SECONDS",
    help = "Pause the job for a given amount of time (in seconds)")

parser.add_argument("--show-memory", action = "store_true", default = False,
    help = "Add information about virtual and swap memory")

parser.add_argument("--show-disks", action = "store_true", default = False,
    help = "Add information about disk partitions and usage")

parser.add_argument("--show-content", metavar = "PATH", action = "append",
    help = "Add information about files and directories in PATH")

parser.add_argument("--show-env", action = "store_true", default = False,
    help = "Add information about environment variables")

parser.add_argument("--show-args", action = "store_true", default = False,
    help = "Add information about command line arguments")

parser.add_argument("--format",
    choices = ["json", "json-compact", "yaml"], default = "json",
    help = "Format of the report (default: %(default)s)")

parser.add_argument("--to-stdout", action = "store_true",
    help = "Output the report on the standard output stream")

parser.add_argument("--to-stderr", action = "store_true",
    help = "Output the report on the standard error stream")

parser.add_argument("--to-file", metavar = "FILE",
    help = "Output the report to a file")

parser.add_argument("--exit-with-code",
    type = int, metavar = "INTEGER", default = 0,
    help = "Exit code (default: %(default)d)")

parser.add_argument("--version", action = "version",
    version = __version__)

# separate this program's arguments from extra arguments, if any
if ("--" in sys.argv):
    i = sys.argv.index("--")
    args, extra_args = sys.argv[:i], sys.argv[i+1:]
else:
    args, extra_args = sys.argv, []

args = parser.parse_args(args[1:])

def _format_integers(d):
    d_ = {}
    for (key, value) in d.items():
        d_[key] = value
        if (isinstance(value, int)):
            d_[key + "_readable"] = "{:,}".format(value)

    return d_

report = {
    "version": __version__,
    "location": os.path.dirname(os.path.abspath(__file__)),
    "time": {
        "epoch": time.time(),
        "datetime_utc": datetime.datetime.utcnow().isoformat(),
        "datetime": datetime.datetime.now().isoformat(),
        "zone": "/".join(time.tzname),
    },
    "platform": {
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": platform.node(),
        "system": platform.system(),
        "system_release": platform.release(),
        "system_version": platform.version()},
    "cpu": {
        "number_logical": psutil.cpu_count(),
        "number_physical": psutil.cpu_count(logical = False)}}

if (args.show_memory):
    report.update(memory = {
        "virtual": _format_integers(psutil.virtual_memory()._asdict()),
        "swap": _format_integers(psutil.swap_memory()._asdict())})

if (args.show_disks):
    partitions = [dict(nt._asdict()) for nt in psutil.disk_partitions()]
    for partition in partitions:
        partition.update(_format_integers(
            psutil.disk_usage(partition["mountpoint"])._asdict()))

    report.update(disks = partitions)

def _format_permissions(st_mode):
    to_str = {'7':'rwx', '6' :'rw-', '5' : 'r-x', '4':'r--', '0': '---'}
    return "".join(to_str.get(x, x) for x in str(oct(st_mode)[-3:]))

if (args.show_content is not None):
    report.update(content = [])

    def tree(path):
        with os.scandir(path) as entries:
            for entry in entries:
                yield entry
                if (entry.is_dir(follow_symlinks = True)):
                    yield from tree(entry.path)

    for path in args.show_content:
        if (not os.path.isdir(path)):
            content = "NOT_FOUND"
        else:
            content = []
            for entry in tree(path):
                entry_stats = entry.stat()

                permissions = _format_permissions(entry_stats.st_mode)
                if (entry.is_dir()):
                    permissions = "d" + permissions
                else:
                    permissions = "-" + permissions

                try:
                    user = pwd.getpwuid(entry_stats.st_uid).pw_name
                except KeyError:
                    user = "UNKNOWN"

                try:
                    group = grp.getgrgid(entry_stats.st_gid).gr_name
                except KeyError:
                    group = "UNKNOWN"

                content.append({
                    "path": entry.path,
                    "size": entry_stats.st_size,
                    "size_readable": "{:,}".format(entry_stats.st_size),
                    "permissions": permissions,
                    "user": user, "group": group})

            if (len(content) > 0):
                content.sort(key = lambda entry: entry["path"])
            else:
                content = "EMPTY"

        report["content"].append({
            "path": path, "content": content})

if (args.show_env):
    report["env"] = dict(os.environ)

if (args.show_args):
    report["args"] = extra_args

if (args.format == "json"):
    report = json.dumps(report,
        sort_keys = True,
        indent = True)

elif (args.format == "json-compact"):
    report = json.dumps(report,
        sort_keys = True,
        separators = (",", ":"))

elif (args.format == "yaml"):
    report = yaml.dump(report,
        explicit_start = True,
        default_flow_style = False)

if (not report.endswith("\n")):
    report += "\n"

if (args.sleep):
    time.sleep(args.sleep)

if (args.to_stdout):
    sys.stdout.write(report)
    sys.stdout.flush()

if (args.to_stderr):
    sys.stderr.write(report)
    sys.stderr.flush()

if (args.to_file):
    with open(args.to_file, "a") as fh:
        fh.write(report)

sys.exit(args.exit_with_code)
