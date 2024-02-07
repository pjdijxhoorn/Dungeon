data "digitalocean_kubernetes_cluster" "dungeon-run" {
  name = "dungeon-run-cluster"
  depends_on = [digitalocean_kubernetes_cluster.dungeon-run]
}

provider "kubernetes" {
  host  = data.digitalocean_kubernetes_cluster.dungeon-run.endpoint
  token = data.digitalocean_kubernetes_cluster.dungeon-run.kube_config[0].token
  cluster_ca_certificate = base64decode(
    data.digitalocean_kubernetes_cluster.dungeon-run.kube_config[0].cluster_ca_certificate
  )
}

provider "helm" {
  kubernetes {
    host  = digitalocean_kubernetes_cluster.dungeon-run.endpoint
    token = digitalocean_kubernetes_cluster.dungeon-run.kube_config[0].token

    cluster_ca_certificate = base64decode(
      digitalocean_kubernetes_cluster.dungeon-run.kube_config[0].cluster_ca_certificate
    )
  }
}

resource "kubernetes_namespace" "loki-stack" {
  metadata {
    annotations = {
      name = "loki-stack"
    }

    name = "loki-stack"
  }
  depends_on = [digitalocean_kubernetes_cluster.dungeon-run]
}

resource "helm_release" "loki" {
  name       = "loki"
  repository = "https://grafana.github.io/helm-charts"
  chart      = "loki-stack"
  version    = "2.10.1"
  namespace = "loki-stack"

  values = [
    templatefile("${path.module}/../dashboard/values.yaml")
  ]

  set {
    name  = "grafana.enabled"
    value = "true"
  }

  set {
    name  = "promtail.enabled"
    value = "true"
  }
  depends_on = [kubernetes_namespace.loki-stack]
}