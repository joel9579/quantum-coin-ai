# Build the image
docker build -t crypto-forecast-app .

# Run the container
docker run -p 8000:8000 crypto-forecast-app