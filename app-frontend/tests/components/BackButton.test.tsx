import { render, screen } from "@testing-library/react";
import BackLink from "@/components/BackButton";
import { describe, it } from '@jest/globals';

/**
 * Tests for the BackLink component.
 * 
 * This suite of tests ensures that the BackLink component renders correctly, 
 * including the "Back" text and the associated SVG icon. The tests check 
 * that the SVG has the correct attributes, and that the "Back" text has 
 * the appropriate styling.
 */
describe('Backlint Component', () => {
    it('renders the SVG icon correctly', () => {
        // Destructure the result of render to access the container
        const { container } = render(<BackLink />);

        // Check that the "Back" text is rendered
        expect(screen.getByText('Back')).toBeInTheDocument();

        // Check that the <svg> element is rendered
        const svgIcon = container.querySelector('svg'); // Use container.querySelector to find the <svg> element
        expect(svgIcon).toBeInTheDocument();
    });

    it('renders the SVG icon with correct attributes', () => {
        // Destructure the result of render to access the container
        const { container } = render(<BackLink />);

        const svgIcon = container.querySelector('svg'); // Find the <svg> element

        // Check that the SVG has the correct attributes
        expect(svgIcon).toHaveAttribute('xmlns', 'http://www.w3.org/2000/svg');
        expect(svgIcon).toHaveAttribute('viewBox', '0 0 20 20');
    });

    it('renders the "Back" text with correct styling', () => {
        render(<BackLink />);

        const backText = screen.getByText('Back');

        // Check that the text is rendered with the expected classes
        expect(backText).toHaveClass('underline', 'font-bold', 'text-sm', '-ml-1');
    });
}
);