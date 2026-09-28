variable "cluster_name" {
  description = "Nombre del clúster EKS."
  type        = string
}

variable "k8s_cluster_version" {
  description = "Versión de Kubernetes del clúster EKS."
  type        = string
}

variable "cluster_endpoint_public_access" {
  description = "Habilita el acceso público al endpoint del clúster."
  type        = bool
  default     = true
}

variable "node_instance_types" {
  description = "Tipos de instancia del node group gestionado."
  type        = list(string)
  default     = ["t3.medium"]
}

variable "node_desired_size" {
  description = "Cantidad deseada de nodos worker."
  type        = number
  default     = 2
}

variable "node_min_size" {
  description = "Cantidad mínima de nodos worker."
  type        = number
  default     = 1
}

variable "node_max_size" {
  description = "Cantidad máxima de nodos worker."
  type        = number
  default     = 3
}
