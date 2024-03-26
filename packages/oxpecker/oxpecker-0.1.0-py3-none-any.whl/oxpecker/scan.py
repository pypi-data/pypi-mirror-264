"""Module for scanning a project."""

import time
from pathlib import Path

import rich_click as click
from click_spinner import spinner

from oxpecker import LANGUAGES, WORK_DIR
from oxpecker.database import createdb
from oxpecker.file import upload
from oxpecker.task import create, inspect, report
from oxpecker.utils import calculate_sha256, create_zip, retry_if_network_error


@click.command(
    short_help="Scan a project and generate vulnerabilities and POC report.",
    help="""Scan a project and generate vulnerabilities and POC report.

    For now existing archive, CodeQL database etc. for the same project
    will be deleted and new ones will be generated.
    """,
)
@click.option(
    "--language",
    default="java",
    show_default=True,
    help=f"""
        The language that the new database will be used to
        analyze.

        Use `codeql resolve languages` to get a list of the
        pluggable language extractors found on the
        search path.

        When the `--db-cluster` option is given, this can
        appear multiple times, or the value can be a
        comma-separated list of languages.

        If this option is omitted, and the source root
        being analysed is a checkout of a GitHub
        repository, the CodeQL CLI will make a call to
        the GitHub API to attempt to automatically
        determine what languages to analyse. Note that
        to be able to do this, a GitHub PAT token must
        be supplied either in the environment variable
        GITHUB_TOKEN or via standard input using the
        `--github-auth-stdin` option.

        Legitimate choice is one of {LANGUAGES}.
    """,
)
@click.option(
    "--source-root",
    default=".",
    show_default=True,
    type=click.Path(),
    help="""
        The root source code directory. In
        many cases, this will be the checkout root.
        Files within it are considered to be the primary
        source files for this database. In some output
        formats, files will be referred to by their
        relative path from this directory.
        """,
)
@click.option(
    "--build-command",
    help="""
        For compiled languages, build commands that will
        cause the compiler to be invoked on the source
        code to analyze. These commands will be executed
        under an instrumentation environment that allows
        analysis of generated code and (in some cases)
        standard libraries.
        If no build command is specified, the command
        attempts to figure out automatically how to
        build the source tree, based on heuristics from
        the selected language pack.
        Beware that some combinations of multiple
        languages require an explicit build command to
        be specified.
""",
)
@click.option(
    "--build-target",
    help="Build target, only support .jar/.war for now.",
    type=click.Path(),
    required=True,
)
@click.option(
    "--sandbox-url", required=True, help="Sandbox environment URL for POC generation."
)
@click.option(
    "--sandbox-headers",
    help="HTTP headers to pass to sandbox environment, e.g. authentication credentials.",
)
@click.option(
    "--poc-start-index",
    type=click.INT,
    default=0,
    help="Start index for generating POC of candidate vulnerability.",
)
@click.option(
    "--poc-max-count",
    type=click.INT,
    default=1,
    help="Max number of vulnerabilities for generatiing POC.",
)
@click.option(
    "--wait-for-report/--no-wait-for-report",
    is_flag=True,
    show_default=True,
    default=True,
    help="Whether wait for report after scan.",
)
@click.option(
    "--precompile-jsp/--no-precompile-jsp",
    is_flag=True,
    show_default=True,
    default=False,
    help="""Enable JSP precompilation.""",
)
@click.option(
    "--ignore-gitignore/--no-ignore-gitignore",
    is_flag=True,
    default=True,
    show_default=True,
    help="Ignore patterns in .gitignore when creating source archive.",
)
@click.pass_context
@retry_if_network_error()
def scan(
    ctx,
    language,
    source_root,
    build_command,
    build_target,
    sandbox_url,
    sandbox_headers,
    poc_start_index,
    poc_max_count,
    wait_for_report,
    precompile_jsp,
    ignore_gitignore,
):  # pylint: disable=too-many-arguments,too-many-locals
    """Scan a project."""
    db_dir = WORK_DIR / "codeql-databases"
    src_dir = WORK_DIR / "sources"
    build_dir = WORK_DIR / "builds"
    db_dir.mkdir(parents=True, exist_ok=True)
    src_dir.mkdir(parents=True, exist_ok=True)
    build_dir.mkdir(parents=True, exist_ok=True)

    # create source archive
    src_archive: Path = src_dir / f"{Path(source_root).stem}.zip"
    click.secho(
        f"ℹ️  Creating source zip archive {src_archive} from {source_root}...",
        fg="blue",
        bold=True,
    )
    with spinner():
        create_zip(source_root, src_archive, ignore_gitignore=ignore_gitignore)

    # upload source archive
    click.secho(
        f"ℹ️  Uploading source zip archive {src_archive} to server...",
        fg="blue",
        bold=True,
    )
    with spinner():
        ctx.invoke(upload, filename=src_archive)

    # create codeql db
    database = db_dir / f"{Path(source_root).stem}.codeqldb"
    click.secho(
        f"ℹ️  Creating CodeQL database from source {source_root}...",
        fg="blue",
        bold=True,
    )
    with spinner():
        ctx.invoke(
            createdb,
            database=database,
            language=language,
            source_root=source_root,
            command=build_command,
            precompile_jsp=precompile_jsp,
        )

    # upload build target
    click.secho(
        f"ℹ️  Uploading build target {build_target} to server...", fg="blue", bold=True
    )
    with spinner():
        ctx.invoke(upload, filename=build_target)

    # create codeql db archive
    db_archive: Path = db_dir / f"{Path(source_root).stem}.codeqldb.zip"
    click.secho(
        f"ℹ️  Creating CodeQL database zip archive {db_archive}...", fg="blue", bold=True
    )
    with spinner():
        create_zip(database, db_dir / db_archive, ignore_gitignore=False)

    # upload codeql db archive
    click.secho(
        f"ℹ️  Uploading CodeQL database zip archive {db_archive} to server...",
        fg="blue",
        bold=True,
    )
    with spinner():
        ctx.invoke(upload, filename=db_archive)

    # create task
    click.secho("ℹ️  Creating task on server...", fg="blue", bold=True)
    task_id = ctx.invoke(
        create,
        language=language,
        source_code=calculate_sha256(src_archive),
        codeql_db=calculate_sha256(db_archive),
        build_target=calculate_sha256(build_target),
        sandbox_url=sandbox_url,
        sandbox_headers=sandbox_headers,
        poc_start_index=poc_start_index,
        poc_max_count=poc_max_count,
    )
    ctx.ensure_object(dict)
    if not task_id:
        click.secho("Task creation failed!")
        ctx.abort()

    if not wait_for_report:
        click.secho(
            f"ℹ️  Task is being processed on the server. Use `oxpecker task inspect {task_id}` to see its status.",
            fg="blue",
            bold=True,
        )
        ctx.exit()
    else:
        while True:
            try:
                click.secho(
                    "ℹ️  Task is being processed on the server. Please wait or exit by Ctrl-C now and "
                    f"use `oxpecker task inspect {task_id}` to see its status.",
                    fg="blue",
                    bold=True,
                )
                time.sleep(3)
                ctx.invoke(inspect, task_id=task_id)
                status = ctx.obj["response"].json()["taskStatus"]
                if status == "SUCCESS":
                    ctx.invoke(report, task_id=task_id)
                    ctx.exit()
                else:
                    click.secho(f"Task {task_id} status is: {status}")
                    if status == "FAILED":
                        ctx.exit()
            except InterruptedError:
                ctx.exit()
