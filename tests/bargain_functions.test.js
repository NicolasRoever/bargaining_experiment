
//--------------------------------------------------------------------
//Test sendOffer

const sendOffer = require('../_static/bargaining_functions.js');

// Mock objects

global.liveSend = jest.fn();

const mockSlider = {
    value: jest.fn().mockReturnValue(5)
};


//Test

describe('sendOffer function', () => {

    // Reset mocks and DOM before each test to ensure isolation
    beforeEach(() => {
        // Set up the DOM
        document.body.innerHTML = `<button id="btn-offer-slider"></button>`;
        
        // Clear previous mock data
        liveSend.mockClear();
        mockSlider.value.mockClear();
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

