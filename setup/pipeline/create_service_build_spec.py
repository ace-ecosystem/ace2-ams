#!/usr/bin/env python3
import os
import yaml

with open('setup/pipeline/service_build_spec.yml') as f:
    spec = yaml.safe_load(f)
spec['batch']['build-matrix']['dynamic']['env']['variables']['PATH'] = os.listdir('services')
print(yaml.dump(spec))
