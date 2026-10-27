from pathlib import Path


def write_final_subtitles(output_directory: Path, video_stem: str, corrected_srt: str) -> Path:
    final_srt = output_directory / f"{video_stem}.srt"
    final_srt.write_text(corrected_srt, encoding="utf-8")
    return final_srt
