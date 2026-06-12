import { useState } from "react";

import FormInput from "../components/FormInput";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";
import parseCommaSeparated from "../utils/parseCommaSeparated";

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
        skills: parseCommaSeparated(formData.skills),
        experience_years: parseInt(formData.experience_years) || 0,
        preferred_locations: parseCommaSeparated(formData.preferred_locations),
        expected_salary: parseFloat(formData.expected_salary) || null,
        preferred_roles: parseCommaSeparated(formData.preferred_roles),
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
          <FormInput
            label="Full Name"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
          />

          <FormInput
            label="Phone"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
          />

          <FormInput
            label="Education"
            name="education"
            value={formData.education}
            onChange={handleChange}
            placeholder="e.g., B.Tech Computer Science"
          />

          <FormInput
            label="Skills (comma separated)"
            name="skills"
            value={formData.skills}
            onChange={handleChange}
            placeholder="e.g., Python, React, SQL"
          />

          <FormInput
            label="Years of Experience"
            name="experience_years"
            type="number"
            value={formData.experience_years}
            onChange={handleChange}
          />

          <FormInput
            label="Preferred Locations (comma separated)"
            name="preferred_locations"
            value={formData.preferred_locations}
            onChange={handleChange}
            placeholder="e.g., Remote, NYC, SF"
          />

          <FormInput
            label="Expected Salary"
            name="expected_salary"
            type="number"
            value={formData.expected_salary}
            onChange={handleChange}
            placeholder="e.g., 120000"
          />

          <FormInput
            label="Preferred Job Roles (comma separated)"
            name="preferred_roles"
            value={formData.preferred_roles}
            onChange={handleChange}
            placeholder="e.g., Backend Developer, Full Stack Engineer"
          />
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
