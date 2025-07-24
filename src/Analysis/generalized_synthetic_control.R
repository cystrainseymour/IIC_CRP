library(fect)
library(readr)
library(stringr)

perform_gsynth <- function(path){
	my_data <- data.frame()
	
	files <- list.files(path)
	
	for(i in 1:length(files)){
		samp <- read.delim(paste(path, files[i], sep = "/"), sep = "\t")
		
		samp$Datetime <- parse_datetime(samp$Datetime, format = "%B %d, %Y %H:%M %p")
		
		samp$Index <- i
		my_data <- rbind(samp, my_data)
	}
	
	my_data$Treated <- as.integer(as.logical(my_data$Treated))
	
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
				r = c(0,5),
				se = TRUE,
				vartype = "parametric",
				nboots = 1000
			)
			
	return(g)
}
