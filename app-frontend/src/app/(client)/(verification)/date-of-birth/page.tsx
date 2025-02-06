import Link from "next/link";
import BackLink from "@/components/BackButton";
import Continue_btn from "@/components/ContinueButton";
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'What is your DOB?',
}

export default function Verify() {
  return (
    <div className="p-10 ml-20">
      <Link href={"/your-name"}>
        <BackLink />
      </Link>
      <div className="grid grid-rows-3 mt-5">
        <h2 className="underline tracking-tight text-2xl font-semibold">
          What is your DOB?
        </h2>

        <div>
          <label htmlFor="dob">
            <div className="mt-7 leading-5 tracking-tight">
              <p className="text-1xl font-semibold">Date of birth</p>
            </div>
          </label>
          <input
            className="border border-black focus:to-blue-500 w-1/4 size-12 p-5"
            type="date"
            name="dob"
            id="dob"
            maxLength={20}
            required
          />
        </div>
        <Continue_btn />
      </div>
    </div>
  );
}
