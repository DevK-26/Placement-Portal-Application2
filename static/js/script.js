// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Password confirmation validation
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirm_password');
        const passwordHelp = document.getElementById('passwordHelp');

        function validatePasswords() {
            if (confirmPassword.value === '') {
                passwordHelp.textContent = '';
                passwordHelp.className = 'form-text';
                return;
            }

            if (password.value === confirmPassword.value) {
                passwordHelp.textContent = 'Passwords match!';
                passwordHelp.className = 'form-text text-success';
                confirmPassword.classList.remove('is-invalid');
                confirmPassword.classList.add('is-valid');
            } else {
                passwordHelp.textContent = 'Passwords do not match!';
                passwordHelp.className = 'form-text text-danger';
                confirmPassword.classList.remove('is-valid');
                confirmPassword.classList.add('is-invalid');
            }
        }

        password.addEventListener('input', validatePasswords);
        confirmPassword.addEventListener('input', validatePasswords);

        // Form validation on submit
        registerForm.addEventListener('submit', function(event) {
            if (password.value !== confirmPassword.value) {
                event.preventDefault();
                event.stopPropagation();
                alert('Passwords do not match!');
            }

            if (password.value.length < 6) {
                event.preventDefault();
                event.stopPropagation();
                alert('Password must be at least 6 characters long!');
            }
        });
    }
});
