gunicorn -w 1 --timeout 600 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT
