"""Entry point script for EaseAI."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.easeai.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None,
    )
