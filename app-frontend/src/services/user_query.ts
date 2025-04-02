import { gql } from "@apollo/client";

export const CHECK_ID = gql`
query MyQuery($doctorId: String!) {
    verifyDoctorId(doctorId: $doctorId) {
        message
        success
    }
}
`;