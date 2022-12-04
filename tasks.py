from invoke import task

@task
def start(ctx):
    with ctx.cd("bibtex_generator"):
        ctx.run("flask run")

@task
def lint(ctx):
    ctx.run("pylint bibtex_generator")

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive bibtex_generator")

@task
def robot(ctx):
    ctx.run("robot bibtex_generator/tests")

@task
def coverage_report(ctx):
    ctx.run("coverage erase")
    ctx.run("coverage run --branch -m pytest bibtex_generator")
    ctx.run("coverage run --branch -m robot bibtex_generator/tests")
    ctx.run("coverage combine")
    ctx.run("coverage html")