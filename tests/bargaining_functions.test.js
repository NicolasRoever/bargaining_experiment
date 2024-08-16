//--------------------------------------------------------------------------------------

const    { sendAccept, sendOffer, sendTerminate }    = require('../_static/bargaining_functions.js');


//GLobal Mocks


const mockSlider = {
    value: jest.fn().mockReturnValue(5)
};

global.liveSend = jest.fn();




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

    it('Send the correct data', () => {
        
        sendOffer({
            buttonId: 'btn-offer-slider',
            slider: mockSlider,
            startTime: 1620000000,  
            myId: 123 
        });


        expect(liveSend).toHaveBeenCalledWith({
            type: 'propose',
            amount: 5,
            offer_time: expect.any(Number),
            latest_proposal_by: 123
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