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
    window.chartInstance = null;
    window.stackedBarChartInstance = null;

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

    // Set initial visibility of transaction cost elements
    setTransactionCostsVisibility(js_vars.TA_treatment);
}

// Function to initialize the sliders
function initializeSliders(slider_max_value) {
    // Initialize the first slider (my_slider)
    window.my_slider = new mgslider("offer", 0.00000000001, slider_max_value, 1);
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

/**
 * Main entrypoint: decide whether to warn or to send right away.
 *
 * @param {{ value: () => number }} slider           some p5 or UI slider giving .value()
 * @param {"Buyer"|"Seller"} player_role
 * @param {number} threshold
 * @param {Object} sendOfferParams                   whatever your sendOffer needs
 * @param {(params: Object) => void} sendOffer        function that actually does the send
 */
function processOfferSubmission(slider, player_role, threshold, sendOfferParams, sendOffer) {
    const offerValue = slider.value();
  
    if (needsWarning(offerValue, player_role, threshold)) {
      // show warning, then send once confirmed
      showWarningAndSend(() => sendOffer(sendOfferParams));
    } else {
      // immediate send
      sendOffer(sendOfferParams);
    }
}

/**
 * Show the warning overlay, wire up confirm/cancel, then sendOffer on confirm.
 *
 * @param {() => void} sendOffer      callback to actually send the offer
 */
function showWarningAndSend(sendOffer) {
    const warningDiv = document.getElementById("offer_submit_warning");
    const confirmBtn = document.getElementById("confirmButton");
    const cancelBtn  = document.getElementById("cancelButton");
  
    warningDiv.style.display = "block";
  
    function cleanup() {
      warningDiv.style.display = "none";
      confirmBtn.removeEventListener("click", onConfirm);
      cancelBtn.removeEventListener("click", onCancel);
    }
  
    function onConfirm() {
      cleanup();
      sendOffer();
    }
  
    function onCancel() {
      cleanup();
    }
  
    confirmBtn.addEventListener("click", onConfirm, { once: true });
    cancelBtn .addEventListener("click", onCancel,  { once: true });
}

/**
 * @param {number} offerValue   The value from the slider
 * @param {"Buyer"|"Seller"} role
 * @param {number} threshold    For Buyers: max they'll pay; for Sellers: min they'll accept
 * @returns {boolean}           true if we should show the warning rather than immediately sending
 */
function needsWarning(offerValue, role, threshold) {
    if (role === "Buyer") {
      // Buyer: warning if offer is ABOVE threshold
      return offerValue > threshold;
    } else {
      // Seller: warning if offer is BELOW threshold
      return offerValue < threshold;
    }
}

// This function is called when the player clicks the "Submit" button to make an offer. 
function sendOffer({ buttonId, slider, myId, myRole }) {
    const button = document.getElementById(buttonId);
    button.classList.add('active');

    const offerDetails = {
        type: 'propose',
        amount: slider.value(),
        proposal_by_id: myId, 
        proposal_by_role: myRole

    };

    liveSend(offerDetails);
}

function startCountdown(overlayId, js_vars, initialCount = 5) {
    /**
 * Starts a countdown on a specified overlay element.
 *
 * @param {string} overlayId - The DOM id of the element where the countdown will be displayed.
 * @param {object} js_vars - An object containing language settings (e.g., { langague_code: "en" }).
 * @param {number} initialCount - The starting count value (default is 5).
 */

    const overlay = document.getElementById(overlayId);
    if (!overlay) {
        console.error(`Element with id "${overlayId}" not found.`);
        return;
    }

    let count = initialCount;

    // Determine prefix based on the language code passed in js_vars.
    const prefix = (js_vars["langague_code"] === "en")
        ? "Bargaining starts in"
        : "Die Verhandlung beginnt in";

    // Initialize the overlay text immediately.
    overlay.textContent = `${prefix} ${count}`;

    // Countdown functionality using setInterval.
    const countdownInterval = setInterval(() => {
        count--;
        if (count > 0) {
            overlay.textContent = `${prefix} ${count}`;
        } else {
            overlay.style.display = 'none';
            clearInterval(countdownInterval);
        }
    }, 1000);
}

// This function is called when the player clicks the "Accept" button to accept an offer.
function sendAccept({ payoffElement, myId }) {
    // Retrieve the text content from the provided element
    const payoff = payoffElement.textContent;

    console.log("Payoff inside acceppt function",payoff);

    // Prepare the data to be sent via liveSend
    const data = {
        type: 'accept',
        amount: payoff,
        accepted_by: myId,
    };

    // Send the data
    liveSend(data);
}

// This function is called when the player clicks the "Terminate" button to terminate the game.
function sendTerminate({ myId }) {
    liveSend({
        type: 'terminate',
        terminated_by: myId
    });
}

function createChart(chartName, xValues, yValues, yLabel, yMin, yMax) {
    const ctx = document.getElementById(chartName).getContext('2d');

    // If a chart instance already exists, destroy it before creating a new one
    if (chartInstance) {
        chartInstance.destroy();
    }

    // Create the new chart and store the instance
    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: xValues,
            datasets: [{
                fill: false,
                tension: 0.4,  // Smooth curve
                backgroundColor: "rgba(0,0,255,1.0)",
                borderColor: "black",
                borderWidth: 1.5,
                data: yValues.map((value, index) => ({
                    x: xValues[index],
                    y: value
                })),
                stepped: false,
                pointRadius: 0
            }]
        },
        options: {
            animation: { duration: 0 },
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: yMin,
                    max: yMax,
                    title: {
                        display: true,
                        text: yLabel
                    }
                },
                x: {
                    type: 'category',
                    ticks: {
                        min: 0,
                        max: xValues.length - 1
                    },
                    title: {
                        display: true,
                        text: 'Seconds passed'
                    }
                }
            },
            maintainAspectRatio: true,
            aspectRatio: 1
        }
    });
}

