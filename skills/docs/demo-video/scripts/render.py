#!/usr/bin/env python3
"""Render one inspected local HyperFrames composition; never publish or install skills."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

VERSION = "0.8.38"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--output", required=True, type=Path, help="Output stem, without suffix")
    parser.add_argument("--checked", action="store_true", help="Reuse this turn's check for unchanged input")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--background", help="Original flat canvas #RRGGBB; encode UI GIF directly from PNG RGB")
    mode.add_argument("--video", action="store_true", help="Delivery MP4 path for footage; exact UI colors are not guaranteed")
    args = parser.parse_args()
    if args.background and not re.fullmatch(r"#[0-9a-fA-F]{6}", args.background):
        parser.error("background must be the original canvas color in #RRGGBB format")
    project = args.project.resolve(strict=True)
    source = project / "index.html"
    if not source.is_file():
        parser.error("project must contain index.html")
    stem = args.output.resolve()
    outputs = [stem.with_suffix(suffix) for suffix in [".mp4", ".gif", ".json"]]
    if any(path.exists() for path in outputs):
        parser.error("output exists; choose a new stem to preserve the previous render")
    frames_dir = stem.with_name(stem.name + "-frames")
    if args.background and frames_dir.exists():
        parser.error("PNG frame directory exists; choose a new stem")
    stem.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, DO_NOT_TRACK="1", HYPERFRAMES_NO_TELEMETRY="1")
    cli = ["npm", "exec", "--yes", "--package=hyperframes@" + VERSION, "--", "hyperframes"]
    def run(command):
        subprocess.run(command, check=True, env=env)
    if not args.checked:
        run(cli + ["check", str(project), "--snapshots"])
    ffmpeg = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-n"]
    render = cli + ["render", str(project), "--fps", "60", "--workers", "2", "--no-best-effort"]
    frames = []
    if args.background:
        run(render + ["--format", "png-sequence", "--output", str(frames_dir)])
        frames = sorted(frames_dir.glob("*.png"))
        if not frames or [p.name for p in frames] != [f"frame_{i:06d}.png" for i in range(1, len(frames) + 1)]:
            parser.error("expected a contiguous, one-based HyperFrames PNG sequence")
        dimensions = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
            "stream=width,height", "-of", "json", str(frames[0])], text=True))["streams"][0]
        # Alpha-capable export removes the root canvas. Restore its original color,
        # then branch to RGB MP4 and GIF independently; never quantize a lossy MP4.
        matte = (f"color=c=0x{args.background[1:]}:s={dimensions['width']}x{dimensions['height']}:r=60,format=rgba[paper];"
                 "[paper][0:v]overlay=format=rgb:shortest=1,format=rgb24")
        gif_input = ffmpeg + ["-framerate", "60", "-start_number", "1", "-i", str(frames_dir / "frame_%06d.png")]
        run(gif_input + ["-filter_complex", matte, "-c:v", "libx264rgb", "-crf", "0", "-preset", "medium",
            "-pix_fmt", "rgb24", "-color_range", "pc", "-colorspace", "rgb", "-color_primaries", "bt709",
            "-color_trc", "iec61966-2-1", "-movflags", "+faststart", str(outputs[0])])
        gif_filter = matte + ",fps=25,scale=1200:-1:flags=lanczos,format=rgb24,split[a][b];[a]palettegen=stats_mode=full:reserve_transparent=0[p];[b][p]paletteuse=dither=none"
    else:
        run(render + ["--quality", "delivery", "--output", str(outputs[0])])
        gif_input = ffmpeg + ["-i", str(outputs[0])]
        gif_filter = "fps=25,scale=1200:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3"
    run(gif_input + ["-filter_complex", gif_filter, "-loop", "0", str(outputs[1])])
    inputs = [source, *sorted((project / "assets").glob("**/*"))]
    inputs += [path for path in [project / "index.motion.json", project / "inputs.json"] if path.is_file()]
    result = {"hyperframes": VERSION, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "encoding": {"path": "PNG RGB" if args.background else "delivery MP4", "canvas": args.background,
                           "mp4_role": "lossless RGB editing master" if args.background else "delivery video"},
              "verification": {"browser_playback_verified": False, "decoded_color_verified": False, "seam_reviewed": False},
              "inputs_sha256": {str(path.relative_to(project)): hashlib.sha256(path.read_bytes()).hexdigest()
                               for path in inputs if path.is_file()}, "outputs": []}
    if frames:
        result["capture"] = {"method": "HyperFrames PNG sequence", "frames": len(frames),
            "sequence_sha256": hashlib.sha256("".join(f"{p.name} {hashlib.sha256(p.read_bytes()).hexdigest()}\n" for p in frames).encode()).hexdigest()}
    for path in outputs[:2]:
        probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-show_entries",
            "stream=width,height,avg_frame_rate,nb_read_frames,pix_fmt,color_range,color_space,profile:format=duration", "-of", "json", str(path)], text=True))
        result["outputs"].append({"file": path.name, "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), **probe})
    outputs[2].write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
