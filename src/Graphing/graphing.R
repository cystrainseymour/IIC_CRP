library(plotly)
graph <- function(path){
	my_data <- read.delim(path, sep = "\t")

	fig <- plot_ly(width = 1500)

	colors <- c("#ff7f0e", "#1f77b4", "#9467bd")

	rain <- list(
	  tickfont = list(color = colors[2]),
	  titlefont = list(color = colors[2]),
	  ticksuffix = " in",
	  tickvals = (1:5)/10,
	  overlaying = "y",
	  side = "right",
	  showgrid = FALSE)

	temp <- list(
	  tickfont = list(color = colors[3]),
	  titlefont = list(color = colors[3]),
	  ticksuffix = " F",
	  tickvals = (14:20) * 5,
	  overlaying = "y",
	  side = "right",
	  position = 0.74,
	  showgrid = FALSE)

	fig <- fig %>% add_trace(x = as.list(my_data$Time), y = my_data[,2], mode = "lines+markers", name = colnames(my_data)[2], type = "scatter", marker = list(color = colors[1], showticklabels = FALSE), line = list(color = colors[1]))

	fig <- fig %>% add_trace(x = as.list(my_data$Time), y = my_data[,3], yaxis = "y2", mode = "lines+markers", name = colnames(my_data)[3], type = "scatter", marker = list(color = colors[2], showticklabels = FALSE), line = list(color = colors[2]))

	fig <- fig %>% add_trace(x = as.list(my_data$Time), y = my_data[,4], yaxis = "y3", mode = "lines+markers", name = colnames(my_data)[4], type = "scatter", marker = list(color = colors[3], showticklabels = FALSE), line = list(color = colors[3]))

	fig <- fig %>% layout(
	  title = "Chickahominy 6/6 - 6/7", 
	  yaxis = list(
				tickfont = list(color = colors[1]),
				titlefont = list(color = colors[1]),
				showgrid = FALSE),
	  yaxis2 = rain, 
	  yaxis3 = temp,
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
