// demoHandler.js
console.log('Demo handler script loaded');

document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded - initializing demo buttons');

    // Get all demo buttons
    const demoButtons = document.querySelectorAll('.demo-btn');
    console.log(`Found ${demoButtons.length} demo buttons`);

    // Get textarea
    const textArea = document.getElementById('text');
    if (!textArea) {
        console.error('Textarea with id="text" not found');
        return;
    }

    // Load demo content
    fetch('/static/demo_content.json')
        .then(response => {
            if (!response.ok) throw new Error('Failed to load demo content');
            return response.json();
        })
        .then(data => {
            console.log('Demo content loaded successfully');

            // Add click handlers
            demoButtons.forEach(button => {
                button.addEventListener('click', function () {
                    const demoKey = this.dataset.demo;
                    console.log(`Button clicked: ${demoKey}`);

                    const demoText = data[demoKey];
                    if (demoText) {
                        textArea.value = demoText;
                        textArea.focus();
                        console.log(`Inserted demo text for ${demoKey}`);
                    } else {
                        console.error(`No demo text found for key: ${demoKey}`);
                    }
                });
            });
        })
        .catch(error => {
            console.error('Error loading demo content:', error);
        });
});