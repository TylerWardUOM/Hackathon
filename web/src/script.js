const BASE_URL = "http://10.209.195.140:5000";  // Change to Pi's IP if calling externally
const REFRESH_INTERVAL = 5000; // Refresh every 5 seconds

async function getAttendance() {

    const tableBody = document.querySelector("#attendance-table tbody");
    tableBody.innerHTML = "<tr><td colspan='2'>Loading...</td></tr>";

    try {
        const response = await fetch(`${BASE_URL}/attendance`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({"lectureName": "Advanced Robotics"})
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Response from /attendance:", data);

        // Convert response into an object with student names as keys
        const attendanceObj = {};
        data.attended.forEach(student => {
            // Create an object for each student using their name as the key
            attendanceObj[student.name] = {
                attendance_status: student.attendance_status,
                attendance_percentage: student.attendance_percentage,
                course: student.course,
                year: student.year,
                Verified: student.Verified
            };
        });

        console.log("Formatted Attendance Object:", attendanceObj);
        updateAttendanceTable(attendanceObj);
    } catch (error) {
        console.error("Error fetching attendance:", error);
        tableBody.innerHTML = "<tr><td colspan='2'>Error loading attendance.</td></tr>";
    }
}


function updateAttendanceTable(attendanceObj) {
    const tableBody = document.querySelector("#attendance-table tbody");

    // Clear previous content
    tableBody.innerHTML = "";

    for (const [name, data] of Object.entries(attendanceObj)) {
        const row = document.createElement("tr");

        const nameCell = document.createElement("td");
        nameCell.textContent = name;
        nameCell.style.cursor = 'pointer';
        nameCell.onclick = () => showModal(name, data);

        const statusCell = document.createElement("td");
        statusCell.innerHTML = data.attendance_status ? "✅ Present" : "❌ Not Present";

        const verifiedCell = document.createElement("td");
        verifiedCell.textContent = data.Verified ? "✅ Verified" : "❌ Not Verified";

        row.appendChild(nameCell);
        row.appendChild(statusCell);
        row.appendChild(verifiedCell);
        tableBody.appendChild(row);
    }
}

function showModal(name, data) {

    document.getElementById("modal-title").textContent = `${name}'s Details`;
    document.getElementById("modal-attendance-percentage").textContent = data.attendance_percentage + "%";
    document.getElementById("modal-course").textContent = data.course;
    document.getElementById("modal-year").textContent = data.year;
    //document.getElementById("modal-verified").textContent = data.Verified ? "✅ Verified" : "❌ Not Verified";

    document.getElementById("modal").style.display = "block";

}

document.getElementById("close-modal").onclick = () => {
    document.getElementById("modal").style.display = "none";
    };

window.onclick = (event) => {
    if (event.target === document.getElementById("modal")) {
        document.getElementById("modal").style.display = "none";
    }
};

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
