import Navbar from "../components/Navbar";
import { useState } from "react";
import { useCompany } from "../components/CompanyContext";
import { useNavigate } from "react-router-dom";

export default function RegisterCompanyPage() {
  const { setIdCompany } = useCompany();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Enviar los datos al servidor
    try {
      const response = await fetch("http://localhost:4000/api/companies", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });
      console.log(formData);
      console.log(response);

      if (response.ok) {
        const responseData = await response.json();
        console.log("Respuesta del servidor:", responseData);
        console.log("Registro creado con éxito");
        const responseDataString = responseData[0][0].toString();
        setIdCompany(responseDataString);
        navigate("/job-postings");
      } else {
        console.error(
          "Error al enviar datos. Código de estado:",
          response.status,
        );
      }
    } catch (error) {
      console.error("Error al enviar datos:", error);
    }
  };
  return (
    <>
      <Navbar />
      <h1 className="pt-20 text-center text-6xl font-bold">Register Company</h1>
      <div className="pt-20"></div>
      <form
        onSubmit={handleSubmit}
        action="#"
        className="mx-auto max-w-md rounded-md border border-slate-400 p-4"
      >
        <p className="text-slate-400">Welcome</p>

        <div className="pt-2">
          <label className="block pt-2" htmlFor="companyName">
            Company Name
          </label>
          <input
            className="w-full rounded-md border border-slate-400 p-2"
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
          ></input>
        </div>

        <div>
          <label htmlFor="email" className="block pt-2">
            Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            className="w-full rounded-md border border-slate-400 p-2"
            value={formData.email}
            onChange={handleChange}
          ></input>
        </div>

        <div>
          <label htmlFor="password" className="block pt-2">
            Password
          </label>
          <input
            type="password"
            id="password"
            name="password"
            className="w-full rounded-md border border-slate-400 p-2"
            value={formData.password}
            onChange={handleChange}
          ></input>
        </div>

        <button
          type="submit"
          className="mx-auto mt-4 block rounded-md bg-black px-16 py-2 text-lg text-white"
        >
          Log In
        </button>
      </form>
    </>
  );
}
