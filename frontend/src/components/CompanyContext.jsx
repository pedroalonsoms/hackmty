// CompanyContext.js
import { createContext, useState, useContext } from "react";

const CompanyContext = createContext();

export function CompanyProvider({ children }) {
  const [idCompany, setIdCompany] = useState("");

  return (
    <CompanyContext.Provider value={{ idCompany, setIdCompany }}>
      {children}
    </CompanyContext.Provider>
  );
}

export function useCompany() {
  return useContext(CompanyContext);
}
