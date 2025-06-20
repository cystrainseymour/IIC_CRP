library(plotly)
graph <- function(path){
	my_data <- read.delim(path, sep = "\t")

	fig <- plot_ly(width = 1500)

	turb_color <- "#ff7f0e"
	hourly_rain_color <- "#1f77b4"
	hourly_rain_1hr_color <- "#08706c"
	hourly_rain_2hr_color <- "#016524"
	hr24_rain_color <- "#9467bd"
	
	colors <- c(turb_color, hourly_rain_color, hourly_rain_1hr_color, hourly_rain_2hr_color, hr24_rain_color)

	rain <- list(
	  tickfont = list(color = colors[2]),
	  titlefont = list(color = colors[2]),
	  ticksuffix = " in",
	  tickvals = (1:20)/10,
	  overlaying = "y",
	  side = "right",
	  showgrid = FALSE)

	fig <- fig %>% add_trace(x = as.list(my_data$Time), y = my_data$Average.Turbidity, mode = "lines+markers", name = "Average Turbidity", type = "scatter", marker = list(color = colors[1], showticklabels = FALSE), line = list(color = colors[1]))

	fig <- fig %>% add_trace(x = as.list(my_data$Time), y = my_data$Hourly.Rainfall, yaxis = "y2", mode = "lines+markers", name = "Hourly Rainfall (in)", type = "scatter", marker = list(color = colors[2], showticklabels = FALSE), line = list(color = colors[2]))

	fig <- fig %>% add_trace(x = as.list(my_data$Time), y = my_data$Hourly.Rainfall.1hr.ago, yaxis = "y2", mode = "lines+markers", name = "Hourly Rainfall 1hr ago (in)", type = "scatter", marker = list(color = colors[3], showticklabels = FALSE), line = list(color = colors[3]))

	fig <- fig %>% add_trace(x = as.list(my_data$Time), y = my_data$Hourly.Rainfall.2hrs.ago, yaxis = "y2", mode = "lines+markers", name = "Hourly Rainfall 2hrs ago (in)", type = "scatter", marker = list(color = colors[4], showticklabels = FALSE), line = list(color = colors[4]))

	fig <- fig %>% add_trace(x = as.list(my_data$Time), y = my_data$Rainfall.Past.24.Hours, yaxis = "y2", mode = "lines+markers", name = "Rainfall over past 24hrs (in)", type = "scatter", marker = list(color = colors[5], showticklabels = FALSE), line = list(color = colors[5]))

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
