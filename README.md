# NLU Service

This repository provides a simple NLU (Natural Language Understanding) service that can be built and run using Docker.

## Prerequisites

- Docker installed on your system.
- Git LFS installed if working with large files.

## Build the Docker Image

To build the Docker image, run the following command:

```sh
docker build -t nlu .
```

## Run the Docker Container

Once the image is built, you can run the container with:

```sh
docker run -p 8000:8000 nlu
```

This will start the service on port `8000`.

## API Endpoints

The service exposes a `/predict/` endpoint that accepts POST requests with JSON data.

### Named Entity Recognition (NER) Prediction

To use the NER model, send a request like this:

```sh
curl -X POST "http://localhost:8000/predict/" \
     -H "Content-Type: application/json" \
     -d '{"text": "Nexon vs Car", "model": "ner"}'
```

### Route Prediction

To use the route prediction model, send a request like this:

```sh
curl -X POST "http://localhost:8000/predict/" \
     -H "Content-Type: application/json" \
     -d '{"text": "Nexon vs Car", "model": "route"}'
```

## Git LFS Setup

If your repository contains large files, enable Git LFS using the following steps:

1. **Install Git LFS (if not already installed):**

   ```sh
   git lfs install
   ```

2. **Track a specific folder with large files:**

   ```sh
   git lfs track "large_files/**"
   ```

3. **Commit and push the changes:**

   ```sh
   git add .gitattributes
   git add large_files/
   git commit -m "Track large files using Git LFS"
   git push origin main
   ```

4. **Verify LFS tracking:**

   ```sh
   git lfs ls-files
   ```

5. **For cloning the repository with LFS files, use:**

   ```sh
   git clone https://github.com/user/repo.git
   git lfs pull
   ```

## Notes

- Ensure that the service is running before making API requests.
- The model parameter should be specified correctly (`ner` or `route`).

