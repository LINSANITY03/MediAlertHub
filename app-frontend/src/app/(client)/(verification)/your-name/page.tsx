'use client';

import BackLink from "@/components/BackButton";
import Continue_btn from "@/components/ContinueButton";
import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from 'react-toastify';
import { useLazyQuery } from "@apollo/client";
import { CHECK_USERNAME } from "@/services/user_query";

/**
 * VerifyName Component
 * 
 * This component is used to verify a user's first and last name. It performs a lazy GraphQL query
 * to check the validity of the entered name and stores the response in localStorage if successful.
 * 
 * Upon successful verification, the user is redirected to the "date-of-birth" page.
 * 
 * Side effect:
 * - Sets the document title to "Enter your name" when the component mounts.
 *
 * Features:
 * - Input field for First, and Last name
 * - Apollo Client (useLazyQuery)
 * - React Toastify (toast)
 * - Next.js routing (useRouter)
 * 
 * @returns {JSX.Element} The rendered verify page with form and navigation elements.
 */
export default function VerifyName() {

  /**
   * Sets the browser tab title when the component mounts.
   */
  useEffect(()=>{
    document.title = "Enter your name";
  },[])
  
  const router = useRouter();
  const [first_name, set_fname] = useState("");
  const [last_name, set_lname] = useState("");
  const [FetchData] = useLazyQuery(CHECK_USERNAME, {
    onCompleted: (data) => {
      if (data.verifyUsername.success === true) {
        toast.success(data.verifyUsername.message);
        localStorage.setItem("all-cache", JSON.stringify(data.verifyUsername.body));
        router.push('/date-of-birth');
      } else {
        toast.error(data.verifyUsername?.message || "Something went wrong.");
      }
    },
    onError: (error) => {
      toast.error(error.message)
    }
  });

  /**
   * Handles form submission for verifying a user's name.
   *
   * Prevents the default form behavior, validates input fields, and sends a GraphQL query
   * to verify the username using the Apollo Client.
   *
   * @param {FormEvent<HTMLFormElement>} event - The form submission event.
   * @returns {void}
   */
  async function onSubmit(event: FormEvent<HTMLFormElement>): Promise<void>{

    event.preventDefault();
    if (!first_name.trim()) return;
    if (!last_name.trim()) return;

    FetchData({ variables: { f_name: `${first_name}`, l_name: `${last_name}` }, context: { needsAuth: true} });
  }

  return (
    <div className="p-10 ml-20">
      <Link href={"/your-id"}>
        <BackLink />
      </Link>
      <form action="POST" onSubmit={onSubmit}>
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
              value={first_name}
              onChange={(e) => set_fname(e.target.value)}
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
              value={last_name}
              onChange={(e) => set_lname(e.target.value)}
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
