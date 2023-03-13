### Assignment 2 ###

### Part 1, Regression analysis

#1.
#checking number of empty values and getting rid of them
sum(is.na(dataArrests))
dataArrestsModified <- na.omit(dataArrests)
sum(is.na(dataArrestsModified))

#2
#Splitting the data into subset
library(dplyr)
dataArrestsSplitted <- select(dataArrestsModified, Assault,UrbanPop,Traffic,CarAccidents,Murder)
#Visualizing the splitted data
library(funModeling)
plot_num(dataArrestsSplitted)
summary(dataArrestsSplitted)
#Showing number of negative values
sum(dataArrestsSplitted < 0)

#3 and 4
#Correlation analysis of all the variables
library(corrplot)
cor(dataArrestsModified[,c(1:10)], method = "pearson")
#Visualizing the correlation with corrplot
corrplot(cor(dataArrestsModified[,c(1:10)]), "number")

#5
#Removing one of the values with correlation > 0.8, CarAccidents
dataArrestsModified <- select(dataArrestsModified,Murder,Assault,UrbanPop,Drug,Traffic,Cyber,Kidnapping,Domestic,Alcohol)

#6
#Implementing linear regression
linRegModel=lm(Murder ~ Assault+UrbanPop+Drug+Traffic+Cyber+Kidnapping+Domestic+Alcohol, data = dataArrestsModified)
summary(linRegModel)
coef(linRegModel)

#7
#Removing Kidnapping from the model
linRegModel=lm(Murder ~ Assault+UrbanPop+Drug+Traffic+Cyber+Domestic+Alcohol, data = dataArrestsModified)
summary(linRegModel)
#Removing Alcohol from the model
linRegModel=lm(Murder ~ Assault+UrbanPop+Drug+Traffic+Cyber+Domestic, data = dataArrestsModified)
summary(linRegModel)
#Removing Domestic from the model
linRegModel=lm(Murder ~ Assault+UrbanPop+Drug+Traffic+Cyber, data = dataArrestsModified)
summary(linRegModel)
#Removing Drug from the model
linRegModel=lm(Murder ~ Assault+UrbanPop+Traffic+Cyber, data = dataArrestsModified)
summary(linRegModel)
#Removing Traffic from the model
linRegModel=lm(Murder ~ Assault+UrbanPop+Cyber, data = dataArrestsModified)
summary(linRegModel)
#Removing Cyber from the model
linRegModel=lm(Murder ~ Assault+UrbanPop, data = dataArrestsModified)
summary(linRegModel)
#Removing UrbanPop from the model
#This is not used in final model but was tested
#linRegModel=lm(Murder ~ Assault, data = dataArrestsModified)
#summary(linRegModel)

#9
#Testing the residuals
mean(residuals(linRegModel))
plot(residuals(linRegModel))
library(tsoutliers)
JarqueBera.test(residuals(linRegModel))




### Part 2, Clustering

#1.
#checking number of empty values
sum(is.na(wholesale))

#2.
#Visualizing the data
plot_num(wholesale)
summary(wholesale)

#3
#Correlation analysis
cor(wholesale[,c(1:8)], method = "pearson")
#Visualizing the correlation with corrplot
corrplot(cor(wholesale[,c(1:8)]), "number")

#4
#Creating new normalized data frame
install.packages("scales")
library(scales)
wholesaleNormalized = apply(wholesale, 2, rescale, to=c(0,1))

#5
#Using k-means
library(purrr)

tot_within_ss=map_dbl(1:10, function(k){
  kmeansmdl = kmeans(wholesaleNormalized, centers=k, nstart = 25)
  kmeansmdl$tot.withinss
})
#Elbow plot
plot(1:10,tot_within_ss,type="o",col="blue",xlab="Number of clusters k",ylab="Total WSS",main="Elbow method",panel.first=grid())

#Silhouette, Gap statistic and Calinski-Harabasz methods
library(NbClust)
silClust = NbClust(wholesaleNormalized, distance="euclidean", min.nc=2, max.nc=10, method="kmeans", index="silhouette")
GapClust = NbClust(wholesaleNormalized, distance="euclidean", min.nc=2, max.nc=10, method="kmeans", index="gap")
CHClust = NbClust(wholesaleNormalized, distance="euclidean", min.nc=2, max.nc=10, method="kmeans", index="ch")

#Visualization
par(mfrow = c(1,3))
plot(2:10,silClust$All.index,type="o",xlab="Number of clusters k",ylab="Silhouette index",panel.first = grid())
plot(2:10,GapClust$All.index,type="o",xlab="Number of clusters k",ylab="Gap statistic",panel.first = grid())
plot(2:10,CHClust$All.index,type="o",xlab="Number of clusters k",ylab="Calinski-Harabasz index",panel.first = grid())

#6.
#Using optimal number of clusters
kmeansmdl = kmeans(wholesaleNormalized, centers = 3, nstart = 25)

#Adding cluster memberships
library(dplyr)
wholesaleFinal = wholesale %>% mutate(member = factor(kmeansmdl$cluster))

#Analysing the clusters
wholesaleFinal %>%
  group_by(member)%>%
  summarise_all(list(avg = mean))

wholesaleFinal %>%
  group_by(member)%>%
  summarise_all(list(avg = mean, Std = sd))

#Visualization
par(mfrow = c(1,1))
ggplot(wholesaleFinal, aes(x = Region, y = Channel, col=member))+
  geom_point()+
  ggtitle("Clusters of the dataset")
