#!/usr/bin/env python
# coding:utf-8

import time
import click

from drcom.drcom import Drcom
from drcom.utils import create_logger, migrate

logger = create_logger("drcom.log")

def create_app():
    main = Drcom()
    main.login()
    if main.IS_LOGIN:
        main.get_user_info()
        logger.info("login as {0}, password: {1}. (Used {2} MB)".format(
                             main.count, main.pswd, main.used
                         ))
        # main.logger.info("Usaged {0} MB, Balance {1} MB".format(
        #     main.used, main.balance
        # ))
    else:
        logger.warning("login fail. delete {0} from conf".format(
            main.count
        ))
        main.delete_count(main.user_info)
    return main


@click.group()
def cli():
    pass


@click.command()
def run():
    CONTINUE = True
    while CONTINUE:
        app = create_app()
        start_time = time.time()
        while app.IS_LOGIN and (time.time() - start_time < 2700) and CONTINUE:
            time.sleep(0.5)
            try:
                app.get_user_info()
            except KeyboardInterrupt:
                CONTINUE = False
            except:
                break

@click.command()
def migratedb():
    migrate()

cli.add_command(run)
cli.add_command(migratedb)

if __name__ == "__main__":
    cli()
