import { Dialog } from "@headlessui/react";
import { useEffect, useState } from "react";

export default function Candidate(props) {
  let [isOpen, setIsOpen] = useState(false);
  let [userData, setUserData] = useState(null);

  useEffect(() => {
    const fetchCandidateData = async () => {
      const response = await fetch(
        `http://127.0.0.1:4000/api/user_info/${props.idCandidate}`,
      );

      if (!response.ok) {
        console.error("No se pudo obtener los datos del candidato");
        return;
      }
      const data = await response.json();
      setUserData(data);
      console.log(data);
    };

    fetchCandidateData();
  }, [props.idCandidate]);

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
              Information
            </Dialog.Title>

            {userData && (
              <div>
                <h2 className="mt-3 font-semibold">Name</h2>
                <p>{userData.personal_info.name}</p>

                <h2 className="mt-3 font-semibold">Email</h2>
                <p>{userData.personal_info.email}</p>

                <h2 className="mt-3 font-semibold">URLs</h2>
                {userData.personal_info.urls.map((url, idx) => (
                  <a
                    key={idx}
                    href={url}
                    className="block text-blue-400 underline"
                  >
                    {url}
                  </a>
                ))}

                <h2 className="mt-3 font-semibold">Red Flags</h2>
                {userData.red_flags.map((red_flag, idx) => (
                  <a key={idx} href={red_flag}>
                    {red_flag}
                  </a>
                ))}

                <h2 className="mt-3 font-semibold">Soft Skills</h2>
                <p>
                  {userData.soft_skills
                    .map((soft_skill) => soft_skill)
                    .join(", ")}
                </p>

                <h2 className="mt-3 font-semibold">Hard Skills</h2>
                <p>
                  {userData.technical_skills
                    .map((technical_skill) => technical_skill)
                    .join(", ")}
                </p>
              </div>
            )}

            <div className="mt-3 flex justify-end gap-2">
              <button
                className="rounded-md bg-black px-4 py-2 text-sm text-white"
                onClick={() => setIsOpen(false)}
              >
                Accept
              </button>
            </div>
          </Dialog.Panel>
        </div>
      </Dialog>

      <div className="my-4 flex w-full items-center justify-between rounded border border-black p-4">
        <a
          href={`http://127.0.0.1:4000${props.cvRoute.slice(1)}`}
          target="_blank"
          rel="noreferrer"
        >
          {props.name}
        </a>
        <button onClick={() => setIsOpen(true)}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="h-6 w-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z"
            />
          </svg>
        </button>
      </div>
    </>
  );
}
