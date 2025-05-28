"use client";

import React, { useState, useEffect, FormEvent } from "react";

import BackLink from "@/components/BackButton";
import Continue_btn from "@/components/ContinueButton";
import district from "@/components/District_list";
import province from "@/components/Province_list";

import dynamic from "next/dynamic";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Image from "next/image"; 
import { toast } from "react-toastify";

// Dynamically load the Map component and disable SSR
const MapSelector = dynamic(() => import("@/components/MapSelect"), {
  ssr: false, // Disable SSR for this component
});

/**
 * Represents a geographical position with latitude and longitude.
 */
interface Position {
  lat: number;
  lng: number;
}

/**
 * Represents the structure of the form data.
 */
interface formDataType {
  ageIdentity: number;
  accompIdent: string;
  statusDisease: string;
  statusCondition: string;
  statusSymptom: string;
  files: FileList | null;
  province: string;
  district: string;
}

/**
 * Main form view component for submitting patient details.
 * Handles input changes, file uploads, location selection, and form submission.
 *
 * @returns {JSX.Element} The form UI.
 */
export default function FormView() {
  
  const myDefaultPosition: Position = { lat: 27.658354, lng: 85.325065 }; // Satdobato
  const [selectedPosition, setSelectedPosition] = useState<Position | null>(
    null
  );
  const router = useRouter();
  
  const [formData, setFormData] = useState<formDataType>({
    ageIdentity: 1,
    accompIdent: "",
    statusDisease: "",
    statusCondition: "",
    statusSymptom: "",
    files: null,
    province: "",
    district: ""
  });

  /**
   * Handles text, select, and textarea input changes.
   *
   * @param {React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>} e
   */
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  };

  /**
   * Handles file input changes.
   *
   * @param {React.ChangeEvent<HTMLInputElement>} e
   */
  const handleFilesChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    const maxFiles = 3;

    if (files && files.length > maxFiles) {
      toast.warning(`You can only upload up to ${maxFiles} files.`);
      e.target.value = ""; // Clear the selection
      return;
    }
    setFormData((prev) => ({
      ...prev,
      files: e.target.files
    }));
  };
  
  /**
   * Updates the selected map position.
   *
   * @param {Position} position
   */
  const handlePositionSelect = (position: Position) => {
    setSelectedPosition(position);
  };

  /**
   * Filter states based on the selected country
   */
  const filteredDistrict = district.filter(
    (state) => state.province === formData.province
  );
  
  /**
   * Sets the document title when the component mounts.
   */
  useEffect(() => {
    document.title = "Complete the form";
  }, []);
  
  /**
   * Handles form submission: builds form data, sends request, handles response.
   *
   * @param {FormEvent<HTMLFormElement>} event
   */
  async function onSubmit(event: FormEvent<HTMLFormElement>){
    event.preventDefault();

    const fd = new FormData();
    fd.append("age_identity", formData.ageIdentity.toString());
    fd.append("accomp_ident", formData.accompIdent);
    fd.append("status_disease", formData.statusDisease);
    fd.append("status_condition", formData.statusCondition);
    fd.append("status_symptom", formData.statusSymptom);
    fd.append("province", formData.province);
    fd.append("district", formData.district);
    fd.append("position", selectedPosition ? JSON.stringify(selectedPosition) : "null");

    if (formData.files) {
      Array.from(formData.files).forEach((file) => {
        fd.append("files", file);
      });
    }
    const token = localStorage.getItem("all-cache");
    try {
      const res = await fetch("http://localhost:8001", {
        method: "POST",
        headers: {
          "Authorization": `${token}`
        },
        body: fd, // FormData or JSON.stringify(data)
      });
      
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.message || 'Request failed');
      }
      const data = await res.json();
      if (data.success === true){
        router.push(`/form-preview?session=${data.form_id}`);
      } else {
        toast.error(data.detail)
      }

    } catch (error: unknown) {
      if (error instanceof Error) {
        toast.error(`Error: ${error.message}`);
      } else {
        toast.error('An unknown error occurred.');
      }
    }
  }
  
  return (
    <div className="p-20 ml-20">
      <Link href={"/date-of-birth"}>
        <BackLink />
      </Link>

      <form className="pt-10" action="POST" onSubmit={onSubmit}>
        {/* form1 */}
        <div className="tracking-tight">
          <h2 className="text-2xl font-semibold underline">Identity details</h2>
          <label htmlFor="f_1_q_1">
            <p className="text-xl">1. Patient age</p>
          </label>
          <select name="ageIdentity" id="f_1_q_1" className="border border-black mx-3 p-3"
          value={formData.ageIdentity} onChange={handleInputChange}>
            <option value={1}>1-5</option>
            <option value={2}>6-12</option>
            <option value={3}>13-18</option>
            <option value={4}>19-25</option>
            <option value={5}>26-35</option>
            <option value={6}>36-45</option>
            <option value={7}>46-60</option>
            <option value={8}>61-72</option>
            <option value={9}>73-89</option>
            <option value={10}>90-100</option>
            <option value={11}>100+</option>
          </select>
          <label htmlFor="">
            <p className="text-xl">
              2. Does the patient accompanied by anyone?
            </p>
          </label>

          <textarea
            className="border border-black mx-3 p-3"
            name="accompIdent"
            id="f_1_q_2"
            value={formData.accompIdent}
            onChange={handleInputChange}
            cols={50}
            rows={5}
            required
          />
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

          <textarea
            className="border border-black mx-3 p-3"
            name="statusDisease"
            id="f_2_q_1"
            value={formData.statusDisease}
            onChange={handleInputChange}
            cols={50}
            rows={5}
            required
          />
          <label className="text-xl" htmlFor="f_2_q_2">
            <p>2. Describe the patient current condition?</p>
          </label>
          <textarea
            className="border border-black mx-3 p-3"
            name="statusCondition"
            id="f_2_q_2"
            value={formData.statusCondition}
            onChange={handleInputChange}
            cols={50}
            rows={5}
            required
          />
          <label htmlFor="f_2_q_3">
            <p className="text-xl">
              3. Does the patient has any visible symptoms?
            </p>
          </label>

          <textarea
            className="border border-black mx-3 p-3"
            name="statusSymptom"
            id="f_2_q_3"
            value={formData.statusSymptom}
            onChange={handleInputChange}
            cols={50}
            rows={5}
            required
          />
          <label htmlFor="f_2_q_4">
            <p className="text-xl">
              4. Any other documents related to patient?
            </p>
          </label>

          <div className="flex flex-col items-center justify-center bg-green-200 w-full p-6 rounded-2xl border-2 border-dashed text-center shadow-md mt-5">
            <input name="patient-documents" id="f_2_q_4" type="file" multiple accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.svg" 
            className="hidden" onChange={handleFilesChange}/>
            <label htmlFor="f_2_q_4">
            <Image
              src="/Upload.svg"
              width={85}
              height={79}
              alt="Upload files"
              className=""
            />
          </label>
          <span>Upload Max 3 Files pdf,doc,docx,jpg,jpeg,png,svg</span>

          {/* Show uploaded file list */}
          {formData.files && (
            <ul className="mt-4 w-full text-left text-sm">
              {Array.from(formData.files).map((file, index) => (
                <li key={index} className="mb-1">
                  📄 {file.name} — {(file.size / (1024 * 1024)).toFixed(2)} MB
                </li>
              ))}
            </ul>
          )}
          </div>
        </div>

        {/* form3 */}
        <div className="pt-10">
          <h2 className="text-2xl font-semibold underline">Location</h2>
          <label htmlFor="f_3_q_1">
            <p className="text-xl">1. Province</p>
          </label>

          <select
            className="border border-black mx-3 p-3"
            name="province"
            value={formData.province}
            id="f_3_q_1"
            onChange={handleInputChange}
            required
          >
            <option value="">Select a Province</option> {/* Optional default option */}
            {province.map((each, index) => {
              return (
                <option
                  key={index}
                  value={each.name}
                >
                  {each.name}
                </option>
              );
            })}
          </select>

          {formData.province && (
            <>
              <label htmlFor="f_3_q_2">
                <p className="text-xl">2. District</p>
              </label>
              <select
                className="border border-black mx-3 p-3"
                name="district"
                value={formData.district}
                onChange={handleInputChange}
                id="f_3_q_2"
                required
              >
                {filteredDistrict.map((each, index) => {
                  return (
                    <option key={index} value={each.name}>
                      {each.name}
                    </option>
                  );
                })}
              </select>
            </>
          )}
          <MapSelector
            onPositionSelect={handlePositionSelect}
            defaultPosition={myDefaultPosition}
          />
        </div>
        <Continue_btn />
      </form>
    </div>
  );
}
