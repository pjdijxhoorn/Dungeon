terraform {
    cloud {
    organization = "samohtww"

    workspaces {
      name = "Dev-Ops-dungeon-run"
    }
  }
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.34.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.0.1"
    }
  }
}

variable "do_token" {}

provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_container_registry" "dungeon-run-registry" {
  name                   = "dungeon-run-registry"
  subscription_tier_slug = "basic"
  region                 = "ams3"
}

resource "digitalocean_database_cluster" "dungeon-run-database" {
  name       = "dungeon-run-database"
  engine     = "pg"
  version    = "16"
  size       = "db-s-1vcpu-1gb"
  region     = "ams3"
  node_count = 1
}

resource "digitalocean_kubernetes_cluster" "dungeon-run" {
  name    = "dungeon-run-cluster"
  region  = "ams3"
  version = "1.29.0-do.0"
  registry_integration = true

  node_pool {
    name       = "dungeon-run-cluster-pool"
    size       = "s-4vcpu-8gb"
    auto_scale = true
    min_nodes  = 1
    max_nodes  = 2
    tags = ["dungeon-run-nodes"]
  }
}