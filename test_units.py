#!/usr/bin/env python

import functools
import json
import unittest
import uuid
import os

from test_utils import *
import docker.errors

probe_version = "0.2.2"
probe = lambda client, *args, **kwargs: docker_container(
    client, "probe:" + probe_version, ("--to-stdout",) + args, **kwargs)

random_string = lambda: uuid.uuid4().hex

class IntegrationTests (unittest.TestCase):

    def test_returned_version(self):
        with docker_client() as client:
            with probe(client) as stdout:
                report = json.loads(stdout)
                self.assertEqual(probe_version, report["version"])

    def test_hostname_injection(self):
        hostname = random_string()
        with docker_client() as client:
            with probe(client, hostname = hostname) as stdout:
                report = json.loads(stdout)
                self.assertEqual(hostname, report["platform"]["hostname"])

    def test_environment_injection(self):
        environment = {"FOO": random_string(), "BAR": random_string()}
        with docker_client() as client:
            with probe(client, "--show-env", environment = environment) as stdout:
                report = json.loads(stdout)
                for (key, value) in environment.items():
                    self.assertTrue(key in report["env"])
                    self.assertEqual(value, report["env"][key])

    def test_exit_code(self):
        with docker_client() as client:
            with self.assertRaises(docker.errors.ContainerError) as e:
                with probe(client, "--exit-with-code", "123"):
                    pass
            self.assertEqual(123, e.exception.exit_status)

if (__name__ == "__main__"):
    unittest.main()
