from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "demo_video_render", ROOT / "skills/docs/demo-video/scripts/render.py"
)
assert SPEC is not None and SPEC.loader is not None
RENDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDER)


@pytest.mark.skipif(not shutil.which("ffmpeg") or not shutil.which("ffprobe"), reason="FFmpeg is required for actual RGB encoding")
@pytest.mark.parametrize("background", ["#ffffff", "#0d1117"])
def test_alpha_canvas_survives_actual_mp4_and_gif_encoding(tmp_path, monkeypatch, background):
    project = tmp_path / "composition"
    project.mkdir()
    (project / "index.html").write_text("<html><body>RGB fixture</body></html>")
    output = tmp_path / "intro"
    real_run = subprocess.run

    def capture_fixture(command, **kwargs):
        if command[0] != "npm":
            return real_run(command, **kwargs)
        frames = Path(command[command.index("--output") + 1])
        frames.mkdir()
        # Only HTML capture is substituted. Both delivery encoders and decoders
        # are real, including transparent-canvas compositing and GIF quantization.
        return real_run([
            "ffmpeg", "-v", "error", "-f", "lavfi", "-i",
            "color=c=black@0:s=64x48:r=60,format=rgba,drawbox=x=16:y=12:w=24:h=24:color=0x4488cc:t=fill:replace=1",
            "-frames:v", "12", "-start_number", "1", str(frames / "frame_%06d.png"),
        ], **kwargs)

    monkeypatch.setattr(subprocess, "run", capture_fixture)
    monkeypatch.setattr(sys, "argv", ["render.py", str(project), "--background", background,
                                     "--checked", "--output", str(output)])
    RENDER.main()
    receipt = json.loads(output.with_suffix(".json").read_text())
    assert receipt["capture"]["frames"] == 12
    for entry in receipt["outputs"]:
        path = tmp_path / entry["file"]
        stream = entry["streams"][0]
        pixels = subprocess.check_output([
            "ffmpeg", "-v", "error", "-i", str(path), "-frames:v", "1", "-vf", "format=rgb24", "-f", "rawvideo", "-",
        ])
        assert pixels[:3] == bytes.fromhex(background[1:])
        middle = (stream["height"] // 2 * stream["width"] + stream["width"] // 2) * 3
        assert pixels[middle:middle + 3] == bytes.fromhex("4488cc")
        assert float(entry["format"]["duration"]) == pytest.approx(0.2)
    assert receipt["outputs"][0]["streams"][0]["width"] == 64
    assert receipt["outputs"][0]["streams"][0]["height"] == 48
