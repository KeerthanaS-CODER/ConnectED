let currentMember = 1;
const totalMembers = 7;

// Display milestone popup initially
window.onload = function() {
    const popup = document.getElementById('milestonePopup');
    
    // Remove popup after 3 seconds
    setTimeout(() => {
        popup.classList.add('hidden');
    }, 3000);
};

// Handle member click event to show respective form
document.querySelectorAll('.member').forEach(member => {
    member.addEventListener('click', function() {
        const selectedMember = this.getAttribute('data-member');
        currentMember = selectedMember;

        // Update form title for the selected member
        document.getElementById('formTitle').innerText = `Member Feedback - Member ${selectedMember}`;

        // Show the feedback form and hide the member selection container
        document.getElementById('feedbackFormContainer').classList.remove('hidden');
        document.getElementById('memberContainer').classList.add('hidden');
    });
});

// Handle feedback form submission
document.getElementById('feedbackForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    
    alert(`Feedback for Member ${currentMember} submitted!`);

    // Clear the form for next feedback
    this.reset();

    // Show the "Get Certificate" button after feedback is submitted
    document.getElementById('getCertificateBtn').classList.remove('hidden');
});

// Handle the "Get Certificate" button click
document.getElementById('getCertificateBtn').addEventListener('click', function() {
    const link = document.createElement('a');
    link.href = 'ConnectD.png';  // Path to your certificate image
    link.download = `completion_certificate.png`;  // File name for the download
    link.click();
});
