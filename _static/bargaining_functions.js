






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
    window.SliderClicked = false;
    // Initialize the USDollar formatter
    window.USDollar = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
    });
}

// Function to initialize the sliders
function initializeSliders() {
    // Initialize the first slider (my_slider)
    window.my_slider = new mgslider("offer", 0, 10, 0.1);
    my_slider.f2s = function (val) {
        return '$' + val.toFixed(2);
    };
    my_slider.print(document.getElementById("my_slider"));
    // Optional: Recall the value across errors
    // my_slider.recall();

    // Initialize the second slider (slider_other)
    window.slider_other = new mgslider("other_offer", 0, 10, 0.1);
    slider_other.f2s = function (val) {
        return '$' + val.toFixed(2);
    };
    slider_other.print(document.getElementById("slider_other"));
    slider_other.set(0);
    slider_other.disable();
    // Optional: Recall the value across errors
    // slider_other.recall();
}


// This function is called when the player clicks the "Submit" button to make an offer. 
function sendOffer({ buttonId, slider, startTime, myId }) {
    const button = document.getElementById(buttonId);
    button.classList.add('active');

    const offerDetails = {
        type: 'propose',
        amount: slider.value(),
        offer_time: Math.floor(Date.now() / 1000 - startTime),
        latest_proposal_by: myId
    };

    liveSend(offerDetails);
}

// This function is called when the player clicks the "Accept" button to accept an offer.
function sendAccept({ otherProposal, startTime, myId }) {

    liveSend({
        type: 'accept',
        amount: otherProposal,
        acceptance_time: Math.floor(Date.now() / 1000 - startTime),
        accepted_by: myId
    });
}

// This function is called when the player clicks the "Terminate" button to terminate the game.
function sendTerminate({ startTime, myId }) {
    liveSend({
        type: 'terminate',
        termination_time: Math.floor(Date.now() / 1000 - startTime),
        terminated_by: myId
    });
}



function createChart(chartName, xValues, yValues, yLabel, yMin, yMax) {
    // Create a new dataset that matches the length of yValues with the xValues
    const limitedData = yValues.map((value, index) => ({
        x: xValues[index], 
        y: value
    }));

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
                data: limitedData,  // Use the mapped data
                steppedLine: true,
                pointRadius: 0,
            }],
        },
        options: {
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
                        min: 0, 
                        max: xValues.length - 1,  // Keep the full x-axis
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

function updateCurrencyElement(elementId, amount) {
    document.getElementById(elementId).innerHTML = USDollar.format(amount);
}

function updateElementText(elementId, content) {
    document.getElementById(elementId).innerHTML = content;
}

function updateCharts(data, js_vars) {
    createChart(
        chartName= 'TA_cost_chart',
        xValues= data.x_axis_values_TA_graph, 
        yValues= data.total_cost_y_values,
        yLabel="Total Transaction Costs",
        yMin= 0, 
        yMax= js_vars.y_axis_maximum_TA_graph
    );

    createChart(
        chartName= 'delay_chart',
        xValues= data.x_axis_values_delay_graph, 
        yValues= data.total_delay_y_values,
        yLabel= "Total Delay in Payment",
        yMin= 0, 
        yMax= js_vars.y_axis_maximum_delay_graph
    );
}



module.exports = {  sendAccept, sendOffer, sendTerminate, createChart } ; // Export the function for testing