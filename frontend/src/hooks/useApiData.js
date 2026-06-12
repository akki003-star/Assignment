import { useEffect, useState } from "react";

import api from "../services/api";

export default function useApiData(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const response = await api.get(url);
        if (!cancelled) setData(response.data);
      } catch (err) {
        console.error(`Failed to fetch ${url}:`, err);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [url]);

  return { data, loading };
}
