euclidian = function(p1, p2) {
  sqrt(sum((p1 - p2)^2))
}

kmeans = function(dados, k) {
  centroides = dados[sample(1:nrow(dados), k),]
  print(centroides)
  clus = NA
  for (i in 1:nrow(dados)) {
    current = dados[i,]
    #calcula distancia do ponto para o todos os centroides
    dists = NA
    for (j in 1:k) {
      print(current)
      print(centroides[j,])
      dists[j] = euclidian(current,centroides[j,])
      print(dists[j])
    }
    #poe o ponto no cluster do centroide mais proximo
    print(dists)
    clus[i] = which.min(dists)
  }
  clus
}
