from invoke import task

@task
def start(ctx):
    with ctx.cd("src/services"):
        ctx.run("flask run")

@task
def lint(ctx):
    ctx.run("pylint src")

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src")