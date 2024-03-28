"""Project sub command cli."""
import datetime
import io
import os
import sys
import tempfile
import time
from pathlib import Path

import click
import click.exceptions
import rich
import rich.console
import rich.json
import rich.table
from PIL import Image

import ikcli.utils.rich
from ikcli.common.cli import role_choice, visibility_choice
from ikcli.namespaces.core import Namespaces
from ikcli.users.core import Users

from .core import Projects

# Click choice on cloud providers
provider_choice = click.Choice(["AWS", "SCALEWAY_VIA_SCALEDYNAMICS"], case_sensitive=False)

# Click choice on cloud provider region
provider_region_choice = click.Choice(["FRANCE", "GERMANY", "IRELAND"], case_sensitive=False)

# Click choice on deployment flavour
provider_flavour_choice = click.Choice(["SERVERLESS", "CLUSTER", "GPU"], case_sensitive=False)

# Click choice on deployment size
provider_size_choice = click.Choice(["XS", "S", "M", "L", "XL"], case_sensitive=False)

# click choice on period
period_choice = click.Choice(["day", "yesterday", "week", "last_week", "month", "last_month"], case_sensitive=False)

# Click choice on log level
level_choice = click.Choice(["INFO", "WARNING", "ERROR"], case_sensitive=False)

# A decorator to give Projects object to commands
pass_projects = click.make_pass_decorator(Projects)


@click.group(name="project")
@click.pass_context
def cli_project(ctx):
    """Manage projects."""
    ctx.obj = Projects(ctx.obj)


@cli_project.command(name="ls")
@click.option("--name", help="Filter projects by name")
@click.option("--limit", type=int, default=20, help="Specify how many rows to display")
@pass_projects
def cli_project_list(projects, name, limit):
    """List projects."""
    ikcli.utils.rich.table(
        projects.list(name=name).limit(limit),
        "Projects",
        ["name", "path", "description", "visibility"],
    )


@cli_project.command(name="add")
@click.option("--description", help="Project description")
@click.option("--visibility", type=visibility_choice, help="Project visibility")
@click.argument("namespace")
@click.argument("name")
@pass_projects
def cli_project_add(projects, namespace, name, description, visibility):
    """Add project NAME on NAMESPACE."""
    # Get namespace
    namespace = Namespaces(projects.get_http_request()).get(name=namespace)

    # Add project
    ikcli.utils.rich.create(
        f"Add Project '{name}' to {namespace}",
        namespace.projects,
        name=name,
        description=description,
        visibility=visibility,
    )


@cli_project.command(name="show")
@click.argument("name")
@pass_projects
def cli_project_show(projects, name):
    """Show project NAME."""
    try:
        project = projects.get(name=name)
    except ikcli.net.api.exceptions.ObjectNotFoundException:
        rich.print(f"[orange3]Unable to find project {name}.")
        sys.exit(1)

    # Get member list
    members = project.members.list()
    extra = [ikcli.utils.rich.table(members, "Members", ["username", "role", "source"], display=False)]

    # Display project
    ikcli.utils.rich.show(project, "Project", ["name", "description", "visibility"], extra=extra)


@cli_project.command(name="delete")
@click.argument("name")
@pass_projects
def cli_project_delete(projects, name):
    """Delete project NAME."""
    ikcli.utils.rich.delete(projects.get(name=name))


@cli_project.command(name="push")
@click.argument("name")
@click.argument(
    "workflow_filename",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True, path_type=Path),
)
@pass_projects
def cli_project_push(projects, name, workflow_filename):
    """
    Push workflow to project.

    NAME                Project name.
    WORKFLOW_FILENAME   Path to workflow json file.
    """
    # Get project
    project = projects.get(name=name)

    # Push workflow
    console = rich.console.Console()
    with ikcli.utils.rich.HTTPTransferProgress("Workflow", project.get_http_request(), download=False, upload=True):
        workflow = project.workflows.create(workflow_filename)
    console.print(f"[green] {workflow}")


