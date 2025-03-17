import "@/styles/globals.css";

import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from '@tanstack/react-query'

import queryClient from "@/utils/queryClient";

export default function App({ Component, pageProps }) {
  return <QueryClientProvider client={queryClient}>
    <Component {...pageProps} />;
  </QueryClientProvider>

}
