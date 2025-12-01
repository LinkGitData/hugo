terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
  }
  backend "gcs" {
    bucket  = "linklin-lab-tfstate"
    prefix  = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Artifact Registry
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = var.repository_name
  description   = "Docker repository for Link Blog"
  format        = "DOCKER"
  depends_on    = [google_project_service.artifactregistry]
}

# Cloud Run Service (Placeholder)
resource "google_cloud_run_v2_service" "default" {
  name     = var.service_name
  location = var.region
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello" # Placeholder
      ports {
        container_port = 8080
      }
    }
  }
  
  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
      client,
      client_version,
    ]
  }

  depends_on = [google_project_service.run]
}

# Allow unauthenticated access to Cloud Run
resource "google_cloud_run_service_iam_member" "public" {
  service  = google_cloud_run_v2_service.default.name
  location = google_cloud_run_v2_service.default.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Serverless NEG
resource "google_compute_region_network_endpoint_group" "neg" {
  name                  = "link-blog-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    service = google_cloud_run_v2_service.default.name
  }
  depends_on = [google_project_service.compute]
}

# Backend Service
resource "google_compute_backend_service" "default" {
  name      = "link-blog-backend"
  protocol  = "HTTP"
  port_name = "http"
  timeout_sec = 30
  enable_cdn  = true

  backend {
    group = google_compute_region_network_endpoint_group.neg.id
  }
}

# URL Map
resource "google_compute_url_map" "default" {
  name            = "link-blog-urlmap"
  default_service = google_compute_backend_service.default.id
}

# Global Static IP Address
resource "google_compute_global_address" "default" {
  name = "link-blog-ip"
}

# Managed SSL Certificate
resource "google_compute_managed_ssl_certificate" "default" {
  name = "link-blog-cert"

  managed {
    domains = [var.domain_name]
  }
}

# Target HTTP Proxy (for HTTP to HTTPS redirect or just HTTP access)
resource "google_compute_target_http_proxy" "default" {
  name    = "link-blog-http-proxy"
  url_map = google_compute_url_map.default.id
}

# Target HTTPS Proxy
resource "google_compute_target_https_proxy" "default" {
  name             = "link-blog-https-proxy"
  url_map          = google_compute_url_map.default.id
  ssl_certificates = [google_compute_managed_ssl_certificate.default.id]
}

# Global Forwarding Rule (HTTP)
resource "google_compute_global_forwarding_rule" "http" {
  name       = "link-blog-forwarding-rule-http"
  target     = google_compute_target_http_proxy.default.id
  port_range = "80"
  ip_address = google_compute_global_address.default.id
}

# Global Forwarding Rule (HTTPS)
resource "google_compute_global_forwarding_rule" "https" {
  name       = "link-blog-forwarding-rule-https"
  target     = google_compute_target_https_proxy.default.id
  port_range = "443"
  ip_address = google_compute_global_address.default.id
}
