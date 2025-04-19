# ffix

Remux video files using ffmpeg.

## Installation

- With [uv](https://docs.astral.sh/uv/):
  ```bash
  uvx ffix
  ```
- With [pipx](https://pipx.pypa.io/):
  ```bash
  pipx run ffix
  ```

## Usage

```bash
ffix -o OUTPUT_DIR [--keep] [PATH]
```

- `-o, --out-path` &nbsp; Directory to save remuxed videos.
- `-k, --keep / --no-keep` &nbsp; Keep original files (default: originals are deleted).
- `PATH` &nbsp; Directory with videos to process (default: current directory).

**Example:**
```bash
ffix -o fixed_videos --keep ./my_videos
```

## License

MIT License. See [LICENSE](LICENSE) for details.
