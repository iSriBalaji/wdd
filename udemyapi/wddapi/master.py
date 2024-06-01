import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8081,
        # ssl_certfile="cert.pem",
        # ssl_keyfile="key.pem",
        reload=True,
        log_level="debug"
    )