function updateCurrencyElement(elementId, amount) {
    console.log("Attempting to update element:", elementId);
    const element = document.getElementById(elementId);
    if (!element) {
        console.log("Element not found:", elementId);
        return;
    }
    console.log("Element found, updating with amount:", amount);
    element.innerHTML = EuroFormatter.format(amount);
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
    updateElementText('time_spent', Math.round(data.bargaining_time_elapsed));

    // Update currency elements 
    if (js_vars.TA_treatment) {
        updateCurrencyElement('TA_costs', data.current_TA_costs);
        updateCurrencyElement('cumulated_TA_costs', data.cumulated_TA_costs);
        // Update charts with the provided data and js_vars
        updateCharts(data, js_vars);
    }
    
    updateCurrencyElement('my_payoff_terminate', data.current_payoff_terminate);
    updateCurrencyElement('other_payoff_terminate', -data.other_player_transaction_cost);
}

function createStackedBarChart(chartName, firstPercentage, secondPercentage) {
    const ctx = document.getElementById(chartName).getContext('2d');

    // If a chart instance already exists, destroy it before creating a new one
    if (stackedBarChartInstance) {
        stackedBarChartInstance.destroy();
    }
    // Create a new chart and store the instance
    stackedBarChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Percentage of Gains from Trade'], // Single label for the stack
            datasets: [{
                label: `You keep`, // Label for first percentage
                data: [Math.round(firstPercentage * 1000) / 10],
                backgroundColor: 'green', // Green bar for first percentage
                borderColor: 'green',
                borderWidth: 1
            }, {
                label: `You pay`, // Label for second percentage
                data: [Math.round(secondPercentage * 1000) / 10],
                backgroundColor: 'red', // Red bar for second percentage
                borderColor: 'red',
                borderWidth: 1
            }]
        },
        options: {
            animation: {
                duration: 0 // Disable animation (bars will appear instantly)
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100, // Set y-axis to 0-100%
                    ticks: {
                        callback: function(value) {
                            return value + '%'; // Add percentage sign on y-axis labels
                        }
                    },
                    stacked: true // Enable stacking
                },
                x: {
                    stacked: true // Enable stacking
                }
            },
            plugins: {
                legend: {
                    display: true, // Display legend
                    position: 'top', // Legend position
                    title: {
                        display: true,
                        text: 'Gains from Trade'
                    },
                    labels: {
                        color: 'grey', // Color of the legend text
                    }
                },
                tooltip: {
                    enabled: false // Disable tooltip
                },
                datalabels: {
                    display: true,
                    color: 'black',
                    formatter: (value, context) => {
                        return value + '%'; // Display percentage next to the bars
                    }
                }
            }
        },
        plugins: [ChartDataLabels] // Enable data labels plugin
    });
}

function showNotification(message) {
    var notification = document.getElementById("notification");
    notification.innerText = message;
    notification.style.display = "block";

    // Hide the notification after 3 seconds
    setTimeout(function() {
        notification.style.display = "none";
    }, 3000);
}

// Function to temporarily change the text color of a specific element
function changeTextColor(element_id, color, duration) {
    var element = document.getElementById(element_id);
    if (element) {
        var originalColor = element.style.color; // Save the original color

        element.style.color = color; // Change to the desired color

        // Revert the color back after the specified duration
        setTimeout(function() {
            element.style.color = originalColor;
        }, duration);
    }
}

