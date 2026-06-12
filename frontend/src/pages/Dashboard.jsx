import { useEffect, useState } from "react";

import api from "../services/api";

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await api.get("/applications/dashboard");
      setStats(response.data);
    } catch (err) {
      console.error("Failed to fetch stats:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const statCards = [
    {
      label: "Total Applications",
      value: stats?.total_applications || 0,
      color: "bg-blue-500",
    },
    { label: "Applied", value: stats?.applied || 0, color: "bg-green-500" },
    { label: "Pending", value: stats?.pending || 0, color: "bg-yellow-500" },
    {
      label: "Interviews",
      value: stats?.interviews || 0,
      color: "bg-purple-500",
    },
    { label: "Offers", value: stats?.offers || 0, color: "bg-emerald-500" },
    {
      label: "Rejections",
      value: stats?.rejections || 0,
      color: "bg-red-500",
    },
  ];

  return (
    <div>
      <h1 className="mb-8 text-2xl font-bold text-gray-900">Dashboard</h1>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {statCards.map((card) => (
          <div
            key={card.label}
            className="overflow-hidden rounded-lg bg-white shadow"
          >
            <div className="p-6">
              <div className="flex items-center">
                <div className={`rounded-md ${card.color} p-3`}>
                  <span className="text-2xl font-bold text-white">
                    {card.value}
                  </span>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">
                    {card.label}
                  </p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-10 rounded-lg bg-white p-6 shadow">
        <h2 className="mb-4 text-lg font-semibold text-gray-900">
          Quick Actions
        </h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <a
            href="/jobs"
            className="rounded-lg border-2 border-dashed border-gray-300 p-6 text-center hover:border-blue-500 hover:bg-blue-50"
          >
            <p className="text-sm font-medium text-gray-900">Search Jobs</p>
            <p className="mt-1 text-xs text-gray-500">
              Find matching opportunities
            </p>
          </a>
          <a
            href="/profile"
            className="rounded-lg border-2 border-dashed border-gray-300 p-6 text-center hover:border-blue-500 hover:bg-blue-50"
          >
            <p className="text-sm font-medium text-gray-900">Update Profile</p>
            <p className="mt-1 text-xs text-gray-500">
              Improve your match score
            </p>
          </a>
          <a
            href="/applications"
            className="rounded-lg border-2 border-dashed border-gray-300 p-6 text-center hover:border-blue-500 hover:bg-blue-50"
          >
            <p className="text-sm font-medium text-gray-900">
              View Applications
            </p>
            <p className="mt-1 text-xs text-gray-500">Track your progress</p>
          </a>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
