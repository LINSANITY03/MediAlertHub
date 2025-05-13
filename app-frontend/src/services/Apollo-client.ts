import { ApolloClient, InMemoryCache, HttpLink, from } from "@apollo/client";
import { setContext } from '@apollo/client/link/context';

// fastapi graphql endpoint
const httpLink = new HttpLink({
    uri: "http://0.0.0.0:8000/graphql",
});

// function to add localstorage item to headers
const verifLink = setContext((_, { headers, needsAuth }) => {

    // Only proceed if we're on the client-side
    if (typeof window === 'undefined' || !needsAuth) {
        return { headers };
    }

    const token = localStorage.getItem("all-cache");

    return {
        headers: {
            ...headers,
            ...(token ? {"Authorization": `${token}`} : {}),
        },
    };
}); 

// create an instance of apolloclient
const client = new ApolloClient({
    link: from([verifLink, httpLink]), // verifLink runs first before httplink (similar to decorators)
    cache: new InMemoryCache(),
});

export default client;