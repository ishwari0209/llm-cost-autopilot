import { useEffect, useState, useCallback } from "react";

export function useApi(fetcher, deps = [], { pollMs } = {}) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(
    async (silent = false) => {
      if (!silent) setLoading(true);
      setError(null);
      try {
        const result = await fetcher();
        setData(result);
      } catch (err) {
        setError(err.message || "Something went wrong.");
      } finally {
        if (!silent) setLoading(false);
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    deps
  );

  useEffect(() => {
    load();
    if (pollMs) {
      const id = setInterval(() => load(true), pollMs);
      return () => clearInterval(id);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [load, pollMs]);

  return { data, error, loading, refetch: load };
}
