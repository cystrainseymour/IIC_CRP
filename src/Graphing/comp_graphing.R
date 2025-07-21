library(plotly)
library(hash)
library(stringr)
graph <- function(path){
	my_data <- read.delim(path, sep = "\t")
	
	chart_title <- str_split_1(path,"/")
	chart_title <- chart_title[length(chart_title)-1]

	fig <- plot_ly(width = 2000)

	turb_color <- "#000000"
	pred_color <- "#000000"
	rain_color <- "#3c00ff"
	
	wind_speed_color <- "#808080"
	wind_run_color <- "#4AE1FF"
	
	temp_color <- "#ff0000"
	hi_color <- "#ff570f"
	low_color <- "#ffe608"
	thsw_color <- "#ff0aff"

	maxim <- 2.5
	for(i in my_data[,3]){
		if(i > maxim){
			maxim <- i
		}
	}
	if(maxim > 5){
		maxim <- 10
	}
	
	rain <- list(
	  tickfont = list(color = rain_color),
	  titlefont = list(color = rain_color),
	  ticksuffix = " in",
	  
	  overlaying = "y",
	  side = "right",
	  tick0 = 0,
	  dtick = maxim/5,
	  autorangeoptions = list(max = 2.5, min = 0),
	  ticklabeloverflow = "hide past div",
	  
	  rangemode = "tozero",
	  showgrid = FALSE)

	temp <- list(
	  tickfont = list(color = temp_color),
	  titlefont = list(color = temp_color),
	  ticksuffix = "° C",
	  tickvals = (0:12)*5,
	  
	  overlaying = "y",
	  side = "left",
	  position = 0.25,
	  
	  
	  
	  showgrid = FALSE)

	wind_speed <- list(
	  tickfont = list(color = wind_speed_color),
	  titlefont = list(color = wind_speed_color),
	  ticksuffix = " mph",
	  tickvals = (0:6)*5,
	  range = 0:6,
	  overlaying = "y",
	  side = "right",
	  position = 0.75,
	  rangemode = "tozero",
	  
	  minallowed = 30,
	  showgrid = FALSE)

	wind_run <- list(
	  tickfont = list(color = wind_run_color),
	  titlefont = list(color = wind_run_color),
	  ticksuffix = " mi",
	  tickvals = (0:10)/5,
	  range = 0:2,
	  overlaying = "y",
	  side = "right",
	  position = 0.8,
	  
	  rangemode = "tozero",
	  showgrid = FALSE)
	
	entries <- hash()
	entries[["speed"]] <- c(wind_speed_color, "y4", "Wind Speed")
	entries[["run"]] <- c(wind_run_color, "y5", "Wind Run")
	entries[["rainfall"]] <- c(rain_color, "y2", "10m Rainfall")
	entries[["temperature"]] <- c(temp_color, "y3", "Temperature")
	entries[["high"]] <- c(hi_color, "y3", "High Temp")
	entries[["low"]] <- c(low_color, "y3", "Low Temp")
	entries[["thsw"]] <- c(thsw_color, "y3", "THSW Index")
	entries[["predictions"]] <- c(pred_color, "y1", "Predictions")
	  
	fig <- fig %>% add_trace(x = as.list(my_data[,1]), y = my_data[,2], mode = "lines+markers", name = colnames(my_data)[2], type = "scatter", marker = list(color = turb_color, showticklabels = FALSE), line = list(color = turb_color))

	for(i in 3:length(colnames(my_data))){
		name_vec <- str_split_1(colnames(my_data)[i], "\\.")
		
		count <- 1
		
		entry <- entries[[tolower(name_vec[count])]]
		while(is.null(entry)){
			entry <- entries[[tolower(name_vec[count])]]
			count <- count + 1
		}
		fig <- fig %>% add_trace(x = as.list(my_data[,1]), y = my_data[,i], yaxis = entry[2], mode = "lines+markers", name = colnames(my_data)[i], type = "scatter", marker = list(color = entry[1], showticklabels = FALSE), line = list(color = entry[1]))
	}

	fig <- fig %>% layout(
	  title = chart_title,
	  yaxis = list(
				tickfont = list(color = turb_color),
				titlefont = list(color = turb_color),
				showgrid = FALSE),
	  yaxis2 = rain,
	  yaxis3 = temp,
	  yaxis4 = wind_speed,
	  yaxis5 = wind_run,
	  xaxis = list(
				title = '', domain = c(0.3, 0.7)),
	  legend = list(x = 0.85)
	)%>%
	  layout(plot_bgcolor='#ffffff',
			  xaxis = list(
				zerolinecolor = '#ffff',
				zerolinewidth = 2,
				showgrid = FALSE),
			  yaxis = list(
				zerolinecolor = '#ffff',
				zerolinewidth = 2,
				showgrid = FALSE)
          )
	print(fig)
}
