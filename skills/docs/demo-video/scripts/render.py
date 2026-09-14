#!/usr/bin/env python3
"""Render one inspected local HyperFrames composition; never publish or install skills."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

VERSION = "0.8.38"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--output", required=True, type=Path, help="Output stem, without suffix")
    parser.add_argument("--checked", action="store_true", help="Reuse this turn's check for unchanged input")
    args = parser.parse_args()
    project = args.project.resolve(strict=True)
    source = project / "index.html"
    if not source.is_file():
        parser.error("project must contain index.html")
    stem = args.output.resolve()
    outputs = [stem.with_suffix(suffix) for suffix in [".mp4", ".gif", ".json"]]
    if any(path.exists() for path in outputs):
        parser.error("output exists; choose a new stem to preserve the previous render")
    stem.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, DO_NOT_TRACK="1", HYPERFRAMES_NO_TELEMETRY="1")
    cli = ["npm", "exec", "--yes", "--package=hyperframes@" + VERSION, "--", "hyperframes"]
    def run(command):
        subprocess.run(command, check=True, env=env)
    if not args.checked:
        run(cli + ["check", str(project), "--snapshots"])
    run(cli + ["render", str(project), "--fps", "60", "--quality", "delivery",
               "--workers", "2", "--output", str(outputs[0])])
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-n", "-i", str(outputs[0]),
         "-filter_complex", "fps=25,scale=1200:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3",
         "-loop", "0", str(outputs[1])])
    inputs = [source, *sorted((project / "assets").glob("**/*"))]
    inputs += [path for path in [project / "index.motion.json", project / "inputs.json"] if path.is_file()]
    result = {"hyperframes": VERSION, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "inputs_sha256": {str(path.relative_to(project)): hashlib.sha256(path.read_bytes()).hexdigest()
                               for path in inputs if path.is_file()}, "outputs": []}
    for path in outputs[:2]:
        probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
            "stream=width,height,avg_frame_rate:format=duration", "-of", "json", str(path)], text=True))
        result["outputs"].append({"file": path.name, "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), **probe})
    outputs[2].write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
