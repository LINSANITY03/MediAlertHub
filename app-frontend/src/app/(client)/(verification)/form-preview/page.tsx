"use client";

import BackLink from "@/components/BackButton";
import Continue_btn from "@/components/ContinueButton";
import dynamic from "next/dynamic";
import Link from "next/link";
import { useEffect } from "react";

// Dynamically load the Map component and disable SSR
const MapPreviwer = dynamic(() => import("@/components/MapPreview"), {
    ssr: false, // Disable SSR for this component
});

export default function FormPreview() {
  useEffect(() => {
    document.title = "Preview";
  }, []);

  return (
    <div className="p-20 ml-20">
      <Link href={"/"}>
        <BackLink />
      </Link>

      <form className="pt-10">
        {/* form1 */}
        <div className="tracking-tight">
          <h2 className="text-2xl font-semibold underline">Identity details</h2>
          <label htmlFor="f_1_q_1">
            <p className="text-xl">1. Patient age</p>
          </label>
          <p className="ml-5" id="f_1_q_1">
            27
          </p>
          <label htmlFor="">
            <p className="text-xl">
              2. Does the patient accompanied by anyone?
            </p>
          </label>
          <p className="ml-5" id="f_1_q_2">
            At vero eos et accusamus et iusto odio dignissimos ducimus qui
            blanditiis praesentium voluptatum deleniti atque corrupti quos
            dolores et quas molestias excepturi sint occaecati cupiditate non
            provident, similique sunt in culpa qui officia deserunt mollitia
            animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis
            est et expedita distinctio. Nam libero tempore, cum soluta nobis est
            eligendi optio cumque nihil impedit quo minus id quod maxime placeat
            facere possimus, omnis voluptas assumenda est, omnis dolor
            repellendus. Temporibus autem quibusdam et aut officiis debitis aut
            rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint
            et molestiae non recusandae. Itaque earum rerum hic tenetur a
            sapiente delectus, ut aut reiciendis voluptatibus maiores alias
            consequatur aut perferendis doloribus asperiores repellat.
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
            At vero eos et accusamus et iusto odio dignissimos ducimus qui
            blanditiis praesentium voluptatum deleniti atque corrupti quos
            dolores et quas molestias excepturi sint occaecati cupiditate non
            provident, similique sunt in culpa qui officia deserunt mollitia
            animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis
            est et expedita distinctio. Nam libero tempore, cum soluta nobis est
            eligendi optio cumque nihil impedit quo minus id quod maxime placeat
            facere possimus, omnis voluptas assumenda est, omnis dolor
            repellendus. Temporibus autem quibusdam et aut officiis debitis aut
            rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint
            et molestiae non recusandae. Itaque earum rerum hic tenetur a
            sapiente delectus, ut aut reiciendis voluptatibus maiores alias
            consequatur aut perferendis doloribus asperiores repellat.
          </p>

          <label className="text-xl" htmlFor="f_2_q_2">
            <p>2. Describe the patient current condition?</p>
          </label>
          <p className="ml-5" id="f_2_q_2">
            At vero eos et accusamus et iusto odio dignissimos ducimus qui
            blanditiis praesentium voluptatum deleniti atque corrupti quos
            dolores et quas molestias excepturi sint occaecati cupiditate non
            provident, similique sunt in culpa qui officia deserunt mollitia
            animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis
            est et expedita distinctio. Nam libero tempore, cum soluta nobis est
            eligendi optio cumque nihil impedit quo minus id quod maxime placeat
            facere possimus, omnis voluptas assumenda est, omnis dolor
            repellendus. Temporibus autem quibusdam et aut officiis debitis aut
            rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint
            et molestiae non recusandae. Itaque earum rerum hic tenetur a
            sapiente delectus, ut aut reiciendis voluptatibus maiores alias
            consequatur aut perferendis doloribus asperiores repellat.
          </p>

          <label htmlFor="f_2_q_3">
            <p className="text-xl">
              3. Does the patient has any visible symptoms?
            </p>
          </label>

          <p className="ml-5" id="f_2_q_3">
            At vero eos et accusamus et iusto odio dignissimos ducimus qui
            blanditiis praesentium voluptatum deleniti atque corrupti quos
            dolores et quas molestias excepturi sint occaecati cupiditate non
            provident, similique sunt in culpa qui officia deserunt mollitia
            animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis
            est et expedita distinctio. Nam libero tempore, cum soluta nobis est
            eligendi optio cumque nihil impedit quo minus id quod maxime placeat
            facere possimus, omnis voluptas assumenda est, omnis dolor
            repellendus. Temporibus autem quibusdam et aut officiis debitis aut
            rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint
            et molestiae non recusandae. Itaque earum rerum hic tenetur a
            sapiente delectus, ut aut reiciendis voluptatibus maiores alias
            consequatur aut perferendis doloribus asperiores repellat.
          </p>

          <label htmlFor="f_2_q_4">
            <p className="text-xl">
              4. Any other documents related to patient?
            </p>
          </label>

          <div className="bg-primary_green w-full m-5 p-10">
            <p className="text-2xl font-medium text-center">No Document</p>
          </div>
        </div>

        {/* form3 */}
        <div className="pt-10">
          <h2 className="text-2xl font-semibold underline">Location</h2>
          <label htmlFor="f_3_q_1">
            <p className="text-xl">1. Province</p>
          </label>
          <p className="ml-5" id="f_3_q_1">
            Bagmati
          </p>

          <label htmlFor="f_3_q_2">
            <p className="text-xl">2. District</p>
          </label>
          <p className="ml-5" id="f_3_q_2">
            Lalitpur
          </p>
        <MapPreviwer lat={27.658354} lng={85.325065} />
        </div>

        <Continue_btn />
      </form>
    </div>
  );
}
