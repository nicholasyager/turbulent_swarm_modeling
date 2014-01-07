require(rgl)

swarmfiles = dir(pattern="*.csv")

rgl.open()
bg3d("white")


for (i in 1:length(swarmfiles)){

    i = as.numeric(i)
    value = formatC(as.numeric(i), width = 3, format = "d", flag = "0")
    rgl.clear()
    swarm = read.csv(swarmfiles[i])
  
    print(i)    

    colors = rainbow(length(swarm$x))
    
    aspect3d(x=1, y=1, z=1)
    plot3d(x=swarm$x, y=swarm$y, z=swarm$z, col=colors,xlim=c(0,10), ylim=c(0,10), zlim=c(0,10) )
    
    n = 200
    theta <- seq(0, 2*pi, len=n)
    
    x <- 5 + 5 * cos(theta)
    x2 <- 5 + 7 * cos(theta)
    x3 <- 5 + 3 * cos(theta)
    z <- 5 + 5 * sin(theta)
    z2 <- 5 + 7 * sin(theta) 
    z3 <- 5 + 3 * sin(theta) 
    y <- rep(5, n) 
    lines3d(x,y,z)
    lines3d(x2,y,z2, col="gray") 
    lines3d(x3,y,z3, col="gray") 
    
    rgl.lines(c(5,5), c(0, 10), c(5,5),col="gray")
    
    for (j in 1:length(swarm$x)) {
      rgl.lines(c(swarm$x[j], swarm$x[j] + swarm$i[j]), c(swarm$y[j], swarm$y[j] + swarm$j[j]), c(swarm$z[j],swarm$z[j] + swarm$k[j]), col=colors[j])
    }
    
    rgl.snapshot(paste("swarm_",value,".png",sep=""))
}
