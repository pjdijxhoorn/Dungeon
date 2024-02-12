data "digitalocean_kubernetes_cluster" "dungeon-run-2" {
  name = "dungeon-run-cluster"
  depends_on = [digitalocean_kubernetes_cluster.dungeon-run]
}

resource "kubernetes_namespace" "kubernetes-dashboard" {
  metadata {
    annotations = {
      name = "kubernetes-dashboard"
    }
    name = "kubernetes-dashboard"
  }
  depends_on = [digitalocean_kubernetes_cluster.dungeon-run]
}

resource "helm_release" "kubernetes-dashboard" {
  name = "kubernetes-dashboard"
  repository = "https://kubernetes.github.io/dashboard/"
  chart      = "kubernetes-dashboard"
  namespace  = "kubernetes-dashboard"

  set {
    name  = "protocolHttp"
    value = "true"
  }

  set {
    name  = "service.externalPort"
    value = 80
  }

  set {
    name  = "rbac.clusterReadOnlyRole"
    value = "true"
  }
  depends_on = [kubernetes_namespace.kubernetes-dashboard]
}