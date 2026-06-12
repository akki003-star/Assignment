import { useState } from "react";
import { Link } from "react-router-dom";

import ErrorAlert from "../components/ErrorAlert";
import FormInput from "../components/FormInput";
import { useAuth } from "../context/AuthContext";

function Register() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { register } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await register(email, password, fullName);
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="w-full max-w-md space-y-8 rounded-lg bg-white p-8 shadow">
        <div>
          <h2 className="text-center text-3xl font-bold text-gray-900">
            Create Account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Start automating your job applications
          </p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <ErrorAlert message={error} />
          <div className="space-y-4">
            <FormInput
              required
              placeholder="Full Name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
            />
            <FormInput
              type="email"
              required
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <FormInput
              type="password"
              required
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button
            type="submit"
            className="w-full rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Create Account
          </button>
          <p className="text-center text-sm text-gray-600">
            Already have an account?{" "}
            <Link to="/" className="text-blue-600 hover:text-blue-500">
              Sign in
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}

export default Register;
