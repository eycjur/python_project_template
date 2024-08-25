const API_BASE_URL = "http://localhost:8100"; // LOCAL_PORTに合わせて変更。

async function register() {
    const text = document.getElementById("registerText").value;

    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: text }),
        });

        if (response.ok) {
            const data = await response.json();
            alert(`Register successful: ${data.text}`);
        } else {
            const errorData = await response.json();
            alert(`Register failed: ${errorData.detail || 'Unknown error'}`);
        }
    } catch (error) {
        console.error("Error during registration:", error);
    }
}

async function getHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/history`);

        if (response.ok) {
            const data = await response.json();
            const historyResult = document.getElementById("historyResult");
            historyResult.textContent = JSON.stringify(data.messages, null, 2);
        } else {
            alert("Failed to fetch history.");
        }
    } catch (error) {
        console.error("Error fetching history:", error);
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
