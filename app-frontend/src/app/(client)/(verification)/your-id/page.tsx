'use client';

import Link from "next/link";
import BackLink from "@/components/BackButton";
import Continue_btn from "@/components/ContinueButton";

import { FormEvent } from "react";
import { useRouter } from 'next/navigation';

export default function Verify() {
  const router = useRouter()
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    router.push('/your-name')
  }

  return (
    <div className="p-10 ml-20 mt-40">
      <Link href={"/"}>
        <BackLink />
      </Link>
      <div className="grid grid-rows-4 mt-5">
        <h2 className="underline tracking-tight text-2xl font-semibold">
          Verify your details
        </h2>
        <form action="POST" onSubmit={onSubmit}>
          <div>
            <label htmlFor="work_id">
              <div className="leading-5 tracking-tight">
                <p className="text-1xl font-semibold">Work ID</p>
                <p className="font-extralight text-sm">
                  This will be your work id
                </p>
              </div>
            </label>
            <input
              className="border border-black focus:to-blue-500 w-1/4 size-12 p-5"
              type="text"
              name="work_id"
              id="work_id"
              maxLength={20}
              required
            />
          </div>
          <Continue_btn />
        </form>
      </div>
    </div>
  );
}
