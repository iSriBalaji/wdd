import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "device:app",
        host="0.0.0.0",
        port=8080,
        # ssl_certfile="cert.pem",
        # ssl_keyfile="key.pem",
        reload=True,
        log_level="debug"
    )
