library('ggplot2')
# Loading the csv file
mydata=read.csv("C:/Users/sruja/Desktop/Courses/AIT 580/Final Project/Drug-related-deaths2.csv")
mydata$Date <- as.Date(mydata$Date, format= "%m/%d/%y")
tab <- table(cut(mydata$Date, 'month'))
tab
## Format
final_df=data.frame(Date=format(as.Date(names(tab)), '%m/%Y'),
           Frequency=as.vector(tab))

final_df['Index']=1:84

plot( Frequency~Index, data = final_df,main='Count of deaths for each month from 2012 to 2018')

ggplot(final_df,aes(x=Index,y=Frequency)) +
  geom_point(shape=21, size=2, fill="green", color="black")+
  geom_smooth(method=loess, size=1.2)+
  ggtitle('Count of deaths for each month from 2012 to 2018')

final_df<-na.omit(final_df)



cor(final_df$Index,final_df$Frequency)
cor.test(final_df$Index,final_df$Frequency, method=c("pearson"))


lm.fit <- lm(Frequency~Index,data=final_df)
summary(lm.fit)
plot(lm.fit)


coef(lm.fit)

# prediction

actuals_preds <- data.frame(cbind(actuals=final_df$Frequency, predicteds=predict(lm.fit)))  # make actuals_predicteds dataframe.
correlation_accuracy <- cor(actuals_preds)  
correlation_accuracy
head(actuals_preds)

pred_vals=85:96
predict(lm.fit, data.frame(Index = pred_vals))





