'use client';

import Link from "next/link";
import BackLink from "@/components/BackButton";
import Continue_btn from "@/components/ContinueButton";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from 'next/navigation';
import { useLazyQuery } from "@apollo/client";
import { CHECK_DOB } from "@/services/user_query";
import { toast } from 'react-toastify';

/**
 * The Verify component is responsible for verifying the user's date of birth (DOB).
 * It prompts the user to enter their DOB and sends it to the backend for validation.
 * 
 * @returns {JSX.Element} The form UI.
 */
export default function Verify() {
  const router = useRouter();
  const [dob, setdob] = useState("");

  /**
   * Lazy-loaded query to verify the user's date of birth.
   * If the verification is successful, the user is redirected to the form details page.
   * 
   * @param {object} data - The response data from the server after attempting to verify the DOB.
   */
  const [FetchData] = useLazyQuery(CHECK_DOB,{
    onCompleted: (data) => {
      if (data.verifyDob.success == true) {
        toast.success(data.verifyDob.message)
        localStorage.setItem("all-cache", JSON.stringify(data.verifyDob.body))
        router.push("/form-details");
      } else {
        toast.error(data.verifyDob.message)
        }
    },
    onError: (error) => {
      toast.error(error.message)
    }
  })

  useEffect(() => {
    document.title = "What is your DOB?";
  }, []);

  /**
   * Handles the form submission when the user enters their DOB.
   * Prevents the default form behavior and triggers the verification request.
   * 
   * @param {FormEvent<HTMLFormElement>} event - The form submission event.
   * @returns {Promise<void>} Resolves when the form submission handling is complete.
   */
  async function onSubmit(event: FormEvent<HTMLFormElement>){
    event.preventDefault()
    FetchData({ variables: { dob: `${dob}` }, context: { needsAuth: true} });
  }
  return (
    <div className="p-10 ml-20">
      <Link href={"/your-name"}>
        <BackLink />
      </Link>
      <div className="grid grid-rows-3 mt-5">
        <h2 className="underline tracking-tight text-2xl font-semibold">
          What is your DOB?
        </h2>
        <form action="POST" onSubmit={onSubmit}>
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
              value={dob}
              onChange={(e) => {setdob(e.target.value)}}
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
