document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.word-section');
    let currentSection = 0;
    let isScrolling = false;

    function scrollToSection(index) {
        sections[index].scrollIntoView({ behavior: 'smooth' });
    }

    window.addEventListener('wheel', function(event) {
        if (isScrolling) return;

        if (event.deltaY > 0) {
            if (currentSection < sections.length - 1) {
                currentSection++;
                scrollToSection(currentSection);
            }
        } else {
            if (currentSection > 0) {
                currentSection--;
                scrollToSection(currentSection);
            }
        }

        isScrolling = true;
        setTimeout(function() {
            isScrolling = false;
        }, 500);
    });
});