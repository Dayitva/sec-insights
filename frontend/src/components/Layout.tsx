import React from "react";
import { Analytics } from "@vercel/analytics/react";
import type { PropsWithChildren } from "react";
const Layout = ({ children }: PropsWithChildren) => {
  return <>{children}<Analytics /></>;
};
export default Layout;
