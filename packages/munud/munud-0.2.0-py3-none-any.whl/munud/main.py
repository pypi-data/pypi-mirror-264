import click
import yaml
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

from munud.cgen import build_code_from_payload_format

__version__ = "0.2.0"

BYTE_SIZE = 8


@click.group()
@click.version_option(__version__)
@click.option("-f", "--fmt", help="A file describing the wanted format.")
@click.pass_context
def main(ctx, fmt):
    ctx.ensure_object(dict)
    if not fmt:
        return

    ctx.obj["fmt"] = fmt


@main.command()
@click.option("-f", "--fmt", help="A file describing the wanted format.")
@click.option("-o", "--output", help="The output .h file.")
@click.option(
    "--crlf",
    is_flag=True,
    show_default=True,
    default=False,
    help="Use \\r\\n (crlf) as newline instead of \\n (crlf).",
)
@click.option(
    "--use-assert",
    is_flag=True,
    show_default=True,
    default=False,
    help="Generate assert check before writing to payload.",
)
@click.option(
    "--get-only",
    is_flag=True,
    show_default=True,
    default=False,
    help="Generate only getters.",
)
@click.option(
    "--set-only",
    is_flag=True,
    show_default=True,
    default=False,
    help="Generate only setters.",
)
@click.option(
    "--without-struct",
    is_flag=True,
    show_default=True,
    default=False,
    help="Do not generate a struct containing the payload.",
)
@click.option(
    "--packed-struct",
    is_flag=True,
    show_default=True,
    default=False,
    help="Add the gcc __attribute__((packed)) attribute to the struct.",
)
@click.option("-n", "--struct-name", default="Payload", help="Payload struct name.")
@click.option(
    "--without-safety-mask",
    is_flag=True,
    show_default=True,
    default=False,
    help="Removes the 0xff mask when writing ints on bytes.",
)
@click.option(
    "--payload-type",
    default="uint8_t*",
    help="The type of the payload, usually uint8_t*.",
)
@click.pass_context
def cgen(
    ctx,
    fmt,
    output,
    crlf,
    use_assert,
    get_only,
    set_only,
    without_struct,
    packed_struct,
    struct_name,
    without_safety_mask,
    payload_type,
):

    if not fmt:
        if not hasattr(ctx, "obj"):
            print("Please specify a format (--fmt).")
            return

        fmt = ctx.obj.get("fmt")
    if not fmt:
        print("Please specify a format (--fmt).")
        return

    if get_only and set_only:
        print("get-only and set-only are, obviously, mutually exclusive.")
        return

    with open(fmt, "r") as f:
        c_file_result = build_code_from_payload_format(
            yaml.safe_load(f),
            newline="\r\n" if crlf else "\n",
            use_assert=use_assert,
            generate_getters=not set_only,
            generate_setters=not get_only,
            generate_struct=not without_struct,
            packed_struct=packed_struct,
            safety_mask=not without_safety_mask,
            payload_type=payload_type,
            struct_name=struct_name,
        )

    if output:
        with open(output, "w") as outfile:
            outfile.write(c_file_result)
    else:
        console = Console()
        syntax = Syntax(c_file_result, "c")
        console.print(syntax)


@main.command()
@click.option("-f", "--fmt", help="A file describing the wanted format.")
@click.pass_context
def show(ctx, fmt):

    if not fmt:
        if not hasattr(ctx, "obj"):
            print("Please specify a format (--fmt).")
            return

        fmt = ctx.obj.get("fmt")
    if not fmt:
        print("Please specify a format (--fmt).")
        return

    table = Table(title="Payload")

    table.add_column("Type", justify="right", style="red", no_wrap=True)
    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Size (bits)", style="magenta")
    table.add_column("Byte Span", justify="right", style="green")

    with open(fmt, "r") as f:

        offset = 0
        for var in yaml.safe_load(f):
            var_size = var.get("size")
            var_name = var.get("name")
            var_type = var.get("type")

            if var_size is None:
                raise ValueError(
                    "Ill-formed payload structure: unable to find variable size"
                )

            if var_name is None:
                raise ValueError(
                    "Ill-formed payload structure: unable to find variable name"
                )

            if var_type is None:
                raise ValueError(
                    "Ill-formed payload structure: unable to find variable type"
                )

            start_bit = offset
            end_bit = offset + var_size

            bytes_start = start_bit // BYTE_SIZE
            bytes_end = end_bit // BYTE_SIZE + 1

            bit_start = start_bit % BYTE_SIZE
            bit_end = BYTE_SIZE - (end_bit % BYTE_SIZE)

            if bit_end == BYTE_SIZE:
                bit_end = 0
                bytes_end -= 1

            table.add_row(
                var_type,
                var_name,
                f"{var_size}",
                f"[{bytes_start} (+{bit_start}) - {bytes_end}]",
            )

            offset += var_size

        console = Console()
        console.print(table)

        print(f"Total payload size: {offset} bits")