function createSinglePercentageBarChart(chartName, percentage) {
    const ctx = document.getElementById(chartName).getContext('2d');

    // If a chart instance already exists, destroy it before creating a new one
    if (window.singlePercentageBarChartInstance) {
        window.singlePercentageBarChartInstance.destroy();
    }

    // Create a new chart and store the instance
    window.singlePercentageBarChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Percentage'],
            datasets: [{
                label: 'Percentage',
                data: [Math.round(percentage * 100)], // Round to one decimal place
                backgroundColor: 'red',
                borderColor: 'red',
                borderWidth: 1
            }]
        },
        options: {
            animation: {
                duration: 0 // Disable animation
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100, // Set y-axis to 0-100%
                    ticks: {
                        callback: function(value) {
                            return value + '%'; // Add percentage sign on y-axis labels
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false // Hide legend
                },
                tooltip: {
                    enabled: false // Disable tooltip
                },
                datalabels: {
                    display: true,
                    color: 'black',
                    anchor: 'end',
                    align: 'bottom',
                    formatter: (value) => {
                        return value + '%'; // Display percentage on top of the bar
                    }
                }
            },
            maintainAspectRatio: true,
            aspectRatio: 2
        },
        plugins: [ChartDataLabels] // Enable data labels plugin
    });
}

function updateOtherPayoffAcceptanceElementBuyer(elementId, data, js_vars) {

    console.log("Function updateOtherPayoffAcceptanceElementBuyer called");

   
    // Case 1: The buyer makes an offer and we want to show the seller's payoff.
    if (elementId == "other_payoff_other_accepts_live_buyer"){

        if (js_vars.information_asymmetry == "one-sided") {
            updateCurrencyElement(
                elementId = elementId,
                amount = (data.buyer_proposal- js_vars.other_valuation  - data.cumulated_TA_costs).toFixed(2)
            );
        } else {
            updateElementText(
                elementId = elementId,
                amount = (data.buyer_proposal.toFixed(2) + " - Objektwert Verkäufer" + (js_vars.TA_treatment ? " - Transaktionskosten ("+data.cumulated_TA_costs.toFixed(2) + "€)" : ""))
            );
        }
    } else if (elementId == "other_payoff_I_accept_buyer"){

        if (js_vars.information_asymmetry == "one-sided") {
            updateCurrencyElement(
                elementId = elementId,
                amount = (data.seller_proposal - js_vars.other_valuation - data.cumulated_TA_costs).toFixed(2)
            );
        } else {
            updateElementText(
                elementId = elementId,
                amount = (data.seller_proposal.toFixed(2) + " - Objektwert Verkäufer" + (js_vars.TA_treatment ? " - Transaktionskosten ("+data.cumulated_TA_costs.toFixed(2) + "€)" : ""))
            );
        }
    }

}

function updateOtherPayoffAcceptanceElementSeller(elementId, data, js_vars) {

    //Case 1: This is the element that shows what happens when the seller makes an offer and the buyer accepts it.
    if (elementId == "other_payoff_other_accepts_live_seller"){

        if (js_vars.language_code == "en"){
            updateElementText(
            elementId=elementId,
            content="Buyer's valuation - " + "Offer ("+data.seller_proposal.toFixed(2) + "€)" + (js_vars.TA_treatment ? " - Negotiation Costs ("+data.cumulated_TA_costs.toFixed(2) + "€)" : "")
            );
        } else if (js_vars.language_code == "de"){
        updateElementText(
            elementId=elementId,
            content="Objektwert Käufer - " + "Angebot ("+data.seller_proposal.toFixed(2) + "€)" + (js_vars.TA_treatment ? " - Verhandlungskosten ("+data.cumulated_TA_costs.toFixed(2) + "€)" : "")
        );
        } 
    } 

    //Case 2: This is the element that shows what happens when the buyer makes an offer and the seller accepts it.
    else if (elementId == "other_payoff_I_accept_seller"){

        if (js_vars.language_code == "en"){
            updateElementText(
            elementId=elementId,
            content="Buyer's valuation - " + "Offer ("+data.buyer_proposal.toFixed(2) + "€)" + (js_vars.TA_treatment ? " - Negotiation Costs ("+data.cumulated_TA_costs.toFixed(2) + "€)" : "")
            );
        } else if (js_vars.language_code == "de"){
        updateElementText(
            elementId=elementId,
            content="Objektwert Käufer - " + "Angebot ("+data.buyer_proposal.toFixed(2) + "€)" + (js_vars.TA_treatment ? " - Verhandlungskosten ("+data.cumulated_TA_costs.toFixed(2) + "€)" : "")
        );
        } 
    }
}

function setTransactionCostsVisibility(TA_treatment) {
    const taElements = document.querySelectorAll('#TA_costs, #cumulated_TA_costs, #TA_cost_chart, .three_columns_left h5, .three_columns_left p');
    taElements.forEach(element => {
        element.style.display = TA_treatment ? '' : 'none';
    });
}

module.exports = {
    sendAccept,
    sendOffer,
    sendTerminate,
    createChart,
    updateSliderDisplay,
    needsWarning,
    showWarningAndSend,
    processOfferSubmission
};