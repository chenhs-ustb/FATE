#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import json
import os

from cachetools import LRUCache
from cachetools import cached
from ruamel import yaml

PROJECT_BASE = None


def get_project_base_directory():
    global PROJECT_BASE
    if PROJECT_BASE is None:
        PROJECT_BASE = os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, os.pardir))
    return PROJECT_BASE


@cached(cache=LRUCache(maxsize=10))
def load_json_conf(conf_path):
    if os.path.isabs(conf_path):
        json_conf_path = conf_path
    else:
        json_conf_path = os.path.join(get_project_base_directory(), conf_path)
    try:
        with open(json_conf_path) as f:
            return json.load(f)
    except:
        raise EnvironmentError("loading json file config from '{}' failed!".format(json_conf_path))


def dump_json_conf(config_data, conf_path):
    if os.path.isabs(conf_path):
        json_conf_path = conf_path
    else:
        json_conf_path = os.path.join(get_project_base_directory(), conf_path)
    try:
        with open(json_conf_path, "w") as f:
            json.dump(config_data, f, indent=4)
    except:
        raise EnvironmentError("loading json file config from '{}' failed!".format(json_conf_path))


def load_json_conf_real_time(conf_path):
    if os.path.isabs(conf_path):
        json_conf_path = conf_path
    else:
        json_conf_path = os.path.join(get_project_base_directory(), conf_path)
    try:
        with open(json_conf_path) as f:
            return json.load(f)
    except:
        raise EnvironmentError("loading json file config from '{}' failed!".format(json_conf_path))


def load_yaml_conf(conf_path):
    if not os.path.isabs(conf_path):
        conf_path = os.path.join(get_project_base_directory(), conf_path)
    try:
        with open(conf_path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise EnvironmentError("loading yaml file config from {} failed:".format(conf_path), e)


def set_server_conf(config, SERVER_CONF_PATH, SERVERS):
    # manager
    federatedId = config.get('federatedId')
    server_conf = load_json_conf_real_time(SERVER_CONF_PATH)
    manager_conf = server_conf.get(SERVERS).get('fatemanager', {})
    if manager_conf:
        server_conf[SERVERS]['fatemanager']['federatedId'] = federatedId
    else:
        server_conf[SERVERS]['fatemanager'] = {}
        server_conf[SERVERS]['fatemanager']['federatedId'] = federatedId
    json_conf_path = os.path.join(get_project_base_directory(), SERVER_CONF_PATH)
    rewrite_json_file(json_conf_path, server_conf)
    return {'federatedId': federatedId}


def rewrite_json_file(filepath, json_data):
    with open(filepath, 'w') as f:
        json.dump(json_data, f, indent=4, separators=(',', ': '))
    f.close()


if __name__ == "__main__":
    print(get_project_base_directory())
    print(load_json_conf('federatedml/transfer_variable/definition/transfer_conf.json'))