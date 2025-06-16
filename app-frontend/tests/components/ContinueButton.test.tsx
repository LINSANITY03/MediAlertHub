import { render, screen } from "@testing-library/react";
import { describe, it } from '@jest/globals';
import Continue_btn from "@/components/ContinueButton";

/**
 * Test suite for the Continue_btn component.
 * 
 * This suite contains tests to ensure that the Continue_btn component
 * renders correctly, has the right text content, and includes the correct
 * attributes such as button type.
 */
describe('Continue Button', ()=> {
    it('renders the text', () => {
        render(<Continue_btn/>)

        const button = screen.getByRole('button', {name: "continue"});
        expect(button).toBeInTheDocument();
    });

    it('is of type submit', ()=> {
        render(<Continue_btn/>)

        const button = screen.getByRole('button', {name: "continue"});
        expect(button).toHaveAttribute('type','submit')
    });
});
