document.getElementById('uploadForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent the default form submission

    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('http://127.0.0.1:5003/upload', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            document.getElementById('message').textContent = result.message;
        } else {
            document.getElementById('message').textContent = 'Error: ' + response.statusText;
        }

    } catch (error) {
        console.error('Error:', error); // Log any errors
        document.getElementById('message').textContent = 'Error uploading file: ' + error.message;
    }
});

// Display the "YOU WON!" message and hide it slowly
document.addEventListener('DOMContentLoaded', function () {
    const message = document.getElementById('message');
    message.style.display = 'block';
    setTimeout(() => {
        message.style.opacity = '0';
        setTimeout(() => {
            message.style.display = 'none';
        }, 1000); // Delay for opacity transition
    }, 3000);
});