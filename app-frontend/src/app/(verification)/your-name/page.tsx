import BackLink from "@/components/BackButton";
import Continue_btn from "@/components/ContinueButton";
import Link from "next/link";

export default function VerifyName() {
  return (
    <div className="p-10 ml-20">
        <Link href={"/your-id"}>
      <BackLink />
        </Link>
      <div className="grid grid-rows-4 mt-10">
        <h2 className="underline tracking-tight text-3xl font-semibold">
          Enter your name
        </h2>
        <div>
          <label htmlFor="first_name">
            <div className="mt-7 leading-5 tracking-tight">
              <p className="text-3xl font-semibold">First Name</p>
            </div>
          </label>
          <input
            className="border border-black focus:to-blue-500 w-1/4 size-12 p-5"
            type="text"
            name="first_name"
            id="first_name"
            maxLength={20}
            required
          />
        </div>
        <div>
          <label htmlFor="last_name">
            <div className="mt-7 leading-5 tracking-tight">
              <p className="text-3xl font-semibold">Last Name</p>
            </div>
          </label>
          <input
            className="border border-black focus:to-blue-500 w-1/4 size-12 p-5"
            type="text"
            name="last_name"
            id="last_name"
            maxLength={20}
            required
          />
        </div>
        <Continue_btn />
      </div>
    </div>
  );
}
