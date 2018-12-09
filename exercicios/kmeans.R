euclidian = function(p1, p2) {
  sqrt(sum((as.numeric(p1) - as.numeric(p2))^2))
}

kmeans = function(dados, k) {
  centroides = dados[sample(1:nrow(dados), k),]
  clus = rep(0, nrow(dados))
  repeat{
    for (i in 1:nrow(dados)) {
      current = dados[i,]
      #calcula distancia do ponto para o todos os centroides
      dists = NA
      for (j in 1:k) {
        dists[j] = euclidian(current,centroides[j,])
      }
      #poe o ponto no cluster do centroide mais proximo
      clus[i] = which.min(dists)
    }
    centroides_anteriores = centroides
    for (c in 1:k) {
      centroides[c,] = apply(dados[which(clus == c),], 2, mean)
    }
    print(centroides_anteriores)
    if(all(centroides == centroides_anteriores)) {
      break
    }
  }
  clus
}
