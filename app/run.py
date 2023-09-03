import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "general.main:app", port=8000, host="0.0.0.0",
        reload=True, reload_dirs=['/code'], log_level="info"
    )
