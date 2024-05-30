"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """CoffiFilter."""


if __name__ == "__main__":
    main(prog_name="coffifilter")  # pragma: no cover
