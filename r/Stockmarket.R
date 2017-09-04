stockmarket<-read.csv("Stockmarket.csv",sep=",",header=T)
train=(stockmarket$Year<2004)
stockmarket.test=stockmarket[!train,]
direction.test=stockmarket$Direction[!train]
library(MASS)
y=lda(Direction~Lag1+Lag2+Lag3+Lag4+Lag5,data=stockmarket,subset=train)
pred=predict(y,stockmarket.test)
pre.class=pred$class
table(pre.class,direction.test)



