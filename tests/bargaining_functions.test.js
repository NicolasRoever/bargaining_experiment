//--------------------------------------------------------------------------------------
const    { sendAccept, sendOffer, sendTerminate, createChart, updateSliderDisplay, needsWarning, showWarningAndSend, processOfferSubmission}    = require('../_static/bargaining_functions.js');




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
    beforeAll(() => {
        // Set up the global variable with the DOM element
        document.body.innerHTML = `
            <div id="my_payoff_accept" style="display: inline">1000.50</div>
        `;
        window.mMyPayoffAccept = document.getElementById('my_payoff_accept');
    });

    beforeEach(() => {
        // Clear all mocks before each test
        liveSend.mockClear();
    });

    it('should send the correct data', () => {
        // Call sendAccept with the global variable
        sendAccept({
            payoffElement: window.mMyPayoffAccept,  // Use the global variable
            startTime: 1620000000,  // Mocked start time
            myId: 123  // Mocked user ID
        });

        // Check if liveSend was called with the correct data
        expect(liveSend).toHaveBeenCalledWith({
            type: 'accept',
            amount: 1000.50,  // Expecting this exact string value
            acceptance_time: expect.any(Number),  // Time should be a number
            accepted_by: 123  // Mocked user ID
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


//-----------------------------------------------------------------------------------------------
// Test offer submission within warning and processOfferSubmission
describe("needsWarning()", () => {
    test("Buyer under threshold → no warning", () => {
      expect(needsWarning( 50, "Buyer", 100 )).toBe(false);
    });
    test("Buyer over threshold → warning", () => {
      expect(needsWarning(150, "Buyer", 100)).toBe(true);
    });
    test("Seller above threshold → no warning", () => {
      expect(needsWarning(120, "Seller", 100)).toBe(false);
    });
    test("Seller below threshold → warning", () => {
      expect(needsWarning( 80, "Seller", 100)).toBe(true);
    });
  });


  
