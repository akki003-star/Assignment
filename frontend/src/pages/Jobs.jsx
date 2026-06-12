import { useState } from "react";

import api from "../services/api";

function Jobs() {
  const [keywords, setKeywords] = useState("");
  const [location, setLocation] = useState("");
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await api.post("/jobs/search", {
        keywords: keywords
          .split(",")
          .map((k) => k.trim())
          .filter(Boolean),
        location: location || null,
      });
      setJobs(response.data);
    } catch (err) {
      console.error("Search failed:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleApply = async (jobId) => {
    try {
      await api.post("/applications/apply", { job_id: jobId });
      alert("Application submitted successfully!");
    } catch (err) {
      alert(err.response?.data?.detail || "Application failed");
    }
  };

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-900">Job Search</h1>

      <form
        onSubmit={handleSearch}
        className="mb-8 rounded-lg bg-white p-6 shadow"
      >
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <input
            type="text"
            placeholder="Keywords (comma separated)"
            className="rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
          />
          <input
            type="text"
            placeholder="Location"
            className="rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
          <button
            type="submit"
            disabled={loading}
            className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </div>
      </form>

      <div className="space-y-4">
        {jobs.length === 0 && !loading && (
          <p className="py-8 text-center text-gray-500">
            Search for jobs to get started
          </p>
        )}
        {jobs.map((job) => (
          <div key={job.id} className="rounded-lg bg-white p-6 shadow">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {job.title}
                </h3>
                <p className="text-sm text-gray-600">{job.company}</p>
                <p className="mt-1 text-sm text-gray-500">{job.location}</p>
                {job.salary_min && job.salary_max && (
                  <p className="mt-1 text-sm text-green-600">
                    ${job.salary_min.toLocaleString()} - $
                    {job.salary_max.toLocaleString()}
                  </p>
                )}
                {job.requirements?.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-1">
                    {job.requirements.map((req) => (
                      <span
                        key={req}
                        className="rounded-full bg-blue-100 px-2 py-1 text-xs text-blue-800"
                      >
                        {req}
                      </span>
                    ))}
                  </div>
                )}
              </div>
              <button
                onClick={() => handleApply(job.id)}
                className="rounded-md bg-green-600 px-4 py-2 text-sm text-white hover:bg-green-700"
              >
                Apply
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Jobs;
