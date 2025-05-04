document.addEventListener('DOMContentLoaded', () => {
    const filterBtn = document.getElementById('filterBtn');
    const addVideoForm = document.getElementById('addVideoForm');
    const videoList = document.getElementById('videoList');

    // Function to create sparkles
// Function to create sparkles
// Create a sparkle container
const sparkleContainer = document.createElement('div');
sparkleContainer.classList.add('sparkle-container');
document.body.appendChild(sparkleContainer);

// Function to create sparkles
const createSparkle = () => {
    const sparkle = document.createElement('div');
    sparkle.classList.add('sparkle');
    const size = Math.random() * 8 + 5; // Random size between 5 and 10
    sparkle.style.width = `${size}px`;
    sparkle.style.height = `${size}px`;
    sparkle.style.left = `${Math.random() * window.innerWidth}px`;
    sparkle.style.top = `${Math.random() * window.innerHeight}px`;
    sparkleContainer.appendChild(sparkle);

    // Remove sparkle after animation
    sparkle.addEventListener('animationend', () => {
        sparkle.remove();
    });
};

// Create sparkles at intervals
setInterval(createSparkle, 300);



    // Function to fetch videos based on selected filters
    const fetchVideos = (language = '', domain = '') => {
        let url = '/videos';
        const params = [];

        if (language) {
            params.push(`language=${encodeURIComponent(language)}`);
        }
        if (domain) {
            params.push(`domain=${encodeURIComponent(domain)}`);
        }

        if (params.length > 0) {
            url += `?${params.join('&')}`;
        }

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(videos => {
                videoList.innerHTML = ''; // Clear the current video list
                if (Array.isArray(videos)) {
                    videos.forEach(video => {
                        const videoItem = document.createElement('div');
                        videoItem.classList.add('video-item');
                        videoItem.innerHTML = `
                            <h3>${video.title}</h3>
                            <p>Language: ${video.language}</p>
                            <p>Domain: ${video.domain}</p>
                            <video width="320" height="240" controls>
                                <source src="${video.url}" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                        `;
                        videoList.appendChild(videoItem);
                    });
                } else {
                    console.error('Expected an array of videos but received:', videos);
                }
            })
            .catch(error => {
                console.error('Error fetching videos:', error);
            });
    };

    // Event listener for the filter button
    filterBtn.addEventListener('click', () => {
        const language = document.getElementById('languageSelect').value;
        const domain = document.getElementById('domainSelect').value;
        fetchVideos(language, domain);
    });

    // Event listener for the add video form submission
    addVideoForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent form submission

        // Safely get element values
        const title = document.getElementById('videoTitle') ? document.getElementById('videoTitle').value : null;
        const file = document.getElementById('videoFile') ? document.getElementById('videoFile').files[0] : null;
        const language = document.getElementById('newVideoLanguage') ? document.getElementById('newVideoLanguage').value : null;
        const domain = document.getElementById('newVideoDomain') ? document.getElementById('newVideoDomain').value : null;

        // Log the values for debugging
        console.log('Title:', title);
        console.log('File:', file);
        console.log('Language:', language);
        console.log('Domain:', domain);

        if (!title || !file || !language || !domain) {
            console.error('Error: All fields are required');
            return;
        }

        const formData = new FormData();
        formData.append('title', title);
        formData.append('videoFile', file);
        formData.append('language', language);
        formData.append('domain', domain);

        // Post the new video to the server
        fetch('/videos', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // Clear the form
                addVideoForm.reset();
                // Refresh the video list
                fetchVideos();
            } else {
                console.error('Error adding video:', response.statusText);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Initial fetch of videos on page load
    fetchVideos();
});
