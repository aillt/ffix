import mimetypes
import subprocess
from pathlib import Path
from typing import Annotated

import typer
from rich import print

mimetypes.init()


def is_video(fn: Path) -> bool:
    if not fn.is_file():
        return False
    mime_type, _ = mimetypes.guess_type(fn)
    return mime_type is not None and mime_type.startswith("video/")


def run(
    out_path: Annotated[Path, typer.Option("--out-path", "-o")],
    keep: Annotated[bool, typer.Option("--keep/--no-keep", "-k")] = False,
    path: Annotated[Path, typer.Argument()] = Path("."),
) -> None:
    print(f"Source dir: {path.resolve()}")
    print(f"Output dir: {out_path.resolve()}")
    print(f"Keep original files: {keep}")

    files = list(path.glob("*"))

    for fn in files:
        if not is_video(fn):
            print(f"[dim]Skipping: {fn.name}[/dim]")
            continue

        out_path.mkdir(parents=True, exist_ok=True)
        out_fn = out_path / f"{fn.name}"
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

            print(f"[green]Successfully processed '{fn}'[/green]")  # Changed message
            if not keep:
                try:
                    fn.unlink()
                    print(f"[yellow]Removed original file '{fn}'[/yellow]")
                except OSError as e:
                    print(f"[red]Error removing original file '{fn}': {e}[/red]")

        except subprocess.CalledProcessError as e:
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

        except subprocess.SubprocessError as e:
            print(f"[red]Failed to run ffmpeg command: {e}[/red]")
        except FileNotFoundError:
            print(
                "[red]Error: 'ffmpeg' command not found. Is ffmpeg installed and in your PATH?[/red]"
            )


def main():
    typer.run(run)


if __name__ == "__main__":
    main()
