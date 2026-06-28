const API_URL =
  "http://import.meta.env.VITE_API_URL";

const RECOMMENDATION_TIMEOUT_MS = 4000;

export const getRecommendations =
  async (userId) => {

    try {

      const controller = new AbortController();
      const timeoutId = window.setTimeout(() => {
        controller.abort();
      }, RECOMMENDATION_TIMEOUT_MS);

      try {
        const response = await fetch(`${API_URL}/recommend/${userId}`, {
          signal: controller.signal
        });

        if (!response.ok) {
          const text = await response.text().catch(() => null);
          return { error: `Server error ${response.status}: ${text || response.statusText}` };
        }

        const data = await response.json();

        // normalize responses to an object with recommendations or error
        if (Array.isArray(data)) {
          return { recommendations: data };
        }

        return data;
      } catch (err) {
        if (err?.name === "AbortError") {
          return { timeout: true };
        }

        return { error: `Network error: ${err?.message || "unknown"}` };
      } finally {
        window.clearTimeout(timeoutId);
      }

    } catch (error) {

      console.error(
        "Recommendation API Error:",
        error
      );
      return { error: `Unexpected error: ${error?.message || String(error)}` };
    }
};