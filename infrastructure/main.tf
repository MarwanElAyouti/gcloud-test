provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project_id
  region      = "us-central1"  # Replace with your desired region
}

resource "google_cloud_run_service" "fastapi_service" {
  name     = "fastapi-service"
  location = "us-central1"  # Replace with your desired region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/my-fastapi-app:latest"  # Replace with your Docker image tag
      }
    }
  }
}

variable "project_id" {
  description = "Google Cloud Project ID"
}

variable "credentials_file" {
  description = "Path to Google Cloud service account key file"
}
