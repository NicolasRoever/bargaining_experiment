function sum(a, b) {
    return a + b;
  }
  module.exports = sum;



function initializeElements() {
    // This function initializes global variables at the beginning of the game
    window.btnSliderSubmit = document.getElementById('btn-offer-slider');
    window.msgOtherProposal = document.getElementById('other-proposal');
    window.msgMyProposal = document.getElementById('my-proposal');
    window.btnAccept = document.getElementById('btn-accept');
    window.msgMyPayoffAccept = document.getElementById('my_payoff_accept');
    window.otherProposal = null;
    window.isFirstClick = true;
    window.AlreadyRefreshed = false;
    window.SliderClicked = false
}

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