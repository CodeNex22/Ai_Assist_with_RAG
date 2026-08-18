# Troubleshooting

## Backend unavailable

- Confirm that the backend container is running.
- Check the logs with `docker compose logs backend`.

## Ollama not responding

- Ensure the Ollama service is running or use the `ollama` profile.
- Verify the `OLLAMA_URL` environment variable.

## Uploads fail

- Confirm that the file size is under 5MB.
- Check that the backend can write to the shared documents volume.
