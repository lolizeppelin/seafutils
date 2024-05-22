#! /usr/bin/env python
import os.path
from oslo_config import generator

path = os.path.dirname(__file__)
cfgs = (
    ['--namespace', 'seafile', '--output-file', 'etc/seafile/seafile.conf'],
    ['--namespace', 'seafile.init', '--output-file', 'etc/initialize.conf'],
)

os.chdir(path)

etc = os.path.join("etc", "seafile")
if not os.path.exists(etc):
    os.makedirs(etc, mode=0o755)

for args in cfgs:
    generator.main(args)
