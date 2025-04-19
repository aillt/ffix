import mimetypes
import subprocess
from pathlib import Path
from typing import Annotated

import typer

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

    files = list(path.iterdir())

    for fn in files:
        if not is_video(fn):
            continue

        out_path.mkdir(parents=True, exist_ok=True)
        out_fn = out_path / f"{fn.name}"
        print(f"Converting '{fn}' to '{out_fn}'")

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
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)

            if result.returncode == 0:
                print(f"[green]Successfully converted '{fn}'")
                if not keep:
                    fn.unlink()
                    print(f"[yellow]Removed original file '{fn}'")
            else:
                print(f"[red]Error converting '{fn}'")
                print(f"[red]Error output: {result.stderr}")

        except subprocess.SubprocessError as e:
            print(f"[red]Failed to run ffmpeg: {e}")


def main():
    typer.run(run)


if __name__ == "__main__":
    main()
