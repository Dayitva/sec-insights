import { type AppType } from "next/dist/shared/lib/utils";
import Layout from "~/components/Layout";
import { AuthContextProvider } from "~/stores/authContext";
import "~/styles/globals.css";
import ReactGA from "react-ga4";

import { IntercomProvider } from "react-use-intercom";
import { GOOGLE_ANALYTICS_ID, INTERCOM_ID } from "~/constants";

ReactGA.initialize(GOOGLE_ANALYTICS_ID);

const MyApp: AppType = ({ Component, pageProps }) => {
  return (
    <>
    <AuthContextProvider>
      <IntercomProvider appId={INTERCOM_ID}>
        <Layout>
          <Component {...pageProps} />
        </Layout>
      </IntercomProvider>
    </AuthContextProvider>
    </>
  );
};

export default MyApp;
