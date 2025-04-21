/** 
 * Continue_btn component renders a button with the label "continue".
 * 
 * This button is styled with Tailwind CSS classes and is intended to be used 
 * as a submit button, typically for forms or actions that move the user to 
 * the next step in the application.
 * 
 * @returns {JSX.Element} A JSX element representing the "continue" button with specific styling.
 */
export default function Continue_btn(){
    return (
        <button className="rounded-md bg-btn_green mt-5 w-1/5 text-white text-2xl h-1/2 hover:bg-dark_green" type="submit">
          continue
        </button>
    )
  }