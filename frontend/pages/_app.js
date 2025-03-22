import "@/styles/globals.css";

import {
  QueryClientProvider,
} from '@tanstack/react-query'

import queryClient from "@/utils/queryClient";

import GlobalStateProvider from "@/components/state_providers/GlobalState"

export default function App({ Component, pageProps }) {
  return <GlobalStateProvider>
    <QueryClientProvider client={queryClient}>
      <Component {...pageProps} />;
    </QueryClientProvider>
  </GlobalStateProvider>

}
