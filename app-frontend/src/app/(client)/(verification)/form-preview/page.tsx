"use client";

import BackLink from "@/components/BackButton";
import Continue_btn from "@/components/ContinueButton";
import dynamic from "next/dynamic";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";
import { toast } from "react-toastify";

/**
 * Represents a geographical position with latitude and longitude.
 */
interface Position {
  lat: number;
  lng: number;
}

/**
 * Represents a collection of filenames related to patient documents.
 */
interface Files {
  filename: string[]
}

/**
 * Represents the structure of the form data.
 */
interface formDataType {
  ageIdentity: string;
  accompIdent: string;
  statusDisease: string;
  statusCondition: string;
  statusSymptom: string;
  files: Files | null;
  province: string;
  district: string;
  position: Position | null
}

/**
 * Dynamically load the Map component and disable SSR
 */
const MapPreviwer = dynamic(() => import("@/components/MapPreview"), {
    ssr: false, // Disable SSR for this component
});

/**
 * FormPreview component renders a preview of patient form data fetched
 * based on a session ID from the URL search parameters.
 * 
 * It displays identity details, status examination, documents, and location,
 * including a map preview if location coordinates are available.
 * 
 * It also handles form submission with a confirmation alert and redirects
 * the user to the home page.
 * 
 * @component
 * @returns {JSX.Element} The form preview UI.
 */
export default function FormPreview() {
  const searchParams = useSearchParams();
  const session = searchParams.get("session");
  const router = useRouter();
  const [formData, setFormData] = useState<formDataType>({
    ageIdentity: "",
    accompIdent: "",
    statusDisease: "",
    statusCondition: "",
    statusSymptom: "",
    files: null,
    province: "",
    district: "",
    position: null
  });

  /**
   * Fetch form data from the API using the given session ID.
   * Updates the state with the fetched data or shows an error toast on failure.
   * 
   * @param {string} session - The session ID used to fetch data.
   */
  async function fetchData(session: string ){
    const token = localStorage.getItem("all-cache");
    try {
      const res = await fetch(`http://localhost:8001/${session}`, {
        method: "GET",
          headers: {
            "Authorization": `${token}`
          },
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.message || 'Request failed');
      }
      const data = await res.json();
      if (data.success === false){
        toast.error(data.detail)
      }else{
        setFormData(prev => ({
          ...prev,
          ...data.body
        }));
      }
    } catch (error: unknown) {
      if (error instanceof Error) {
        toast.error(`Error: ${error.message}`);
      } else {
        toast.error('An unknown error occurred.');
      }
    }};
  
  /**
   * Set document title and fetch form data when the session param changes.
   */
  useEffect(() => {
    document.title = "Preview";
    if (!session) return;
    
    fetchData(session);
    
  }, [session]);

  /**
   * Handle form submission by preventing default behavior,
   * redirecting to the homepage, and showing an alert message.
   * 
   * @param {FormEvent<HTMLFormElement>} event - The form submit event.
   */
  async function onSubmit(event: FormEvent<HTMLFormElement>){
    event.preventDefault();
    const token = localStorage.getItem("all-cache");
    try {
      const res = await fetch(`http://localhost:8001/${session}`, {
        method: "POST",
          headers: {
            "Authorization": `${token}`
          },
          body: JSON.stringify(formData)
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.message || 'Request failed');
      }
      const data = await res.json();
      if (data.success === true){
        localStorage.setItem('successMessage', data.detail);
        router.push('/');
      }else{
        toast.error(data.detail);
      }
    } catch (error: unknown) {
      if (error instanceof Error) {
        toast.error(`Error: ${error.message}`);
      } else {
        toast.error('An unknown error occurred.');
      }
    };
  }

  return (
    <div className="p-20 ml-20">
      <Link href={"/"}>
        <BackLink />
      </Link>

      <form className="pt-10" action="POST" onSubmit={onSubmit}>
        {/* form1 */}
        <div className="tracking-tight">
          <h2 className="text-2xl font-semibold underline">Identity details</h2>
          <label htmlFor="f_1_q_1">
            <p className="text-xl">1. Patient age</p>
          </label>
          <p className="ml-5" id="f_1_q_1">
            {formData.ageIdentity}
          </p>
          <label htmlFor="">
            <p className="text-xl">
              2. Does the patient accompanied by anyone?
            </p>
          </label>
          <p className="ml-5" id="f_1_q_2">
            {formData.accompIdent}
          </p>
        </div>

        {/* form2 */}
        <div className="pt-10 tracking-tight">
          <h2 className="text-2xl font-semibold underline">
            Status examination
          </h2>
          <label htmlFor="f_2_q_1">
            <p className="text-xl">
              1. Does the patient have any disease currently?
            </p>
          </label>
          <p className="ml-5" id="f_2_q_1">
            {formData.statusDisease}
          </p>

          <label className="text-xl" htmlFor="f_2_q_2">
            <p>2. Describe the patient current condition?</p>
          </label>
          <p className="ml-5" id="f_2_q_2">
            {formData.statusCondition}
          </p>

          <label htmlFor="f_2_q_3">
            <p className="text-xl">
              3. Does the patient has any visible symptoms?
            </p>
          </label>

          <p className="ml-5" id="f_2_q_3">
            {formData.statusSymptom}
          </p>

          <label htmlFor="f_2_q_4">
            <p className="text-xl">
              4. Any other documents related to patient?
            </p>
          </label>

          <div className="bg-primary_green w-full m-5 p-10">
            {formData.files?.filename && formData.files.filename.length > 0 ? (
            formData.files.filename.map((each, index) => (
              <p className="text-2xl font-medium text-center" key={index}>{each}</p>
            ))
          ): (
            <p className="text-2xl font-medium text-center">No document</p>
          )
          }
          </div>
        </div>

        {/* form3 */}
        <div className="pt-10">
          <h2 className="text-2xl font-semibold underline">Location</h2>
          <label htmlFor="f_3_q_1">
            <p className="text-xl">1. Province</p>
          </label>
          <p className="ml-5" id="f_3_q_1">
            {formData.province}
          </p>

          <label htmlFor="f_3_q_2">
            <p className="text-xl">2. District</p>
          </label>
          <p className="ml-5" id="f_3_q_2">
            {formData.district}
          </p>
          {formData.position && <MapPreviwer lat={27.658354} lng={85.325065} />}
        
        </div>

        <Continue_btn />
      </form>
    </div>
  );
}