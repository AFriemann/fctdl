#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import click, logging, platform, os

from . import __version__
from .config import read_config
from .factorio import Factorio

logger = logging.getLogger(__name__)

pass_factorio = click.make_pass_decorator(Factorio)

@click.group()
@click.version_option(version=__version__)
@click.option('--debug/--no-debug', default=False)
@click.option('-c', '--config', default=os.path.expanduser('~/.config/fctdl.yml'))
@click.option('-u', '--username')
@click.option('-p', '--password')
@click.pass_context
def main(ctx, debug, config, username, password):
    """main"""
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    logging.getLogger('requests').setLevel(logging.DEBUG if debug else logging.WARNING)

    cfg = read_config(config)

    if not username:
        username = cfg.username if cfg.username else click.prompt('username')
    if not password:
        password = cfg.password if cfg.password else click.prompt('password', hide_input=True)

    ctx.obj = Factorio(username, password)

@main.command()
@click.option('-a', '--architecture', type=click.Choice(['x86', 'x64']), default='x64' if '64' in platform.machine() else 'x86')
@click.argument('versions', nargs=-1)
@click.argument('path', type=click.Path(exists=True, file_okay=False, writable=True))
@pass_factorio
def get(factorio, architecture, versions, path):
    for version in versions:
        factorio.download(version, architecture, path)

@main.command()
@click.argument('branch', default='stable', type=click.Choice(['stable', 'experimental']))
@pass_factorio
def list(factorio, branch):
    factorio.list(branch)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
