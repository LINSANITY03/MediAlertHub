"use client";

import Link from "next/link";
import BackLink from "@/components/BackButton";
import Continue_btn from "@/components/ContinueButton";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { useLazyQuery } from "@apollo/client";
import { CHECK_ID } from "@/services/user_query";
import { toast } from 'react-toastify';

/**
 * Verify component allows users to input and validate their Work ID.
 * 
 * On successful verification via GraphQL query, the user is redirected to a new page
 * and relevant data is stored in localStorage. It also handles error messaging using toast notifications.
 *
 * Features:
 * - Input field for Work ID
 * - Form submission with validation
 * - Lazy query using Apollo Client
 * - Navigation via Next.js router
 * - Success and error toasts for feedback
 *
 * @returns {JSX.Element} The rendered verify page with form and navigation elements.
 */
export default function Verify() {
  const router = useRouter();
  const [userId, setUserId] = useState("");
  const [FetchData] = useLazyQuery(CHECK_ID, {
    onCompleted: (data) => {
      if (data.verifyDoctorId.success == true) {
        toast.success(data.verifyDoctorId.message)
        localStorage.setItem("all-cache", JSON.stringify(data.verifyDoctorId.body))
        router.push("/your-name");
      } else {
        toast.error(data.verifyDoctorId.message)
        }
    },
    onError: (error) => {
      toast.error(error.message)
    }
  });
  
  /**
   * Handles the form submission for verifying a doctor's Work ID.
   *
   * Prevents the default form action, validates the user input, and triggers a lazy GraphQL query
   * to check the doctor's ID using Apollo Client.
   *
   * @param {FormEvent<HTMLFormElement>} event - The form submit event.
   * @returns {void}
   */
  async function handleSubmit(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();

    if (!userId.trim()) return;
    FetchData({ variables: { doctorid: `${userId}` } });
  };

  return (
    <div className="p-10 ml-20 mt-40">
      <Link href={"/"}>
        <BackLink />
      </Link>
      <div className="grid grid-rows-4 mt-5">
        <h2 className="underline tracking-tight text-2xl font-semibold">
          Verify your details
        </h2>
        <form action="POST" onSubmit={handleSubmit}>
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
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              maxLength={50}
              required
            />
          </div>
          <Continue_btn />
        </form>
      </div>
    </div>
  );
}
