
import click
import os
from .generator import generate_template

@click.command()
@click.option('--output', '-o', default='.', help='Output path for the template')
def cli(output):
    generate_template(output)



if __name__ == "__main__":
    cli()