#
#   Members
#
@cli_project.group(name="member")
def cli_project_member():
    """Manage project members."""
    pass


@cli_project_member.command(name="ls")
@click.argument("project_name")
@click.option("--username", help="Filter project members by name")
@click.option("--role", type=role_choice, help="Filter project members by role")
@pass_projects
def cli_project_member_list(projects, project_name, username, role):
    """List project members."""
    # Get project and members
    project = projects.get(name=project_name)
    members = project.members.list(username=username, role=role)

    # Display on table
    ikcli.utils.rich.table(members, "Members", ["username", "role", "source"])


@cli_project_member.command(name="add")
@click.argument("project_name")
@click.argument("username")
@click.argument("role", type=role_choice)
@pass_projects
def cli_project_member_add(projects, project_name, username, role):
    """Add project members."""
    # Get project and user
    project = projects.get(name=project_name)
    user = Users(projects.get_http_request()).get(username=username)
    ikcli.utils.rich.create(
        f"Add '{username}' as {project_name}'s {role}",
        project.members,
        user=user,
        role=role,
    )


@cli_project_member.command(name="delete")
@click.argument("project_name")
@click.argument("username")
@pass_projects
def cli_project_member_delete(projects, project_name, username):
    """Remove project member."""
    # Get project and member
    project = projects.get(name=project_name)
    member = project.members.get(username=username)
    ikcli.utils.rich.delete(member)


#
#   Workflow
#
@cli_project.group(name="workflow")
def cli_workflow():
    """Manage workflows."""
    pass


@cli_workflow.command(name="ls")
@click.argument("project_name")
@click.option("--name", help="Filter workflow by name")
@click.option("--limit", type=int, default=20, help="Specify how many rows to display")
@pass_projects
def cli_workflow_list(projects, project_name, name, limit):
    """List workflows."""
    # Get project
    project = projects.get(name=project_name)

    # Display workflow
    ikcli.utils.rich.table(
        project.workflows.list(name=name).limit(limit),
        "Workflows",
        ["name", "description", "tag"],
    )


@cli_workflow.command(name="show")
@click.argument("project_name")
@click.argument("workflow_name")
@pass_projects
def cli_workflow_show(projects, project_name, workflow_name):
    """Show workflow."""
    # Get project
    project = projects.get(name=project_name)

    # Get workflow
    workflow = project.workflows.get(name=workflow_name)
    rich.print_json(data=workflow["data"])


@cli_workflow.command(name="deploy")
@click.argument("project_name")
@click.argument("workflow_name")
@click.argument("provider", type=provider_choice)
@click.argument("region", type=provider_region_choice)
@click.argument("flavour", type=provider_flavour_choice)
@click.option("--size", type=provider_size_choice, default="M")
@pass_projects
def cli_workflow_deploy(projects, project_name, workflow_name, provider, region, flavour, size):
    """Deploy workflow."""
    # Get project and workflow
    project = projects.get(name=project_name)
    workflow = project.workflows.get(name=workflow_name)

    # Create deployment
    console = rich.console.Console()
    with console.status(f"[cyan]Deploying {workflow} to {provider} {flavour} {region} ...", spinner="earth"):
        deployment = workflow.deployments.create(provider=provider, flavour=flavour, region=region, size=size)
    console.print(f"\U0001F30D  [bold green]{deployment}")


@cli_workflow.command(name="delete")
@click.argument("project_name")
@click.argument("workflow_name")
@pass_projects
def cli_workflow_delete(projects, project_name, workflow_name):
    """Delete workflow."""
    # Get project
    project = projects.get(name=project_name)

    # Delete workflow
    ikcli.utils.rich.delete(project.workflows.get(name=workflow_name))


#
#   Deployment
#
@cli_project.group(name="deployment")
def cli_deployment():
    """Manage deployments."""
    pass


