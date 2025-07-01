library(plotly)
graph <- function(path){
	my_data <- read.delim(path, sep = "\t")

	fig <- plot_ly(width = 1500)

	turb_color <- "#ff7f0e"
	rate_color <- "#ffff00"
	rain_color <- "#1f77b4"
	rain_prev_color <- "#08706c"
	rain_2prev_color <- "#016524"
	rain_24_color <- "#9467bd"
	
	colors <- c(turb_color, rate_color, rain_color, rain_prev_color, rain_2prev_color, rain_24_color)

	rain <- list(
	  tickfont = list(color = colors[3]),
	  titlefont = list(color = colors[3]),
	  ticksuffix = " in",
	  tickvals = (1:20)/2,
	  overlaying = "y",
	  side = "right",
	  showgrid = FALSE)
	  
	fig <- fig %>% add_trace(x = as.list(my_data[,1]), y = my_data[,2], mode = "lines+markers", name = colnames(my_data)[2], type = "scatter", marker = list(color = colors[1], showticklabels = FALSE), line = list(color = colors[1]))

	for(i in 3:length(colnames(my_data)))
	{
		fig <- fig %>% add_trace(x = as.list(my_data[,1]), y = my_data[,i], yaxis = "y2", mode = "lines+markers", name = colnames(my_data)[i], type = "scatter", marker = list(color = colors[i-1], showticklabels = FALSE), line = list(color = colors[i-1]))
	}

	fig <- fig %>% layout(
	  title = "Chickahominy 6/6 - 6/7", 
	  yaxis = list(
				tickfont = list(color = colors[1]),
				titlefont = list(color = colors[1]),
				showgrid = FALSE),
	  yaxis2 = rain,
	  xaxis = list(
				title = '', domain = c(0.3, 0.7)),
	  legend = list(x = 0.80)
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
