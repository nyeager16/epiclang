document.addEventListener("DOMContentLoaded", () => {
    const videosData = document.getElementById("videos-data").textContent;
    const videos = JSON.parse(videosData);

    let currentIndex = 0;
    const videoFrame = document.getElementById("video-frame");

    // Function to load video at the current index
    const loadVideo = (index) => {
        if (index < 0 || index >= videos.length) return;
        videoFrame.src = `https://www.youtube.com/embed/${videos[index].url}`;
        
        videoFrame.classList.remove("visible");
        videoFrame.classList.add("hidden"); // Start with hidden for transition
        
        setTimeout(() => {
            videoFrame.classList.remove("hidden");
            videoFrame.classList.add("visible");
        }, 100); // Delay to trigger transition
    };

    // Load the first video
    loadVideo(currentIndex);

    // Handle scroll events
    const handleScroll = (event) => {
        const deltaY = event.deltaY;

        if (deltaY > 0 && currentIndex < videos.length - 1) {
            // Scroll down to the next video
            currentIndex++;
            videoFrame.classList.remove("visible");
            videoFrame.classList.add("hidden");
            setTimeout(() => loadVideo(currentIndex), 500); // Wait for the fade-out transition
        } else if (deltaY < 0 && currentIndex > 0) {
            // Scroll up to the previous video
            currentIndex--;
            videoFrame.classList.remove("visible");
            videoFrame.classList.add("hidden");
            setTimeout(() => loadVideo(currentIndex), 500); // Wait for the fade-out transition
        }
    };

    // Add scroll listener
    window.addEventListener("wheel", handleScroll, { passive: true });
});
