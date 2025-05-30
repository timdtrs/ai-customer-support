function initChatbot(botId) {
  const container = document.getElementById("chatbot-container");

  const input = document.createElement("input");
  const chat = document.createElement("div");

  input.placeholder = "Ask something...";
  input.addEventListener("keydown", async (e) => {
    if (e.key === "Enter") {
      const userInput = input.value;
      input.value = "";

      chat.innerHTML += `<div>User: ${userInput}</div>`;

      const res = await fetch(`http:localhost:8000/generate/embed-chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput }),
      });

      const data = await res.json();
      chat.innerHTML += `<div>Bot: ${data.response}</div>`;
    }
  });

  container.appendChild(chat);
  container.appendChild(input);
}