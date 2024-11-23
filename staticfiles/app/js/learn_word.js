var player;
var currentIndex = 0;

function onPlayerReady(event) {
    console.log("Player is ready");
    updateButtonLabel();
}

// Initialize YouTube Player
function onYouTubeIframeAPIReady() {
    // Check if player already exists and destroy if necessary
    if (player && player.destroy) {
        player.destroy();
    }

    player = new YT.Player('player', {
        events: {
            'onReady': onPlayerReady
        }
    });
}

// Ensure the API loads and initializes correctly
function reloadYouTubePlayer() {
    if (typeof YT === 'undefined' || typeof YT.Player === 'undefined') {
        const script = document.createElement('script');
        script.src = "https://www.youtube.com/iframe_api";
        document.body.appendChild(script);
    } else {
        onYouTubeIframeAPIReady();
    }
}

// Call reloadYouTubePlayer on page load
window.onload = reloadYouTubePlayer;

// Function to skip to the current timestamp
function skipToCurrent() {
    if (player && player.seekTo) {
        player.seekTo(timestamps[currentIndex].time, true);
    }
}

// Function to go to the previous timestamp
function previousTimestamp() {
    if (currentIndex > 0) {
        currentIndex--;
        updateButtonLabel();
        skipToCurrent();
    }
}

// Function to go to the next timestamp
function nextTimestamp() {
    if (currentIndex < timestamps.length - 1) {
        currentIndex++;
        updateButtonLabel();
        skipToCurrent();
    }
}

// Update button label with the current word
function updateButtonLabel() {
    const button = document.querySelector('.nav-button:nth-child(2)');
    button.innerText = `Skip to "${timestamps[currentIndex].word}"`;
}

// Set initial button label
document.addEventListener('DOMContentLoaded', updateButtonLabel);