@cli_deployment.command(name="ls")
@click.argument("project_name")
@click.argument("workflow_name")
@pass_projects
def cli_deployment_list(projects, project_name, workflow_name):
    """List deployments."""
    # Get project and workflow
    project = projects.get(name=project_name)
    workflow = project.workflows.get(name=workflow_name)

    # List deployments
    ikcli.utils.rich.table(
        workflow.deployments.list(),
        "Deployments",
        ["provider", "region", "flavour", "size", "tag", "status", "endpoint"],
    )


@cli_deployment.command(name="update")
@click.argument("project_name")
@click.argument("workflow_name")
@click.option("--provider", type=provider_choice, help="Cloud provider")
@click.option("--region", type=provider_region_choice, help="Cloud provider region")
@click.option("--flavour", type=provider_flavour_choice, help="Deployment flavour")
@click.option("--size", type=provider_size_choice, default=None)
@pass_projects
def cli_deployment_update(projects, project_name, workflow_name, provider, region, flavour, size):
    """Update deployment against workflow or size."""
    console = rich.console.Console()

    # Get project and workflow
    project = projects.get(name=project_name)
    workflow = project.workflows.get(name=workflow_name)

    # Get deployments to update
    deployments = [
        deployment
        for deployment in workflow.deployments.list(provider=provider, region=region, flavour=flavour)
        if (deployment["tag"] != workflow["tag"])
        or (size is not None and deployment["size"] != size)
        or deployment["status"] == "ERROR"
    ]
    if len(deployments) == 0:
        console.print("[orange3]Nothing to update")
        return

    # Display and confirm
    ikcli.utils.rich.table(
        deployments,
        "Will update these deployments",
        ["provider", "region", "flavour", "size", "tag", "status", "endpoint"],
    )

    if not rich.prompt.Confirm.ask("Continue to update ?"):
        console.print("[orange3]Aborted by user")
        return

    # Update each one
    for deployment in deployments:
        with console.status(f"[cyan]Updating {deployment} ..."):
            if size is not None:
                deployment["size"] = size
            deployment.update()
        console.print("[green]Done")


@cli_deployment.command(name="run")
@click.argument("project_name")
@click.argument("workflow_name")
@click.argument(
    "image",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True, path_type=Path),
)
@click.option("--provider", type=provider_choice, help="Cloud provider")
@click.option("--region", type=provider_region_choice, help="Cloud provider region")
@click.option("--flavour", type=provider_flavour_choice, help="Deployment flavour")
@click.option("--task", help="Workflow task to query. Will prompt user if not given")
@click.option("--output-index", type=click.INT, multiple=True, help="Output index to display (default = all)")
@click.option("--polling", type=click.INT, help="time in seconds between 2 poll when wait for response", default=5)
@pass_projects
def cli_deployment_run(
    projects, project_name, workflow_name, image, provider, region, flavour, task, output_index, polling
):
    """Call deployment endpoint on image."""
    # Get project, workflow and deployment
    project = projects.get(name=project_name)
    workflow = project.workflows.get(name=workflow_name)
    deployment = workflow.deployments.get(provider=provider, region=region, flavour=flavour)

    # If task wasn't specified, ask to user to choose one
    if task is None:
        task_options = {task["task_data"]["name"]: task["task_data"]["name"] for task in workflow["data"]["tasks"]}
        if len(task_options) == 1:
            task = next(iter(task_options))
        else:
            task = ikcli.utils.rich.menu("Choose a task", task_options)

    # Query endpoint
    console = rich.console.Console()
    with console.status(f"[cyan]Querying {deployment} ..."):
        # Get endpoint HTTPRequest object and query
        start = time.time()
        outputs = list(
            deployment.get_endpoint_http_request().run(task, image, output_indexes=output_index, polling=polling)
        )
        duration = int(time.time() - start)

    # Display outputs
    for counter, output in enumerate(outputs):
        (typ, data) = next(iter(output.items()))
        title = f"{typ} ({counter})" if len(output_index) == 0 else typ

        # If type is image, save it and display
        if typ in ("image", "image_binary"):
            image = Image.open(io.BytesIO(data))
            fd, path = tempfile.mkstemp(
                prefix=f"ikcli - {project_name} - {workflow_name} (", suffix=f") {title}.{image.format}"
            )
            with os.fdopen(fd, "w") as fh:
                image.save(fh, image.format)
            ikcli.utils.rich.show_image(path, title=title)
            data = ["Image saved as", path]

        # All data are displayed as JSON
        rich.print(
            rich.panel.Panel(
                rich.padding.Padding(rich.json.JSON.from_data(data=data), (1, 1)),
                title=title,
                width=80,
                border_style="bold green",
            )
        )

    # Print duration
    console.print(f"[green] Done in {duration} seconds")


