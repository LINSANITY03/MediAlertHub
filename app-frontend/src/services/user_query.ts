import { gql } from "@apollo/client";

export const CHECK_ID = gql`
query MyQuery($doctorid: String!) {
    verifyDoctorId(doctorid: $doctorid) {
        message
        success
        body {
            id
            step
        }
    }
}
`;