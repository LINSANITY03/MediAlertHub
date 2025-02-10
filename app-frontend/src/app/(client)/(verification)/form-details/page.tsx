"use client";

import BackLink from "@/components/BackButton";
import Continue_btn from "@/components/ContinueButton";
import React, { useState } from "react";

import dynamic from "next/dynamic";
import Link from "next/link";

// Dynamically load the Map component and disable SSR
const MapSelector = dynamic(() => import("@/components/MapSelect"), {
  ssr: false, // Disable SSR for this component
});

interface Position {
  lat: number;
  lng: number;
}

export default function FormView() {
  const myDefaultPosition: Position = { lat: 27.658354, lng: 85.325065 }; // Satdobato
  const [selectedPosition, setSelectedPosition] = useState<Position | null>(
    null
  );

  const handlePositionSelect = (position: Position) => {
    setSelectedPosition(position);
    console.log("Selected Position:", position);
  };

  return (
    <div className="p-20 ml-20">
      <Link href={"/"}>
        <BackLink />
      </Link>
      <h1 className="text-3xl tracking-tight font-bold pt-6">Preview</h1>

      <form className="pt-10">
        {/* form1 */}
        <div className="tracking-tight">
          <h2 className="text-2xl font-semibold underline">Identity details</h2>
          <label htmlFor="patient_age">
            <p className="text-xl">1. Patient age</p>
          </label>
          <input
            className="border border-black mx-3 p-3"
            type="number"
            name="patient_age"
            id="patient_age"
            max={120}
            min={1}
            defaultValue={1}
            required
          />
          <p className="text-xl">2. Does the patient accompanied by anyone?</p>
          <textarea
            className="border border-black mx-3 p-3"
            name=""
            id=""
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
          <p className="text-xl">
            1. Does the patient have any disease currently?
          </p>
          <textarea
            className="border border-black mx-3 p-3"
            name=""
            id=""
            cols={50}
            rows={5}
            required
          />
          <p className="text-xl">2. Describe the patient current condition?</p>
          <textarea
            className="border border-black mx-3 p-3"
            name=""
            id=""
            cols={50}
            rows={5}
            required
          />
          <p className="text-xl">3. Does the patient has any visible symptoms?</p>
          <textarea
            className="border border-black mx-3 p-3"
            name=""
            id=""
            cols={50}
            rows={5}
            required
          />
          <p className="text-xl">4. Any other documents related to patient?</p>
          <textarea
            className="border border-black mx-3 p-3"
            name=""
            id=""
            cols={50}
            rows={5}
            required
          />
        </div>

        {/* form3 */}
        <div className="pt-10">
          <h2 className="text-2xl font-semibold underline">Location</h2>
          <p className="text-xl">1. District</p>
          <input type="checkbox" name="" id="" required/>
          <p className="text-xl">2. Zone</p>
          <input className="border border-black" type="text" name="" id="" readOnly required/>
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
