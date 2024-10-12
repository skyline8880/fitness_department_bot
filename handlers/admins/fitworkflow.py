name: Fitness-Bot workflow

on:
  push:
    branches:
      - master
      - main

jobs:
  check_code:
    name: Check Code Quality
    runs-on: ubuntu-latest
    steps:
      - name: Check out the repo
        uses: actions/checkout@v4
      - name: Install Python 3.11
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run flake8
        run: flake8 .

  build_and_push_to_docker_hub:
    needs: check_code
    name: Push Docker image to Docker Hub
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/master' || github.ref == 'refs/heads/main'
    steps:
      - name: Check out the repo
        uses: actions/checkout@v4
      - name: Set up Docker Buildx
        uses: docker/setup-buildx@v1
      - name: Login to Docker
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Push to Docker Hub
        uses: docker/build-push-action@v2
        with:
          context: ./
          file: .
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}
