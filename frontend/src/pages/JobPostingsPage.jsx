import Navbar from "../components/Navbar";
import JobPost from "../components/JobPost";
import { Dialog } from "@headlessui/react";
import { useCallback, useEffect, useState } from "react";
import { useCompany } from "../components/CompanyContext";

export default function JobPostingsPage() {
  const { idCompany } = useCompany();
  let [isOpen, setIsOpen] = useState(false);
  let [jobPostings, setJobPostings] = useState([]);

  const [formData, setFormData] = useState({
    id_company: idCompany,
    position_name: "",
    position_description: "",
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleDeleteJobPosting = async (id_company_position) => {
    const response = await fetch(
      `http://localhost:4000/api/jobs/${id_company_position}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      },
    );

    if (response.status === 200) {
      console.log("Registro borrado con éxito");
      handleGetJobPostings();
    } else {
      console.error("Error al enviar datos");
    }
  };

  const handleCreateNewPosting = async (event) => {
    event.preventDefault();
    console.log("handleCreateNewPosting");
    console.log({ idCompany });

    // Enviar los datos al servidor
    try {
      const response = await fetch(
        `http://localhost:4000/api/jobs/companies/${idCompany}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        },
      );
      console.log(formData);
      console.log(response);

      if (response.status === 200) {
        console.log("Registro creado con éxito");
        setIsOpen(false); // Cerrar el diálogo después del envío exitoso
        handleGetJobPostings();
      } else {
        console.error("Error al enviar datos");
      }
      // setIsOpen(false);
    } catch (error) {
      console.error("Error al enviar datos:", error);
    }
  };

  const handleGetJobPostings = useCallback(async () => {
    console.log("handleGetJobPostings");
    const response = await fetch(
      `http://localhost:4000/api/jobs/companies/${idCompany}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      },
    );
    const data = await response.json();
    console.log(data);
    setJobPostings(data);
  }, [idCompany]);

  useEffect(() => {
    handleGetJobPostings();
  }, [handleGetJobPostings]);

  return (
    <>
      <Dialog open={isOpen} onClose={() => setIsOpen(false)}>
        {/* The backdrop, rendered as a fixed sibling to the panel container */}
        <div className="fixed inset-0 bg-black/30" aria-hidden="true" />

        {/* Full-screen container to center the panel */}
        <div className="fixed inset-0 grid place-items-center">
          {/* The actual dialog panel  */}
          <Dialog.Panel className="w-full max-w-md rounded-md bg-white p-6">
            <Dialog.Title className="text-lg font-semibold">
              New Job Posting
            </Dialog.Title>

            <form onSubmit={handleCreateNewPosting}>
              <div>
                <label htmlFor="position_name" className="block pt-3">
                  Title
                </label>
                <input
                  type="text"
                  id="position_name"
                  name="position_name"
                  value={formData.position_name}
                  onChange={handleChange}
                  className="w-full rounded-md border border-slate-400 p-2"
                ></input>
              </div>

              <div>
                <label htmlFor="position_description" className="block pt-2">
                  Description
                </label>
                <input
                  type="text"
                  id="position_description"
                  name="position_description"
                  value={formData.position_description}
                  onChange={handleChange}
                  className="w-full rounded-md border border-slate-400 p-2"
                ></input>
              </div>

              <div className="mt-3 flex justify-end gap-2">
                <button
                  className="rounded-md border border-slate-400 bg-white px-4 py-2 text-black"
                  onClick={() => setIsOpen(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-md bg-black px-4 py-2 text-white"
                  // onClick={() => setIsOpen(false)}
                >
                  Continue
                </button>
              </div>
            </form>
          </Dialog.Panel>
        </div>
      </Dialog>

      <Navbar />
      <div className="mx-auto flex max-w-2xl items-center justify-between">
        <h2 className="py-20 text-center text-6xl font-bold">Job Postings</h2>
        <button
          className="rounded-md bg-black px-16 py-2 text-lg text-white"
          onClick={() => setIsOpen(true)}
        >
          New Posting
        </button>
      </div>
      <div className="mx-auto max-w-2xl">
        {jobPostings.map((jobPosting, idx) => (
          <JobPost
            key={idx}
            href={`/job-postings/${jobPosting.id_company_position}/search`}
            title={jobPosting.position_name}
            onDeleteClick={() => {
              handleDeleteJobPosting(jobPosting.id_company_position);
            }}
          />
        ))}
      </div>
    </>
  );
}
