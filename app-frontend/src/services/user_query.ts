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

export const CHECK_USERNAME = gql`
query MyQuery($f_name: String!, $l_name: String!) {
    verifyUsername(fName: $f_name, lName: $l_name) {
        message
        success
        body {
            id
            step
        }
    }
}
`;