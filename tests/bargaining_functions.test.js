//--------------------------------------------------------------------------------------
const { Chart } = require('chart.js');
const    { sendAccept, sendOffer, sendTerminate, createChart, updateSliderDisplay }    = require('../_static/bargaining_functions.js');




//GLobal Mocks


const mockSlider = {
    value: jest.fn().mockReturnValue(5)
};

global.liveSend = jest.fn();


jest.mock('chart.js', () => {
    return {
        Chart: jest.fn(),
    };
});

const sliderComponent = {
    id: jest.fn(() => 'test-element-id'),
    f2s: jest.fn(() => '$50.00'),
};

let targetElement;





//-----------------------------------------------------------------------------------------------
//Test sendAccept


describe('sendAccept function', () => {
    // Clear mocks before each test
    beforeEach(() => {
        liveSend.mockClear();
    });

    it('should send the correct data', () => {
        // Call sendAccept with test data
        sendAccept({
            otherProposal: 1000,
            startTime: 1620000000,  // Mocked start time
            myId: 123  // Mocked user ID
        });

        // Check if liveSend was called with the correct data
        expect(liveSend).toHaveBeenCalledWith({
            type: 'accept',
            amount: 1000,
            acceptance_time: expect.any(Number),
            accepted_by: 123
        });

    });
});

//-----------------------------------------------------------------------------------------------
//Test sendOffer



describe('sendOffer function', () => {

    // Reset mocks and DOM before each test to ensure isolation
    beforeEach(() => {

        // Clear previous mock data
        liveSend.mockClear();
        mockSlider.value.mockClear();

        // Set up the DOM
        document.body.innerHTML = `<button id="btn-offer-slider"></button>`;
    });

    it('sends the correct data', () => {

        // Set up mock data
        mockSlider.value.mockReturnValue(5);
        
        sendOffer({
            buttonId: 'btn-offer-slider',
            slider: mockSlider,
            startTime: 1620000000,  // A specific start time
            myId: 123,
            myRole: 'buyer' // Example role
        });

        expect(liveSend).toHaveBeenCalledWith({
            type: 'propose',
            amount: 5,
            offer_time: expect.any(Number),
            proposal_by_id: 123,
            proposal_by_role: 'buyer' // Expected role in the sent data
        });
    });
});

//-----------------------------------------------------------------------------------------------
//Test sendTerminate


describe('sendTerminate', () => {
    it('should call liveSend with the correct parameters', () => {

        // Fixed time for testing
        const mockDateNow = jest.spyOn(Date, 'now').mockReturnValue(1625152800000); // July 1, 2021 12:00:00 UTC

        // Test data
        const startTime = 1625152500; // Fixed start time (10 minutes earlier)
        const myId = 'player1';

        // Call the function
        sendTerminate({ startTime, myId });

        // Assert that liveSend was called with the correct data
        expect(liveSend).toHaveBeenCalledWith({
            type: 'terminate',
            termination_time: Math.floor(1625152800 - startTime),
            terminated_by: myId
        });

        // Clean up mock
        mockDateNow.mockRestore();
    });
});

//-----------------------------------------------------------------------------------------------
//Test createChart

describe('createChart', () => {
    beforeEach(() => {
        // Clear the mock before each test
        Chart.mockClear();
    });

    it('should create a chart with the correct parameters when xValues > yValues', () => {
        const chartName = 'testChart';
        const xValues = Array.from({ length: 120 }, (_, i) => i); // 120 x-values
        const yValues = Array.from({ length: 20 }, (_, i) => i * 2); // 20 y-values
        const yLabel = 'Test Y Label';
        const yMin = 0;
        const yMax = 40;

        // Call the function
        createChart(chartName, xValues, yValues, yLabel, yMin, yMax);

        // Check if the Chart constructor was called with the correct parameters
        expect(Chart).toHaveBeenCalledWith(chartName, {
            type: 'line',
            data: {
                labels: xValues,
                datasets: [{
                    fill: false,
                    lineTension: 0,
                    backgroundColor: 'rgba(0,0,255,1.0)',
                    borderColor: 'black',
                    borderWidth: 1.5,
                    data: yValues.map((value, index) => ({ x: xValues[index], y: value })),
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
                            max: yMax,
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
                            labelString: 'Seconds passed',
                        },
                    }],
                },
                maintainAspectRatio: true,
                aspectRatio: 1,
            },
        });
    });
});

//-----------------------------------------------------------------------------------------------
//Test updateSliderDisplay

beforeEach(() => {
    // Create a mock DOM element and spy on getElementById
    targetElement = document.createElement('div');
    targetElement.id = 'test-element-id';
    document.body.appendChild(targetElement);

    jest.spyOn(document, 'getElementById').mockReturnValue(targetElement);
});

afterEach(() => {
    // Clean up DOM and reset mocks
    document.body.innerHTML = '';
    jest.clearAllMocks();
});

describe('updateSliderDisplay', () => {
    it('updates the innerHTML of the target element', () => {
        updateSliderDisplay(sliderComponent, 5000); // 5000 cents = $50.00

        expect(sliderComponent.id).toHaveBeenCalledWith('cur');
        expect(sliderComponent.f2s).toHaveBeenCalledWith(50, false);
        expect(targetElement.innerHTML).toBe('$50.00');
    });
});