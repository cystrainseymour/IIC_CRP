library(plotly)
graph <- function(path){
	my_data <- read.delim(path, sep = "\t")

	fig <- plot_ly(width = 1500)

	turb_color <- "#ff7f0e"
	rain_color <- "#1f77b4"
	temp_color <- "#9467bd"

	rain <- list(
	  tickfont = list(color = rain_color),
	  titlefont = list(color = rain_color),
	  ticksuffix = " in",
	  tickvals = (1:5)/10,
	  overlaying = "y",
	  side = "right",
	  showgrid = FALSE)

	temp <- list(
	  tickfont = list(color = temp_color),
	  titlefont = list(color = temp_color),
	  ticksuffix = " F",
	  tickvals = (14:20) * 5,
	  overlaying = "y",
	  side = "right",
	  position = 0.74,
	  showgrid = FALSE)

	fig <- fig %>% add_trace(x = as.list(my_data$Time), y = my_data$Average.Turbidity, mode = "lines+markers", name = "Average Turbidity", type = "scatter", marker = list(color = turb_color, showticklabels = FALSE), line = list(color = turb_color))

	fig <- fig %>% add_trace(x = as.list(my_data$Time), y = my_data$Rainfall, yaxis = "y2", mode = "lines+markers", name = "Hourly Rainfall (in)", type = "scatter", marker = list(color = rain_color, showticklabels = FALSE), line = list(color = rain_color))

	fig <- fig %>% add_trace(x = as.list(my_data$Time), y = my_data$Temperature, yaxis = "y3", mode = "lines+markers", name = "Temperature (F)", type = "scatter", marker = list(color = temp_color, showticklabels = FALSE), line = list(color = temp_color))

	fig <- fig %>% layout(
	  title = "Chickahominy 6/6 - 6/7", 
	  yaxis = list(
				tickfont = list(color = turb_color),
				titlefont = list(color = turb_color),
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
