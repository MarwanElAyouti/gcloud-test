provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project_id
  region      = "europe-west3"
}

resource "google_cloud_run_service" "friendlyeats_server" {
  name     = "friendlyeats_server"
  location = "europe-west3"  
  project = var.project_id
  template {
    spec {
      containers {
        image = "docker.io/marwanelayouti/friendlyeats-server:latest"
      }
    }
  }
}