const ctaBtn = document.querySelector('.cta-btn');
const container = document.querySelector('.container');
const loginPage = document.querySelector('#login');
const description = document.querySelector('.description');
const gameBeginsText = document.querySelector('.game-begins');

// When "Next" button is clicked, hide the main page and show the login page
ctaBtn.addEventListener('click', function(e) {
    e.preventDefault();
    container.style.display = 'none';
    loginPage.style.display = 'flex';

    // Change the description/quote for the second page
    description.textContent = "Unlock your potential in a gamified world, connected with mentors who turn learning into an epic quest.";

    // Fade out the "Game begins..." text after 2 seconds
    setTimeout(function() {
        gameBeginsText.classList.add('fade-out');
    }, 2000); // 2 seconds delay
});
