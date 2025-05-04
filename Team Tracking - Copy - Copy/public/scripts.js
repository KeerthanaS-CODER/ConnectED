document.addEventListener('DOMContentLoaded', () => {
    // Function to fetch team data
    async function fetchTeamData(teamName) {
        try {
            const response = await fetch(`/team/${teamName}`);
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            displayTeamData(data);
        } catch (error) {
            console.error('Error fetching team data:', error);
        }
    }

    // Function to determine intensity class based on hours
    function getIntensityClass(hours) {
        if (hours < 5) return 'intensity-low';
        if (hours < 7) return 'intensity-medium';
        return 'intensity-high';
    }

    // Function to display team data
    function displayTeamData(data) {
        const teamInfoSection = document.getElementById('team-info');
        const teamDataDiv = document.getElementById('team-data');
        
        // Populate the team info
        teamDataDiv.innerHTML = `
            <div class="team-card">
                <h3>Team Name: ${data.teamName}</h3>
                <h4>Mentor: ${data.mentor.name}</h4>
                <p>Milestones: ${data.milestones.map(ms => `Milestone ${ms.milestone}: ${ms.completed ? 'Completed' : 'Incomplete'}`).join(', ')}</p>
                <p>Work Hours: ${data.workHours.map(wh => `Date: ${wh.date}, Hours: ${wh.hours}`).join(', ')}</p>
                <h4>Students:</h4>
                <ul>
                    ${data.students.map(student => `<li class="${getIntensityClass(student.progress.hours)}">${student.name} - Milestone ${student.progress.milestone}, Hours: ${student.progress.hours}</li>`).join('')}
                </ul>
            </div>
        `;

        // Show the team info section
        teamInfoSection.style.display = 'block';
    }

    // Add event listeners for team links
    document.getElementById('dexters-link').addEventListener('click', (e) => {
        e.preventDefault();
        fetchTeamData('DEXTERS');
    });

    document.getElementById('fixcode-link').addEventListener('click', (e) => {
        e.preventDefault();
        fetchTeamData('FixCode');
    });
});
