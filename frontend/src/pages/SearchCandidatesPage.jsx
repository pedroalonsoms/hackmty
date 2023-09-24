import { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import Select from "react-select";
import { Dialog } from "@headlessui/react";
import { QRCodeSVG } from "qrcode.react";
import Candidate from "../components/Candidate";

export default function SearchCandidatesPage() {
  let [isOpen, setIsOpen] = useState(false);
  let [skillsType, setSkillsType] = useState("");
  let [skillsOptions, setSkillsOptions] = useState([]);
  let [keywords, setKeywords] = useState([]);
  let [candidates, setCandidates] = useState([]);

  useEffect(() => {
    const fetchAllCandidates = async () => {
      const response = await fetch(`http://localhost:4000/api/users`);
      if (!response.ok) {
        console.error("No se pudo obtener lista de skills");
        return;
      }
      const data = await response.json();
      setCandidates(data);
      console.log(data);
    };

    fetchAllCandidates();
  }, []);

  useEffect(() => {
    const fetchSkills = async () => {
      const response = await fetch(`http://localhost:4000/${skillsType}/`);
      if (!response.ok) {
        console.error("No se pudo obtener lista de skills");
        return;
      }
      const data = await response.json();
      setSkillsOptions(data);
      console.log(data);
    };

    if (skillsType != "") {
      fetchSkills();
    }
  }, [skillsType]);

  const handleSearch = async (e) => {
    e.preventDefault();

    let requestBody;

    if (skillsType == "soft_skills") {
      requestBody = {
        softskills: keywords.map((keyword) => keyword.value),
        hardskills: [],
      };
    } else if (skillsType == "hard_skills") {
      requestBody = {
        softskills: [],
        hardskills: keywords.map((keyword) => keyword.value),
      };
    } else {
      throw new Error("Unknown skills type");
    }

    console.log({ ...requestBody });

    const response = await fetch("http://localhost:4000/api/main_candidates", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ...requestBody }),
    });
    if (!response.ok) {
      console.error("No se pudo obtener lista de skills");
      return;
    }
    const data = await response.json();
    setCandidates(data);
    console.log(data);
  };

  return (
    <>
      <Dialog open={isOpen} onClose={() => setIsOpen(false)}>
        <Dialog open={isOpen} onClose={() => setIsOpen(false)}>
          {/* The backdrop, rendered as a fixed sibling to the panel container */}
          <div className="fixed inset-0 bg-black/30" aria-hidden="true" />

          {/* Full-screen container to center the panel */}
          <div className="fixed inset-0 grid place-items-center ">
            {/* The actual dialog panel  */}
            <Dialog.Panel className="flex w-full max-w-md flex-col items-center rounded-md bg-white p-6">
              <Dialog.Title className="text-lg font-semibold">
                Your QR Code
              </Dialog.Title>
              <QRCodeSVG
                value="http://127.0.0.1:3000/upload-cv"
                className="m-4"
              />
              <button
                className="rounded-md border border-slate-400 bg-white px-4 py-2 text-black"
                onClick={() => setIsOpen(false)}
              >
                Close
              </button>
            </Dialog.Panel>
          </div>
        </Dialog>
        ;
      </Dialog>

      <Navbar />

      <div className="mx-auto flex max-w-2xl items-center justify-between">
        <h2 className="py-20 text-center text-6xl font-bold">
          Search Candidates
        </h2>
        <button
          className="rounded-md bg-black px-4 py-2 text-lg text-white"
          onClick={() => setIsOpen(true)}
        >
          View QR
        </button>
      </div>

      <form className="mx-auto max-w-2xl grow" onSubmit={handleSearch}>
        <div className="flex justify-center gap-2">
          <div>
            <input
              type="radio"
              id="hard_skills"
              value="hard_skills"
              name="skills_type"
              onChange={(e) => {
                if (e.target.checked) {
                  setSkillsType("hard_skills");
                }
              }}
            />
            <label htmlFor="hard_skills" className="pl-2">
              Hard Skills
            </label>
          </div>

          <div>
            <input
              type="radio"
              id="soft_skills"
              value="soft_skills"
              name="skills_type"
              onChange={(e) => {
                if (e.target.checked) {
                  setSkillsType("soft_skills");
                }
              }}
            />
            <label htmlFor="soft_skills" className="pl-2">
              Soft Skills
            </label>
          </div>
        </div>

        <Select
          className="mt-2 grow"
          name="skills"
          isMulti
          value={keywords}
          onChange={(newKeywords) => setKeywords(newKeywords)}
          options={skillsOptions.map((skillsOption) => ({
            value: skillsOption,
            label: skillsOption,
          }))}
        />

        <button
          type="submit"
          className="mx-auto mt-3 block rounded-md bg-black px-10 py-2 text-white"
        >
          Search
        </button>
      </form>

      <div className="mx-auto max-w-2xl">
        {candidates.map((candidate, idx) => (
          <Candidate
            key={idx}
            name={candidate.name}
            idCandidate={candidate.id_candidate}
            cvRoute={candidate.cv_route}
          />
        ))}
      </div>
    </>
  );
}
