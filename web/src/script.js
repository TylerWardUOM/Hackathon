const BASE_URL = "http://10.209.195.140:5000";  // Change to Pi's IP if calling externally

async function getAttendance() {
    try {
        const response = await fetch(`${BASE_URL}/attendance`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Response from /attendance:", data);
    } catch (error) {
        console.error("Error fetching attendance:", error);
    }
}

// Call the function
getAttendance();
