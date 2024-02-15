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

resource "kubernetes_namespace" "monitoring-logging" {
  metadata {
    annotations = {
      name = "monitoring-logging"
    }

    name = "monitoring-logging"
  }
  depends_on = [digitalocean_kubernetes_cluster.dungeon-run]
}

resource "helm_release" "metrics_server" {
  name       = "metrics-server"
  repository = "https://kubernetes-sigs.github.io/metrics-server"
  chart      = "metrics-server"
  namespace  = "kube-system"
  depends_on = [digitalocean_kubernetes_cluster.dungeon-run]
}

resource "helm_release" "loki" {
  name       = "loki"
  repository = "https://grafana.github.io/helm-charts"
  chart      = "loki-stack"
  version    = "2.10.1"
  namespace = "monitoring-logging"

  values = [
    "${file("${path.module}/dashboard/values.yaml")}"
  ]

  set {
    name  = "grafana.enabled"
    value = "true"
  }

  set {
    name  = "promtail.enabled"
    value = "true"
  }
  depends_on = [kubernetes_namespace.monitoring-logging]
}

resource "helm_release" "prometheus" {
  name       = "prometheus"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  version    = "56.6.2"
  namespace = "monitoring-logging"
  depends_on = [kubernetes_namespace.monitoring-logging]

  set {
    name = "scrapeInterval"
    value = "30s"
  }

  set {
    name = "evaluationInterval"
    value = "30s"
  }
}

resource "kubernetes_config_map" "grafana-dashboards-custom" {
  metadata {
    name      = "grafana-dashboard-custom"
    namespace = "monitoring-logging"

    labels = {
      grafana_dashboard = 1
    }

    annotations = {
      k8s-sidecar-target-directory = "/tmp/dashboards/custom"
    }
  }

  data = {
    "dungeon-run-dashboard.json" = file("${path.module}/dashboard/dungeon-run-dashboard.json"),
  }
  depends_on = [kubernetes_namespace.monitoring-logging]
}