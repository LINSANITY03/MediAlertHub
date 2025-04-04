'use client';

import BackLink from "@/components/BackButton";
import Continue_btn from "@/components/ContinueButton";
import Link from "next/link";
import { FormEvent, useEffect } from "react";
import { useRouter } from "next/navigation";
import { toast } from 'react-toastify';

export default function VerifyName() {

  useEffect(()=>{
    document.title = "Enter your name";
  },[])
  
  const router = useRouter()
  async function onSubmit(event: FormEvent<HTMLFormElement>){
    event.preventDefault()
    router.push('/date-of-birth')
  }

  return (
    <div className="p-10 ml-20">
      <Link href={"/your-id"}>
        <BackLink />
      </Link>
      <form action="" onSubmit={onSubmit}>
        <div className="grid grid-rows-4 mt-5">
          <h2 className="underline tracking-tight text-2xl font-semibold">
            Enter your name
          </h2>
          <div>
            <label htmlFor="first_name">
              <div className="leading-5 tracking-tight">
                <p className="text-1xl font-semibold">First Name</p>
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
              <div className="mt-3 leading-5 tracking-tight">
                <p className="text-1xl font-semibold">Last Name</p>
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
      </form>
    </div>
  );
}
