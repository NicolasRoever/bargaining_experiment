






function initializeElements() {
    // This function initializes global variables at the beginning of the game
    window.btnSliderSubmit = document.getElementById('btn-offer-slider');
    window.msgOtherProposal = document.getElementById('other-proposal');
    window.msgMyProposal = document.getElementById('my-proposal');
    window.btnAccept = document.getElementById('btn-accept');
    window.MyPayoffAccept = document.getElementById('my_payoff_accept');
    window.otherProposal = null;
    window.isFirstClick = true;
    window.AlreadyRefreshed = false;
    window.SliderClicked = false;
    window.firstSellerProposalMade = false;
    window.firstBuyerProposalMade = false;
    // Initialize the Euro formatter
    window.EuroFormatter = {
        format: function(amount) {
            // Create a formatter with the desired locale (de-DE) but default formatting
            const formatted = new Intl.NumberFormat('de-DE', {
                style: 'currency',
                currency: 'EUR',
            }).format(amount);
    
            // Replace comma with dot for decimal separator
            return formatted.replace(/\./g, '').replace(',', '.');
        }
    };
}

// Function to initialize the sliders
function initializeSliders() {
    // Initialize the first slider (my_slider)
    window.my_slider = new mgslider("offer", 0, 100, 1);
    my_slider.f2s = function (val) {
        return val.toFixed(2) + '€';
    };
    my_slider.print(document.getElementById("my_slider"));
    // Optional: Recall the value across errors
    // my_slider.recall();

    // Initialize the second slider (slider_other)
    // window.slider_other = new mgslider("other_offer", 0, 10, 0.1);
    // slider_other.f2s = function (val) {
    //     return '$' + val.toFixed(2);
    // };
    // slider_other.print(document.getElementById("slider_other"));
    // slider_other.disable();
    // Optional: Recall the value across errors
    // slider_other.recall();
}


// This function is called when the player clicks the "Submit" button to make an offer. 
function sendOffer({ buttonId, slider, startTime, myId, myRole }) {
    const button = document.getElementById(buttonId);
    button.classList.add('active');

    const offerDetails = {
        type: 'propose',
        amount: slider.value(),
        offer_time: Math.floor(Date.now() / 1000 - startTime),
        proposal_by_id: myId, 
        proposal_by_role: myRole

    };


    liveSend(offerDetails);
}

// This function is called when the player clicks the "Accept" button to accept an offer.
function sendAccept({ payoffElement, startTime, myId }) {
    // Retrieve the text content from the provided element
    const payoff = payoffElement.textContent;

    console.log("Payoff inside acceppt function",payoff);

    // Prepare the data to be sent via liveSend
    const data = {
        type: 'accept',
        amount: payoff,
        acceptance_time: Math.floor(Date.now() / 1000 - startTime),
        accepted_by: myId,
    };

    // Send the data
    liveSend(data);
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
                lineTension: 0.4,  // Increase line tension for a smoother curve
                backgroundColor: "rgba(0,0,255,1.0)",
                borderColor: "black",
                borderWidth: 1.5,
                data: limitedData,
                steppedLine: false,  // Disable stepped line to make it smooth
                pointRadius: 0,  // Adjust point radius if you want points to be visible
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
                        max: xValues.length - 1,
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
    document.getElementById(elementId).innerHTML = EuroFormatter.format(amount);
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


function updateSliderDisplay(sliderComponent, proposalInCents) {
    // Generate the ID for the element to update
    const elementId = sliderComponent.id("cur");

    // Get the HTML element by ID
    const targetElement = document.getElementById(elementId);

    // Format the proposal amount from cents to a string (in dollars)
    const formattedValue = sliderComponent.f2s(proposalInCents / 100, false);

    // Update the inner HTML of the target element
    targetElement.innerHTML = formattedValue;
}

function enableButton(buttonId) {
    document.getElementById(buttonId).disabled = false;
}


function updateTimeChangingElements(js_vars, data) {
    // Update text elements
    updateElementText('time_spent', data.bargaining_time_elapsed);
    updateElementText('payment_delay', data.payment_delay);

    // Update currency elements 
    updateCurrencyElement('TA_costs', data.current_TA_costs * 2);
    updateCurrencyElement('cumulated_TA_costs', data.cumulated_TA_costs);
    updateCurrencyElement('my_payoff_terminate', data.current_payoff_terminate);
    updateCurrencyElement('other_payoff_terminate', -data.other_player_transaction_cost);

    // Update charts with the provided data and js_vars
    updateCharts(data, js_vars);
}



module.exports = {  sendAccept, sendOffer, sendTerminate, createChart, updateSliderDisplay } ; // Export the function for testing