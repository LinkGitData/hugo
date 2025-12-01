variable "project_id" {
  description = "The GCP project ID"
  type        = string
  default     = "linklin-lab"
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "The Cloud Run service name"
  type        = string
  default     = "link-blog-service"
}

variable "repository_name" {
  description = "The Artifact Registry repository name"
  type        = string
  default     = "link-blog-repo"
}
