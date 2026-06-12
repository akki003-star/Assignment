import { useState } from "react";

import { useAuth } from "../context/AuthContext";
import api from "../services/api";

function Profile() {
  const { user, setUser } = useAuth();
  const [formData, setFormData] = useState({
    full_name: user?.full_name || "",
    phone: user?.phone || "",
    education: user?.education || "",
    skills: user?.skills?.join(", ") || "",
    experience_years: user?.experience_years || 0,
    preferred_locations: user?.preferred_locations?.join(", ") || "",
    expected_salary: user?.expected_salary || "",
    preferred_roles: user?.preferred_roles?.join(", ") || "",
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage("");
    try {
      const payload = {
        full_name: formData.full_name,
        phone: formData.phone,
        education: formData.education,
        skills: formData.skills
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean),
        experience_years: parseInt(formData.experience_years) || 0,
        preferred_locations: formData.preferred_locations
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean),
        expected_salary: parseFloat(formData.expected_salary) || null,
        preferred_roles: formData.preferred_roles
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean),
      };
      const response = await api.put("/auth/me", payload);
      setUser(response.data);
      setMessage("Profile updated successfully!");
    } catch (err) {
      setMessage("Failed to update profile");
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-900">Profile</h1>

      <form
        onSubmit={handleSubmit}
        className="mx-auto max-w-2xl rounded-lg bg-white p-6 shadow"
      >
        {message && (
          <div
            className={`mb-4 rounded-md p-3 text-sm ${message.includes("success") ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"}`}
          >
            {message}
          </div>
        )}

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Full Name
            </label>
            <input
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Phone
            </label>
            <input
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Education
            </label>
            <input
              name="education"
              value={formData.education}
              onChange={handleChange}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
              placeholder="e.g., B.Tech Computer Science"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Skills (comma separated)
            </label>
            <input
              name="skills"
              value={formData.skills}
              onChange={handleChange}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
              placeholder="e.g., Python, React, SQL"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Years of Experience
            </label>
            <input
              name="experience_years"
              type="number"
              value={formData.experience_years}
              onChange={handleChange}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Preferred Locations (comma separated)
            </label>
            <input
              name="preferred_locations"
              value={formData.preferred_locations}
              onChange={handleChange}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
              placeholder="e.g., Remote, NYC, SF"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Expected Salary
            </label>
            <input
              name="expected_salary"
              type="number"
              value={formData.expected_salary}
              onChange={handleChange}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
              placeholder="e.g., 120000"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Preferred Job Roles (comma separated)
            </label>
            <input
              name="preferred_roles"
              value={formData.preferred_roles}
              onChange={handleChange}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
              placeholder="e.g., Backend Developer, Full Stack Engineer"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={saving}
          className="mt-6 w-full rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {saving ? "Saving..." : "Save Profile"}
        </button>
      </form>
    </div>
  );
}

export default Profile;
