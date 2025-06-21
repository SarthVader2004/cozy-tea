document.getElementById('submitBtn').addEventListener('click', async () => {
  const mood = document.getElementById('moodInput').value.trim();
  const output = document.getElementById('teaOutput');

  // Handle empty input
  if (!mood) {
    output.innerText = "🌸 Please share how you're feeling!";
    return;
  }

  // Show brewing message
  output.innerHTML = "🍵 Brewing your perfect tea...";

  try {
    const res = await fetch("https://cozy-tea.onrender.com/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ mood: mood })
    });

    const data = await res.json();

    if (data.response) {
      // Format nicely with line breaks
      output.innerText = data.response.trim();
    } else {
      output.innerText = "😕 Couldn't get a suggestion. Please try again later.";
    }
  } catch (err) {
    console.error(err);
    output.innerText = "⚠️ Something went wrong. Please check your connection or server.";
  }
});
