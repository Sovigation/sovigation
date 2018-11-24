// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Bar Chart Example
var ctx = document.getElementById("myBarChart");
var myLineChart = new Chart(ctx, {
	type : 'bar',
	data : {
		labels : [ "1학년 1학기", "1학년 2학기", "2학년 1학기", "2학년 2학기", "3학년 1학기",
				"3학년 2학기", "4학년 1학기", "4학년 2학기" ],
		datasets : [ {
			label : "Revenue",
			backgroundColor : "rgba(92,180,193,1)",
			borderColor : "rgba(2,117,216,1)",
			data : [ 0.0, 1.5, 2.0, 2.5, 3.18, 4.23, 4.21, 1.32 ],
		} ],
	},
	options : {
		scales : {
			xAxes : [ {
				time : {
					unit : 'semester'
				},
				gridLines : {
					display : false
				},
				ticks : {
					maxTicksLimit : 6
				}
			} ],
			yAxes : [ {
				ticks : {
					min : 0.0,
					max : 4.5,
					maxTicksLimit : 0.5
				},
				gridLines : {
					display : true
				}
			} ],
		},
		legend : {
			display : false
		}
	}
});
