\
function createChart(chartName, yValues, yLabel, yMin, yMax) {
    new Chart(chartName, {
    type: "line",
    data: {
        labels: xValues,
        datasets: [{
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(0,0,255,1.0)",
            borderColor: "black",
            borderWidth: 1.5,
            data: yValues, 
            step: true,
            fill: false,
            pointRadius: 0,
        }],
    },
    options: {
        //responsive: true, 
        animation: { duration: 0 },
        legend: { display: false },
        scales: {
            yAxes: [{
                ticks: {
                    min: yMin, 
                    max: yMax
                },
                scaleLabel: {
                    display: true, 
                    labelString: yLabel,
                },
            }],
            xAxes: [{
                type: 'category',
                ticks: {
                    //beginAtZero: true,
                    //stepSize: 20,
                    min: 0, 
                    max: xValues.length,
                },
                scaleLabel: {
                    display: true, 
                    labelString: "Seconds passed",
                },
            }]
        },
        maintainAspectRatio: true,
        aspectRatio: 1,
    }
    });
}