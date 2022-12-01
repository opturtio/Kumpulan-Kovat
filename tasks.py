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
