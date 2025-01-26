function startLiveStats() {
  const eventSource = new EventSource("/stats/live");

  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      document.getElementById("site-visits").textContent =
        data.site_visits || 0;
      document.getElementById("processed-requests").textContent =
        data.processed_requests || 0;
    } catch (error) {
      console.error("Error parsing live stats:", error);
    }
  };

  eventSource.onerror = () => {
    console.error("Failed to connect to the live stats server.");
    // document.getElementById("site-visits").textContent = "Error";
    // document.getElementById("processed-requests").textContent = "Error";
    eventSource.close();
  };
}

// Start listening for live updates when the page loads
document.addEventListener("DOMContentLoaded", startLiveStats);
