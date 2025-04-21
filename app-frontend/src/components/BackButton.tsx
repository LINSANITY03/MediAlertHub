/** 
 * BackLink component renders an inline link with an SVG icon and the text "Back".
 * 
 * This component is designed to be used as a back navigation link, typically
 * in the UI of a web application.
 * 
 * @returns {JSX.Element} A JSX element containing an SVG icon and the text "Back".
 */
export default function BackLink(){
    return (
        <div className="inline-flex items-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            className="size-5"
          >
            <path
              fillRule="evenodd"
              d="M11.78 5.22a.75.75 0 0 1 0 1.06L8.06 10l3.72 3.72a.75.75 0 1 1-1.06 1.06l-4.25-4.25a.75.75 0 0 1 0-1.06l4.25-4.25a.75.75 0 0 1 1.06 0Z"
              clipRule="evenodd"
            />
          </svg>

          <p className="underline font-bold text-sm -ml-1">Back</p>
        </div>
    )
}