// script.js
document.addEventListener('DOMContentLoaded', function() {

    const signupForm = document.getElementById('signup-form');
    const contactForm = document.getElementById('contact-form');

    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission

            // Basic form validation (expand as needed)
            const email = document.getElementById('somaiya-email').value;
            const instagram = document.getElementById('instagram-handle').value;

            if (!email.includes('@somaiya.edu')) {
                alert('Please use a valid Somaiya email address.');
                return;
            }

            // You would typically send this data to a backend server
            // for processing (e.g., using fetch or XMLHttpRequest)
            console.log('Signup form submitted!');
            console.log('Email:', email);
            console.log('Instagram:', instagram);

            // Reset the form (optional)
            signupForm.reset();
        });
    }

    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();

            // Basic validation
            const name = document.getElementById('name').value;
            const email = document.getElementById('somaiya-email-contact').value;
            const subject = document.getElementById('subject').value;
            const message = document.getElementById('message').value;

             if (!email.includes('@somaiya.edu')) {
                alert('Please use a valid Somaiya email address.');
                return;
            }

            console.log('Contact form submitted!');
            console.log('Name:', name);
            console.log('Email:', email);
            console.log('Subject:', subject);
            console.log('Message:', message);

            contactForm.reset();
        });
    }

    // Smooth scrolling for navigation links
    document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href').slice(1); // Remove the '#'
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 50, // Adjust for header height
                    behavior: 'smooth'
                });
            }
        });
    });
});