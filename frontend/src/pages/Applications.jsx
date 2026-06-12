import LoadingSpinner from "../components/LoadingSpinner";
import useApiData from "../hooks/useApiData";

function Applications() {
  const { data: applications, loading } = useApiData("/applications/");

  const statusColors = {
    pending: "bg-yellow-100 text-yellow-800",
    applied: "bg-blue-100 text-blue-800",
    interview: "bg-purple-100 text-purple-800",
    rejected: "bg-red-100 text-red-800",
    offer: "bg-green-100 text-green-800",
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-900">
        My Applications
      </h1>

      {!applications || applications.length === 0 ? (
        <div className="rounded-lg bg-white py-12 text-center shadow">
          <p className="text-gray-500">No applications yet.</p>
          <a
            href="/jobs"
            className="mt-2 inline-block text-blue-600 hover:text-blue-500"
          >
            Search for jobs to get started
          </a>
        </div>
      ) : (
        <div className="overflow-hidden rounded-lg bg-white shadow">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                  Job
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                  Match Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                  Applied
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
              {applications.map((app) => (
                <tr key={app.id}>
                  <td className="whitespace-nowrap px-6 py-4">
                    <div className="text-sm font-medium text-gray-900">
                      Job #{app.job_id}
                    </div>
                  </td>
                  <td className="whitespace-nowrap px-6 py-4">
                    <div className="text-sm text-gray-900">
                      {app.match_score
                        ? `${(app.match_score * 100).toFixed(0)}%`
                        : "N/A"}
                    </div>
                  </td>
                  <td className="whitespace-nowrap px-6 py-4">
                    <span
                      className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${statusColors[app.status] || "bg-gray-100 text-gray-800"}`}
                    >
                      {app.status}
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
                    {app.applied_at
                      ? new Date(app.applied_at).toLocaleDateString()
                      : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Applications;
