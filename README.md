Remux video files using ffmpeg.

## Usage

```bash
ffix -o OUTPUT_DIR [--keep] [PATH]
```

- `-o, --out-path`: Directory where remuxed videos are saved.
- `-k, --keep / --no-keep`: Keep originals (default is to delete originals).
- `PATH`: Directory containing videos to process (defaults to current directory).

Example:

```bash
ffix -o fixed_videos --keep ./my_videos
```

## License

MIT License. See [LICENSE](LICENSE) for details.
