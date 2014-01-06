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

    aspect3d(x=1, y=1, z=1)
    plot3d(x=swarm$x, y=swarm$y, z=swarm$z, col="black",xlim=c(0,10), ylim=c(0,10), zlim=c(0,10) )
    
    for (i in 1:length(swarm$x)) {
      rgl.lines(c(swarm$x[i], swarm$x[i] + swarm$i[i]), c(swarm$y[i], swarm$y[i] + swarm$j[i]), c(swarm$z[i],swarm$z[i] + swarm$k[i]), col="black")
    }
    
    mtext3d("x", 'x', col="black")
    mtext3d("y", 'y', col="black")
    mtext3d("z", 'z', col="black")
 
    rgl.texts(0,0,0, i, col="black")
    
    rgl.snapshot(paste("swarm_",value,".png",sep=""))
}
