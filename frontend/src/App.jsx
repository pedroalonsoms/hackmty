import { BrowserRouter, Routes, Route } from "react-router-dom";
import { CompanyProvider } from "./components/CompanyContext";

import RegisterCompanyPage from "./pages/RegisterCompanyPage";
import UploadCVPage from "./pages/UploadCVPage";
import UploadedCVPage from "./pages/UploadedCVPage";
import JobPostingsPage from "./pages/JobPostingsPage";
import SearchCandidatesPage from "./pages/SearchCandidatesPage";

export default function App() {
  return (
    <CompanyProvider>
      <BrowserRouter>
        <Routes>
          <Route index element={<RegisterCompanyPage />} />
          <Route path="/upload-cv" element={<UploadCVPage />} />
          <Route path="/upload-cv/success" element={<UploadedCVPage />} />
          <Route path="/job-postings" element={<JobPostingsPage />} />
          <Route
            path="/job-postings/:id_company_position/search"
            element={<SearchCandidatesPage />}
          />
        </Routes>
      </BrowserRouter>
    </CompanyProvider>
  );
}
