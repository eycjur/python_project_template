const API_BASE_URL = "http://localhost:8100"; // LOCAL_PORTに合わせて変更。

async function postMessage() {
    const content = document.getElementById("postMessageText").value;

    try {
        const response = await fetch(`${API_BASE_URL}/messages`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ content: content }),
        });

        if (response.ok) {
            const data = await response.json();
            alert(`Post message successful: ${data.text}`);
        } else {
            const errorData = await response.json();
            alert(`Post message failed: ${errorData.detail || 'Unknown error'}`);
        }
    } catch (error) {
        console.error("Error during posting message:", error);
    }
}

async function getMessages() {
    try {
        const response = await fetch(`${API_BASE_URL}/messages`);

        if (response.ok) {
            const data = await response.json();
            const getMessagesResult = document.getElementById("getMessagesResult");
            getMessagesResult.textContent = JSON.stringify(data.messages, null, 2);
        } else {
            alert("Failed to fetch messages.");
        }
    } catch (error) {
        console.error("Error fetching messages:", error);
    }
}

async function getError() {
    try {
        const response = await fetch(`${API_BASE_URL}/error`);

        if (response.ok) {
            const data = await response.json();
            const errorResult = document.getElementById("errorResult");
            errorResult.textContent = JSON.stringify(data, null, 2);
        } else {
            alert("Failed to fetch error.");
        }
    } catch (error) {
        console.error("Error fetching error:", error);
    }
}
