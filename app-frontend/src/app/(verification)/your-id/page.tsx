import Link from "next/link";

export default function Verify() {
  return (
    <div className="p-10 ml-20">
      <Link href={"/"}>
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
      </Link>
      <div className="grid grid-rows-4 mt-14">
        <h2 className="underline tracking-tight text-3xl font-semibold">
          Verify your details
        </h2>

        <div>
          <label htmlFor="work_id">
            <div className="mt-7 leading-5 tracking-tight">
              <p className="text-3xl font-semibold">Work ID</p>
              <p className="font-extralight text-sm">
                This will be your work id
              </p>
            </div>
          </label>
          <input
            className="border border-black focus:to-blue-500 w-1/4 size-12"
            type="text"
            name="work_id"
            id="work_id"
            required
          />
        </div>
        <button className="rounded-md bg-btn_green mt-5 w-1/5 text-white text-2xl h-1/2" type="submit">
          continue
        </button>
      </div>
    </div>
  );
}
