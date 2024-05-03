function getCount() {
  fetch("/count")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById(
        "objectCount"
      ).textContent = `Number of Objects: ${data.objectCount}`;
    })
    .catch((error) => {
      console.error("Error fetching object count:", error);
    });
}
