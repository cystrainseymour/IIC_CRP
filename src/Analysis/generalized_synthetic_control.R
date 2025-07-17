library(fect)
library(readr)
library(stringr)

perform_gsynth <- function(times, treated, untreated){
	my_data <- data.frame()
	index <- 1
	
	times <- parse_datetime(times, format = "%Y/%m/%d %H:%M %p")
	
	for(i in 1:length(treated)){
		path <- treated[i]
		samp <- read.delim(path, sep = "\t")
		
		samp$Datetime <- parse_datetime(samp$Datetime, format = "%B %d, %Y %H:%M %p")
		
		samp$Treated <- 1*(samp$Datetime >= times[i])
		samp$Index <- index
		index <- index + 1
		my_data <- rbind(samp, my_data)
	}
	
	for(path in untreated){
		samp <- read.delim(path, sep = "\t")
		
		samp$Datetime <- parse_datetime(samp$Datetime, format = "%B %d, %Y %H:%M %p")
		
		
		samp$Treated <- FALSE
		samp$Index <- index
		index <- index + 1
		my_data <- rbind(samp, my_data)
	}
	
	turb <- ""
	for(i in colnames(my_data)){
		if(grepl("turb",i,ignore.case = TRUE)){
			turb <- i
			break
		}
	}
	
	x_cols <- colnames(my_data)[colnames(my_data) != turb]
	x_cols <- colnames(x_cols)[colnames(x_cols) != "Datetime"]
	x_cols <- colnames(x_cols)[colnames(x_cols) != "Treated"]
	x_cols <- colnames(x_cols)[colnames(x_cols) != "Index"]
	
	g <- fect(method = "gsynth", 
				data = my_data, 
				Y = turb, 
				D = "Treated", 
				X = x_cols,
				index = c("Index", "Datetime"),
				CV = FALSE,
				r = c(0,5)				
			)
			
	return(g)
}