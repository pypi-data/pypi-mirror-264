# -*- coding: utf-8 -*-
# Copyright (c) 2018  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Written by Chenxiong Qi <cqi@redhat.com>
#            Qixiang Wan <qwan@redhat.com>

""" Various utilities """
from fnmatch import fnmatch
from functools import wraps
import os
import re

import gi
gi.require_version('Modulemd', '2.0')    # noqa: E402
from gi.repository import Modulemd    # noqa: E402
from jinja2 import Environment, PackageLoader    # noqa: E402
import koji    # noqa: E402

from .logger import log    # noqa: E402


try:
    from functools import lru_cache
except ImportError:
    def lru_cache():
        def decorator(user_function):
            cache = {}

            @wraps(user_function)
            def wrapper(*args):
                key = tuple(args)
                if key not in cache:
                    cache[key] = user_function(*args)
                return cache[key]
            return wrapper
        return decorator


def validate_mail_address(addr):
    """
    Validate e-mail address format.
    """

    mail_pattern = r"^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$"
    match = re.match(mail_pattern, addr)
    if match:
        return True

    log.error("E-mail address <%s> is not valid.", addr)
    return False


def jinja2_env(category):
    env = Environment(
        loader=PackageLoader("ursa_major", "templates/" + category)
    )

    def regex_replace(s, find, replace):
        return re.sub(find, replace, s)
    env.filters['regex_replace'] = regex_replace

    return env


def get_env_var(var, raise_if_not_exist=False):
    """
    Get variable value from os environ

    :param raise_if_not_exist: If true, raise ValueError when variable is
        not present in os environ, otherwise return None.
    """
    if var not in os.environ and raise_if_not_exist:
        raise ValueError("ENV variable '{}' does not exist.".format(var))
    return os.environ.get(var, None)


def load_mmd(yaml, is_file=False):
    """ Create Modulemd.ModuleStreamV2 object from string or file and return. """
    try:
        mmd = None
        # Modulemd.read_packager_* are supported since libmodulemd 2.11,
        # using old functions.
        if is_file:
            # mmd = Modulemd.read_packager_file(yaml)
            mmd = Modulemd.ModuleStream.read_file(yaml, False, None, None)
        else:
            # mmd = Modulemd.read_packager_string(yaml)
            mmd = Modulemd.ModuleStream.read_string(yaml, False, None, None)
        mmd = mmd.upgrade(Modulemd.ModuleStreamVersionEnum.LATEST)
    except Exception:
        error = 'Invalid modulemd: {0}'.format(yaml)
        log.error(error)
        raise

    return mmd


def requires_included(mmd_requires, config_requires):
    """Test if requires defined in config is included in module metadata

    :param mmd_requires: a mapping representing either buildrequires or
        requires, which is returned from function ``get_buildtime_modules`` and
        ``get_buildtime_streams``, or ``get_runtime_streams`` and
        ``get_runtime_modules``.
    :type mmd_requires: dict[str, Modulemd.SimpleSet]
    :param dict config_requires: a mapping representing either buildrequires or
        requires defined in config file. This is what to check if it is
        included in ``mmd_requires``.
    :return: True if all requires inside ``config_requires`` are included in
        module metadata. Otherwise, False is returned.
    :rtype: bool
    """
    for req_name, req_streams in config_requires.items():
        if req_name not in mmd_requires:
            return False

        if not isinstance(req_streams, list):
            req_streams = [req_streams]

        neg_reqs = set(s[1:] for s in req_streams if s.startswith('-'))
        pos_reqs = set(s for s in req_streams if not s.startswith('-'))

        streams = mmd_requires.get(req_name, set())
        if streams & neg_reqs:
            return False
        if pos_reqs and not (streams & pos_reqs):
            return False
    return True


def mmd_has_requires(mmd, requires):
    """
    Check whether a module represent by the mmd has requires.

    :param mmd: Modulemd.ModuleStreamV2 object
    :param requires: dict of requires, example:
        {'platform': 'f28', 'python3': 'master'}
    """
    return requires_included(mmd_get_runtime_requires(mmd), requires)


def mmd_has_buildrequires(mmd, config_buildrequires):
    """
    Check if a module metadata represented by the mmd has buildrequires.

    :param mmd: a module metadata.
    :type mmd: Modulemd.ModuleStreamV2
    :param dict config_buildrequires: a mapping of buildrequires defined in
        config file to match the module metadata, for example:
        ``{'platform': 'f28', 'python3': 'master'}``.
    :return: True if the specified module metadata has the buildrequires
        defined in config.
    :rtype: bool
    """
    return requires_included(mmd_get_buildtime_requires(mmd),
                             config_buildrequires)


