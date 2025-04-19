import mimetypes
import subprocess
from pathlib import Path
from typing import Annotated

import typer
from rich import print

mimetypes.init()


def format_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def is_video(fn: Path) -> bool:
    if not fn.is_file():
        return False
    mime_type, _ = mimetypes.guess_type(fn)
    return mime_type is not None and mime_type.startswith("video/")


def print_file_size(label: str, fn: Path, color: str) -> int:
    try:
        size = fn.stat().st_size
        print(f"[{color}]{label}: '{fn.name}' size: {format_size(size)}[/{color}]")
        return size
    except Exception as e:
        print(f"[red]Could not get size for '{fn}': {e}[/red]")
        return 0


def handle_ffmpeg_error(fn: Path, e: subprocess.CalledProcessError):
    print(
        f"[red]Error processing '{fn}' (ffmpeg exited with code {e.returncode})[/red]"
    )
    stderr_preview = e.stderr.strip().splitlines()
    if stderr_preview:
        print(
            f"[red]ffmpeg stderr: {' '.join(stderr_preview[:3])}{'...' if len(stderr_preview) > 3 else ''}[/red]"
        )
    else:
        print("[red]ffmpeg stderr: (empty)[/red]")


def process_video_file(fn: Path, out_path: Path, keep: bool) -> tuple[int, int]:
    input_size = print_file_size("Input file", fn, "cyan")
    out_path.mkdir(parents=True, exist_ok=True)
    out_fn = out_path / fn.name
    print(f"Processing '{fn}' -> '{out_fn}'")

    cmd = [
        "ffmpeg",
        "-i",
        str(fn),
        "-c",
        "copy",
        "-y",
        str(out_fn),
    ]

    try:
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
        )

        output_size = print_file_size("Output file", out_fn, "magenta")
        print(f"[green]Successfully processed '{fn}'[/green]")
        if not keep:
            try:
                fn.unlink()
                print(f"[yellow]Removed original file '{fn}'[/yellow]")
            except OSError as e:
                print(f"[red]Error removing original file '{fn}': {e}[/red]")
        return input_size, output_size

    except subprocess.CalledProcessError as e:
        handle_ffmpeg_error(fn, e)
    except subprocess.SubprocessError as e:
        print(f"[red]Failed to run ffmpeg command: {e}[/red]")
    except FileNotFoundError:
        print(
            "[red]Error: 'ffmpeg' command not found. Is ffmpeg installed and in your PATH?[/red]"
        )
    return input_size, 0


def run(
    out_path: Annotated[Path, typer.Option("--out-path", "-o")],
    keep: Annotated[bool, typer.Option("--keep/--no-keep", "-k")] = False,
    path: Annotated[Path, typer.Argument()] = Path("."),
) -> None:
    print(f"Source dir: {path.resolve()}")
    print(f"Output dir: {out_path.resolve()}")
    print(f"Keep original files: {keep}")

    files = list(path.glob("*"))
    total_input_size = 0
    total_output_size = 0

    for fn in files:
        print(f"[dim]{'=' * 79}[/dim]")
        if not is_video(fn):
            print(f"[dim]Skipping: {fn.name}[/dim]")
            continue
        input_size, output_size = process_video_file(fn, out_path, keep)
        total_input_size += input_size
        total_output_size += output_size

    print(f"[dim]{'=' * 79}[/dim]")
    print(f"[bold blue]Total input size: {format_size(total_input_size)}[/bold blue]")
    print(f"[bold blue]Total output size: {format_size(total_output_size)}[/bold blue]")


def main():
    typer.run(run)


if __name__ == "__main__":
    main()
