const BASE_URL = "http://10.209.195.140:5000";  // Change to Pi's IP if calling externally
const REFRESH_INTERVAL = 5000; // Refresh every 5 seconds

async function getAttendance() {

    const tableBody = document.querySelector("#attendance-table tbody");
    tableBody.innerHTML = "<tr><td colspan='2'>Loading...</td></tr>";

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

        // Convert response into an object with student names as keys
        const attendanceObj = {};
        data.attended.forEach(student => {
            attendanceObj[student.name] = student.attended;
        });

        console.log("Formatted Attendance Object:", attendanceObj);
        updateAttendanceTable(attendanceObj);
    } catch (error) {
        console.error("Error fetching attendance:", error);
        //document.getElementById("attendance-list").innerHTML = "<p>Error loading attendance.</p>";

        //const tableBody = document.querySelector("#attendance-table tbody");
        tableBody.innerHTML = "<tr><td colspan = '2'>Loading...</td></tr>";
    }
}

function updateAttendanceTable(attendanceObj) {
    const tableBody = document.querySelector("#attendance-table tbody");

    // Clear previous content
    tableBody.innerHTML = "";

    for (const [name, attended] of Object.entries(attendanceObj)) {
        const row = document.createElement("tr");

        const nameCell = document.createElement("td");
        nameCell.textContent = name;

        const statusCell = document.createElement("td");
        statusCell.innerHTML = attended ? "✅ Present" : "❌ Not Verified";

        row.appendChild(nameCell);
        row.appendChild(statusCell);
        tableBody.appendChild(row);
    }
}

    // Create an unordered list


    /* const ul = document.createElement("ul");

    // Loop through attendanceObj and create list items
    for (const [name, attended] of Object.entries(attendanceObj)) {
        const li = document.createElement("li");
        li.textContent = `${name}: ${attended ? "✅ Present" : "❌ Not Verified"}`;
        ul.appendChild(li);
    }

    // Append list to div
    attendanceDiv.appendChild(ul); */


// Call getAttendance on page load
window.onload = () => {
    getAttendance(); // Initial call
    setInterval(getAttendance, REFRESH_INTERVAL); // Auto-refresh every 5 seconds
};