@cli_deployment.command(name="logs")
@click.argument("project_name")
@click.argument("workflow_name")
@click.option("--provider", type=provider_choice, help="Cloud provider")
@click.option("--region", type=provider_region_choice, help="Cloud provider region")
@click.option("--flavour", type=provider_flavour_choice, help="Deployment flavour")
@click.option(
    "--level",
    type=level_choice,
    help="Filter logs on level",
)
@click.option(
    "--limit",
    type=int,
    help="Limit log count",
)
@click.option("--follow/--no-follow", default=False)
@pass_projects
def cli_deployment_logs(projects, project_name, workflow_name, provider, region, flavour, level, limit, follow):
    """Get deployment logs."""
    console = rich.console.Console()

    # Check options as 'limit' and 'follow' are mutually exclusive
    if limit is not None and follow:
        raise click.UsageError("'limit' and 'follow' are mutually exclusive")
    elif limit is None:
        limit = 1000

    # Get project and workflow
    project = projects.get(name=project_name)
    workflow = project.workflows.get(name=workflow_name)

    # Get deployment and delete
    deployment = workflow.deployments.get(provider=provider, region=region, flavour=flavour)

    # Start a loop to display logs
    start = None
    while True:
        # Get logs to display them
        response = deployment.logs(start=start, limit=limit, level=level)
        for log in response["logs"]:
            rich.print_json(data=log)

        # If no follow option, stop here
        if not follow:
            return

        # If log list was less than limit, we read end of logs.
        # Wait a bit for next one
        if len(response["logs"]) < limit:
            with console.status("[cyan]Wait for next logs ...", spinner="dots"):
                time.sleep(30)

        # Add 1 ms to last log ts_in_millis to get next logs list
        start = response["end"] + 1


def period_to_ts(period: str):  # -> tuple[float, float]:  # when >3.10
    """
    Convert a period name to a tuple of from and to timestamps.

    Args:
        period: Period name

    Returns:
        A tuple of (from, to) timestamps

    Raises:
        ValueError: when period if not supported
    """
    # Get 'to' timestamp, round second and microsecond
    to_dt = datetime.datetime.now().replace(second=0, microsecond=0)

    # If period is 'last N days' type,
    #  remouve amount of days and return results
    if period in ["day", "week", "month"]:
        if period == "day":
            days = 1
        elif period == "week":
            days = 7
        else:  # month
            days = 30
        from_dt = to_dt - datetime.timedelta(days=days)

        return (
            from_dt.timestamp(),
            to_dt.timestamp(),
        )

    # If here, period is 'previous period type',
    #  so first round hours and minutes
    to_dt = to_dt.replace(hour=0, minute=0)

    # Process each cases
    if period == "yesterday":
        from_dt = to_dt - datetime.timedelta(days=1)
    elif period == "last_week":
        to_dt = to_dt - datetime.timedelta(days=to_dt.weekday())
        from_dt = to_dt - datetime.timedelta(days=7)
    elif period == "last_month":
        to_dt = to_dt.replace(day=1)
        from_dt = (to_dt - datetime.timedelta(days=1)).replace(day=1)
    else:
        raise ValueError(f"Don't support period {period}")

    # Return results
    return (
        from_dt.timestamp(),
        to_dt.timestamp(),
    )


