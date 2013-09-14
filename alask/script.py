#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask.ext.script import Manager, prompt_bool
from alembic.command import revision as alembic_revision
from alembic.command import upgrade as alembic_upgrade
from alembic.command import downgrade as alembic_downgrade
from alembic.command import history as alembic_history

from alask.db import get_alembic_config, get_engine, Base
from alask.web.app import app

__all__ = 'manager', 'run'

@Manager
def manager(config=None):
    config = os.path.abspath(config)
    app.config.from_pyfile(config)
    assert 'DATABASE_URL' in app.config, 'DATABASE_URL missing in config.'
    return app


@manager.option('--message', '-m', dest='message', default=None)
def revision(message):
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    m = "--autogenerate"
    alembic_revision(config,
                     message=message,
                     autogenerate=prompt_bool(m, default=True))


@manager.option('--revision', '-r', dest='revision', default='head')
def upgrade(revision):
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    alembic_upgrade(config, revision)


@manager.option('--revision', '-r', dest='revision')
def downgrade(revision):
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    alembic_downgrade(config, revision)


@manger.option('--range', '-n', dest=_range)
def history(_range=10):
    try:
        _range = int(_range)
    except ValueError:
        print "range of history MUST be `int` not %s" % str(type(_range))

    engine = get_engine()
    config, _ = get_alembic_config(engine)
    return alembic_history(config, _range)

@manager.option(manager.add_option('-c', '--config', dest='config', required=True)


def run():
    manager.run()
