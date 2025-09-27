
import shutil, os, subprocess, uuid, tempfile
from dotenv import load_dotenv
load_dotenv()
import boto3

def _ffmpeg_available():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except Exception:
        return False

def simulate_render(input_path: str, output_dir: str, text_overlay: str = "PlayableAd"):
    os.makedirs(output_dir, exist_ok=True)
    fname = os.path.basename(input_path)
    base, ext = os.path.splitext(fname)
    outname = f"{base}_rendered{ext if ext else '.mp4'}"
    outpath = os.path.join(output_dir, outname)

    # If ffmpeg exists, use drawtext. For images -> make short video first.
    if _ffmpeg_available():
        if ext.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
            tmp_video = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}_tmp.mp4")
            cmd_img = ["ffmpeg", "-y", "-loop", "1", "-i", input_path, "-c:v", "libx264", "-t", "5", "-pix_fmt", "yuv420p", tmp_video]
            subprocess.run(cmd_img, check=True)
            src = tmp_video
        else:
            src = input_path

        drawtext = f"drawtext=text='{text_overlay}':fontcolor=white:fontsize=24:x=10:y=h-30:box=1:boxcolor=black@0.5"
        cmd = ["ffmpeg", "-y", "-i", src, "-vf", drawtext, "-c:a", "copy", outpath]
        subprocess.run(cmd, check=True)
    else:
        shutil.copyfile(input_path, outpath)

    # Optionally upload to S3
    S3_BUCKET = os.getenv("S3_BUCKET") or None
    if S3_BUCKET:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
            region_name=os.getenv("S3_REGION")
        )
        key = os.path.join("outputs", os.path.basename(outpath))
        s3.upload_file(outpath, S3_BUCKET, key)
        return outpath, key

    return outpath
