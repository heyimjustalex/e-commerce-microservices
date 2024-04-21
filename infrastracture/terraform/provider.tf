terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.0"
    }
  }
}


provider "google" {
  region      = "europe-north1"
  project     = "peppy-citron-421113"
  credentials = file("peppy-citron-421113-7aca9a107652.json")
  zone        = "europe-north1-a"

}