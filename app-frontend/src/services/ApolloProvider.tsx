"use client";

import { ApolloProvider } from "@apollo/client";
import client from "./Apollo-client";

/** 
 * ApolloWrapper component wraps its children with ApolloProvider.
 * 
 * @param {React.ReactNode} children - The child components that will be wrapped by ApolloProvider.
 * @returns {JSX.Element} The rendered ApolloProvider component containing the children.
 */
export default function ApolloWrapper({ children }: { children: React.ReactNode}) {
    return <ApolloProvider client={client}>{children}</ApolloProvider>
}