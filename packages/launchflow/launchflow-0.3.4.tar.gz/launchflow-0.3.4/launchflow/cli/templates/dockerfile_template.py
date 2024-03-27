import sys
from typing import Literal

from launchflow.cli.project_gen import Framework

DOCKERFILE_SERVICE_TEMPLATE = """\
# NOTE: This Dockerfile uses multi-stage builds for efficient caching and smaller image sizes
# Learn more at https://docs.docker.com/build/building/multi-stage/

# Build Stage 1: Build stage for installing dependencies
FROM {docker_repo_prefix}python:{python_major_version}.{python_minor_version}-slim as builder

# Set a working directory for the build stage
WORKDIR /build

# Install system dependencies required for Python packages to build
RUN apt-get update \\
    && apt-get install -y --no-install-recommends gcc libpq-dev \\
    && apt-get clean \\
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel \\
    && pip install --no-cache-dir --target=/install -r requirements.txt

# Build Stage 2: Build a final slim image for running the application
FROM {docker_repo_prefix}python:{python_major_version}.{python_minor_version}-slim

# Create a non-root user for security purposes
RUN useradd --create-home appuser
USER appuser

# Set environment variables for Python to run in unbuffered mode and not write .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT={port}

# Copy installed dependencies from the builder stage
COPY --from=builder /install /usr/local/lib/python{python_major_version}.{python_minor_version}/site-packages
ENV PATH="${{PATH}}:/usr/local/lib/python{python_major_version}.{python_minor_version}/site-packages/bin"

# Set the working directory and copy only the necessary application files
WORKDIR /code
COPY --chown=appuser:appuser ./{app_dir} /code/{app_dir}
COPY --chown=appuser:appuser ./launchflow.yaml /code/launchflow.yaml

# Expose the port the app runs on
EXPOSE {port}

# Start the application
CMD {startup_cmd}
"""


def template(framework: Framework, cloud_provider: Literal["aws", "gcp"]):
    docker_repo_prefix = ""
    if cloud_provider == "aws":
        docker_repo_prefix = "public.ecr.aws/docker/library/"
    # Dynamically get the current Python major and minor versions
    python_major_version = sys.version_info.major
    python_minor_version = sys.version_info.minor

    if framework == Framework.FASTAPI:
        startup_cmd = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
        # TODO: app_dir should be a parameter / inferred somehow
        app_dir = "app"
    else:
        raise NotImplementedError(f"{framework} is not supported yet.")

    return DOCKERFILE_SERVICE_TEMPLATE.format(
        docker_repo_prefix=docker_repo_prefix,
        python_major_version=python_major_version,
        python_minor_version=python_minor_version,
        port=8000,
        app_dir=app_dir,
        startup_cmd=startup_cmd,
    )


if __name__ == "__main__":
    print(template(Framework.FASTAPI))