def mmd_get_runtime_requires(mmd):
    """
    Check if a module metadata represented by the mmd has requires.

    :param mmd: a module metadata.
    :type mmd: Modulemd.ModuleStreamV2
    :return: a mapping transformed from requires defined in mmd,
        for example: ``{'platform': set(['f28']), 'python3': set(['master'])}``
    :rtype: dict
    """
    deps_list = mmd.get_dependencies()
    mmd_requires = {}
    if not deps_list:
        mmd_requires = {}
    else:
        mmd_requires_modules = deps_list[0].get_runtime_modules()
        for m in mmd_requires_modules:
            mmd_requires[m] = set(deps_list[0].get_runtime_streams(m))
    return mmd_requires


def mmd_get_buildtime_requires(mmd):
    """
    Check if a module metadata represented by the mmd has buildrequires.

    :param mmd: a module metadata.
    :type mmd: Modulemd.ModuleStreamV2
    :return: a mapping transformed from buildrequires defined in mmd,
        for example: ``{'platform': set(['f28']), 'python3': set(['master'])}``
    :rtype: dict
    """
    deps_list = mmd.get_dependencies()
    mmd_requires = {}
    if not deps_list:
        mmd_requires = {}
    else:
        mmd_requires_modules = deps_list[0].get_buildtime_modules()
        for m in mmd_requires_modules:
            mmd_requires[m] = set(deps_list[0].get_buildtime_streams(m))
    return mmd_requires


def nsvc_to_nvr(nsvc, plain_str=True):
    """
    Generate nvr (dict or str) for koji from an nsvc dict

    :param nsvc: N-S-V-C dict
    :type nsvc: dict[str, Any]
    :param plain_str: if True, generate a string as "N-V-R", otherwise a dict, defaults to True
    :type plain_str: bool, optional
    :return: a dict with name,version,release keys or a string as N-V-R
    :rypte: dict[str, str] or str
    """
    nvr_dict = {
        'name': nsvc['name'],
        'version': nsvc['stream'],
        'release': '{version}.{context}'.format(**nsvc)
    }
    if plain_str:
        return koji.buildLabel(nvr_dict)
    else:
        return nvr_dict


def nvr_to_nsvc(nvr, plain_str=True):
    """
    Generate nsvc (dict or str) for MBS from an nvr dict

    :param nvr: N-V-R dict
    :type nvr: dict[str, Any]
    :param plain_str: if True, generate a string as "N:S:V:C", otherwise a dict, defaults to True
    :type plain_str: bool, optional
    :return: a dict with name,stream,version,context keys or a string as N:S:V:C
    :rtype: dict[str, str] or str
    """
    parts = nvr['release'].split('.')
    if len(parts) != 2:
        raise ValueError("Invalid koji nvr for module build: {!s}".format(nvr))
    nsvc_dict = {
        'name': nvr['name'],
        'stream': nvr['version'],
        'version': parts[0],
        'context': parts[1]
    }
    if plain_str:
        return "{name}:{stream}:{version}:{context}".format(**nsvc_dict)
    else:
        return nsvc_dict


def match_any(seq, globs):
    """
    Check if any string in list matches any of the glob patterns


    :param l: list of string
    :type l: list[str]
    :param globs: list of GLOB patterns
    :type globs: list[str]
    :return: True if any matches any; True if globs is None; True if both are [], otherwise False
    :rtype: bool
    """
    if globs is None or seq == globs == []:
        return True
    return any(fnmatch(t, glob) for t in seq for glob in globs)


def find_latest_module(modules, tags_from, koji):
    """
    Get the latest(first) module within tags_from (the tags of the module build on koji matches
    any of pattern in tags_from).

    If tags_from is None, return the 1st item in modules. This is the old behavior without that
    tags_from restriction.
    If tags_from is [], the matched module shouldn't in any tags. (This might be an overkilling
    feature and we should probabliy remove it if it's not needed)

    Notes: modules list is returned by MBS API, so the expected order is from latest to the oldest.

    :param modules: modules from MBS query API
    :type modules: list[dict]
    :param tags_from: a list of glob patterns for module build tags checking
    :type tags_from: list[string] or None
    :param koji: KojiService object
    :type koji: KojiService
    :return: the latest matched item in modules, None if not matched.
    :rtype: dict or None
    """
    if tags_from is None:
        log.info(
            "No tags_from restriction. The latest module is: %s, its koji_tag is %s",
            nsvc_to_nvr(modules[0]), modules[0]['koji_tag']
        )
        return modules[0]
    else:
        log.info("Looking for modules within tags: %s", tags_from)
        for mod in modules:
            modnvr = nsvc_to_nvr(mod)
            log.debug("Validating tags of module: %s", modnvr)
            module_tags = koji.list_tags(modnvr)
            log.debug("Module build: %s is now in tags: %s", modnvr, module_tags)
            if match_any(module_tags, tags_from):
                log.info("Module build: %s (#%s) match", modnvr, mod["id"])
                return mod
            else:
                log.debug(
                    "Tags of module build: %s are not in any of %s, Ignored",
                    modnvr, tags_from
                )
        else:
            log.warning("Module not found in tags: %s", tags_from)
    return None
