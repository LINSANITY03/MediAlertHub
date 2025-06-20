import { render,screen } from "@testing-library/react";
import Home from "@/app/(client)/(dashboard)/page";
import '@testing-library/jest-dom';
import { toast } from "react-toastify";

/**
 * Mock implementation for 'react-toastify' module.
 * 
 * This mock replaces the `toast.success` method with a Jest mock function
 * to allow testing of toast notifications without invoking the real implementation.
 */
jest.mock('react-toastify', () => ({
    toast: {
        success: jest.fn(),
    }
}));

describe('Home Page', () => {
    /**
     * Runs before each test to clear localStorage and reset mocks.
     * @returns {void}
     */
    beforeEach(() => {
        localStorage.clear();
        jest.clearAllMocks();
    });

    /**
     * Tests that the logo and title render correctly on the home page.
     * @returns {void}
     */
    it('renders the logo and title', () => {
        render(<Home />);
        expect(screen.getByAltText('Picture of e-surveillance logo')).toBeInTheDocument();
        expect(screen.getByText('E-surveillance')).toBeInTheDocument();
    });

    /**
     * Tests that if a success message is present in localStorage,
     * a toast success message is shown and the message is removed.
     * @returns {void}
     */
    it('shows toast message if localstorage has successMessage', () => {
        localStorage.setItem('successMessage', 'Data registered.')
        render(<Home />);
        expect(toast.success).toHaveBeenCalledWith('Data registered.');
        expect(localStorage.getItem('successMessage')).toBeNull();
    });

    /**
     * Tests that the service section renders with the correct text.
     * @returns {void}
     */
    it('renders service section', () => {
        render(<Home />)
        expect(screen.getByText('Services')).toBeInTheDocument();
        expect(screen.getByText('Provide the details of the diagnosed condition.')).toBeInTheDocument();
    })
 })