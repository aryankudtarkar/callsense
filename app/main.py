"""FastAPI application entry point for the SER prototype with security hardening."""

import asyncio
from pathlib import Path
from urllib.parse import urlparse
import numpy as np
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.audio import (
    MAX_BYTES,
    AudioValidationError,
    validate_audio_bytes,
)
from app.classifier import (
    MODEL_ID,
    MODEL_REVISION,
    get_classifier,
)
from app.segmentation import (
    WINDOW_DURATION_SECONDS,
    process_audio_segments,
)

app = FastAPI(
    title="Speech Emotion Recognition Prototype",
    description="Local SER review tool using emotion2vec+",
    version="0.1.0",
)

STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

ALLOWED_HOSTS = {"127.0.0.1", "localhost", "testserver"}
ALLOWED_ORIGIN_HOSTS = {"127.0.0.1", "localhost", "testserver"}

_inference_lock = asyncio.Lock()


@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    """Enforce loopback Host, reject untrusted origins, and set defensive headers."""
    raw_host = request.headers.get("host", "")
    host = raw_host.split(":")[0].strip().lower()
    if host and host not in ALLOWED_HOSTS:
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid or untrusted Host header."},
        )

    origin = request.headers.get("origin")
    if origin:
        parsed = urlparse(origin)
        origin_host = (parsed.hostname or "").lower()
        if origin_host not in ALLOWED_ORIGIN_HOSTS:
            return JSONResponse(
                status_code=403,
                content={"detail": "Cross-origin requests are forbidden."},
            )

    try:
        response = await call_next(request)
    except Exception:
        response = JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred."},
        )

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; media-src 'self' blob:; "
        "connect-src 'self'; img-src 'self' data:; frame-ancestors 'none';"
    )
    return response
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Ensure raw tracebacks, paths, or data are never leaked in error responses."""
    if isinstance(exc, HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return JSONResponse(status_code=500, content={"detail": "An internal server error occurred."})


async def read_bounded_body(request: Request, max_bytes: int = MAX_BYTES) -> bytes:
    """Read request body as a bounded byte stream into memory."""
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > max_bytes:
                raise HTTPException(
                    status_code=413,
                    detail=f"Request body exceeds {max_bytes} bytes limit.",
                )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid Content-Length header.")

    chunks = []
    total = 0
    async for chunk in request.stream():
        total += len(chunk)
        if total > max_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"Request body exceeded {max_bytes} bytes limit.",
            )
        chunks.append(chunk)

    return b"".join(chunks)


@app.get("/health")
async def health_check():
    """Local loopback health check endpoint."""
    return {"status": "ok", "app": "ser-prototype"}


@app.get("/")
async def root():
    """Serve the CallSense landing page."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    page_file = STATIC_DIR / "analyze.html"
    if page_file.exists():
        return FileResponse(page_file)
    return {"message": "SER Prototype shell active"}


@app.get("/analyze")
async def analysis_page():
    """Serve the separate local audio analysis workspace."""
    page_file = STATIC_DIR / "analyze.html"
    if page_file.exists():
        return FileResponse(page_file)
    raise HTTPException(status_code=404, detail="Analysis page is unavailable.")


@app.post("/validate")
async def validate_audio_endpoint(request: Request):
    """Validate supported WAV/MP3 input in memory without emotion inference."""
    content_type = request.headers.get("content-type", "").split(";")[0].strip().lower()

    payload = await read_bounded_body(request)
    try:
        validated = validate_audio_bytes(payload, content_type)
        return JSONResponse(
            status_code=200,
            content={
                "valid": True,
                "duration_seconds": validated.duration_seconds,
                "sample_rate": validated.sample_rate,
                "channels": 1,
                "sample_width_bytes": 2,
                "message": "Audio format is valid.",
            },
        )
    except AudioValidationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@app.post("/analyze")
async def analyze_audio_endpoint(request: Request):
    """Run local emotion2vec+ classification in chronological 5-second windows."""
    content_type = request.headers.get("content-type", "").split(";")[0].strip().lower()

    payload = await read_bounded_body(request)
    try:
        validated = validate_audio_bytes(payload, content_type)
    except AudioValidationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e

    # Concurrency control: reject if another inference is in flight
    if _inference_lock.locked():
        raise HTTPException(
            status_code=429,
            detail="Server is currently processing another audio analysis request. Please try again.",
        )

    async with _inference_lock:
        try:
            classifier = get_classifier()
        except Exception:
            raise HTTPException(
                status_code=503,
                detail="Local SER model is currently unavailable.",
            )

        try:
            waveform = np.frombuffer(validated.raw_frames, dtype=np.int16).astype(np.float32) / 32768.0
            segments = process_audio_segments(
                waveform,
                sample_rate=validated.sample_rate,
                classifier=classifier,
            )

            return JSONResponse(
                status_code=200,
                content={
                    "model_id": MODEL_ID,
                    "model_revision": MODEL_REVISION,
                    "device": classifier.device,
                    "duration_seconds": validated.duration_seconds,
                    "sample_rate": validated.sample_rate,
                    "window_duration_seconds": WINDOW_DURATION_SECONDS,
                    "segments": [s.to_dict() for s in segments],
                    "scores_label": "uncalibrated model scores",
                    "notice": (
                        "Model outputs are uncalibrated vocal-expression estimates and never "
                        "indicate truthfulness, intent, credibility, or guilt."
                    ),
                },
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Inference processing failed.",
            )