@cli_deployment.command(name="usage")
@click.argument("project_name")
@click.argument("workflow_name")
@click.option("--provider", type=provider_choice, help="Cloud provider")
@click.option("--region", type=provider_region_choice, help="Cloud provider region")
@click.option("--flavour", type=provider_flavour_choice, help="Deployment flavour")
@click.option("--period", type=period_choice, help="Predefined period")
@click.option("--from", "from_ts", type=int, help="Get usage since timestamp")
@click.option("--to", "to_ts", type=int, help="Get usage until timestamp")
@pass_projects
def cli_deployment_usage(projects, project_name, workflow_name, provider, region, flavour, period, from_ts, to_ts):
    """Get deployment usage."""
    # Ensure period and from/to are not define at same time
    if period is not None and (from_ts is not None or to_ts is not None):
        raise click.exceptions.BadArgumentUsage("'period' and ('from' or 'to') are mutually exclusive")

    console = rich.console.Console()

    # Get deployment
    project = projects.get(name=project_name)
    workflow = project.workflows.get(name=workflow_name)
    deployment = workflow.deployments.get(provider=provider, region=region, flavour=flavour)

    # Set default timestamp values, if needed
    if period is not None:
        (from_ts, to_ts) = period_to_ts(period)

    if to_ts is None:
        to_ts = datetime.datetime.now().replace(second=0, microsecond=0).timestamp()

    if from_ts is None:
        from_ts = (datetime.datetime.fromtimestamp(to_ts) - datetime.timedelta(hours=24)).timestamp()

    # Get usage per products
    usage = deployment.usage(int(from_ts * 1000), int(to_ts * 1000))
    usage_per_product = {data["product"]: data for data in usage}

    # If no data, give a special output
    if len(usage_per_product) == 0:
        console.print("No usage found on period", style="orange3")
        return

    # Extract all timestamps
    all_ts_in_ms = [ts for data in usage for ts in data["data"]]
    ts_in_ms = {ts: datetime.datetime.fromtimestamp(int(ts) / 1000) for ts in set(all_ts_in_ms)}

    # Start table, add all products as columns
    table = rich.table.Table(title=format(workflow), show_header=True, show_footer=True)
    table.add_column("Date", justify="right", style="cyan", footer="Total")
    for product in usage_per_product:
        # Column footer summarize total and unit
        footer = f"{usage_per_product[product]['total']} {usage_per_product[product]['unit'].lower()}s"
        table.add_column(product, footer=footer)

    # Extract values for all products / timestamps
    for ts in sorted(ts_in_ms):
        values = [format(ts_in_ms[ts])]
        for data in usage_per_product.values():
            if ts in data["data"]:
                values.append(format(data["data"][ts]))
            else:
                values.append("-")
        table.add_row(*values)

    # Finally print table
    console.print(table)


@cli_deployment.command(name="delete")
@click.argument("project_name")
@click.argument("workflow_name")
@click.option("--provider", type=provider_choice, help="Cloud provider")
@click.option("--region", type=provider_region_choice, help="Cloud provider region")
@click.option("--flavour", type=provider_flavour_choice, help="Deployment flavour")
@pass_projects
def cli_deployment_delete(projects, project_name, workflow_name, provider, region, flavour):
    """Delete deployment."""
    # Get project and workflow
    project = projects.get(name=project_name)
    workflow = project.workflows.get(name=workflow_name)

    # Get deployment and delete
    deployment = workflow.deployments.get(provider=provider, region=region, flavour=flavour)
    ikcli.utils.rich.delete(deployment)
