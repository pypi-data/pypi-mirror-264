"""Command-line interface"""
import click
from es_client.defaults import OPTION_DEFAULTS
from es_client.helpers.config import (
    cli_opts, context_settings, generate_configdict, get_config, options_from_dict)
from es_client.helpers.logging import configure_logging
from es_client.helpers.utils import option_wrapper
from app.defaults import CLICK_DRYRUN, CLICK_TRACKING
from app.main import Main
from app.version import __version__

click_opt_wrap = option_wrapper() # Needed or pylint blows a fuse

# pylint: disable=unused-argument, redefined-builtin, too-many-locals, too-many-arguments
@click.command(context_settings=context_settings())
@options_from_dict(OPTION_DEFAULTS)
@click_opt_wrap(*cli_opts('dry-run', settings=CLICK_DRYRUN))
@click_opt_wrap(*cli_opts('tracking-index', settings=CLICK_TRACKING))
@click.argument('redactions_file', type=click.Path(exists=True), nargs=1)
@click.version_option(version=__version__)
@click.pass_context
def run(
    ctx, config, hosts, cloud_id, api_token, id, api_key, username, password, bearer_auth,
    opaque_id, request_timeout, http_compress, verify_certs, ca_certs, client_cert, client_key,
    ssl_assert_hostname, ssl_assert_fingerprint, ssl_version, master_only, skip_version_test,
    loglevel, logfile, logformat, blacklist, dry_run, redactions_file, tracking_index
):
    """Elastic PII Redacter"""
    get_config(ctx)
    configure_logging(ctx)
    generate_configdict(ctx)

    main = Main(ctx, redactions_file, tracking_index, dry_run)
    main.run()
