// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    // Constants
    const PHONE_PATTERN = /^[0-9]{10}$/;
    const FORM_SUBMIT_TIMEOUT = 3000; // 3 seconds
    
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

    // CGPA validation for student profile
    const cgpaInput = document.getElementById('cgpa');
    if (cgpaInput) {
        cgpaInput.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (value < 0 || value > 10) {
                this.setCustomValidity('CGPA must be between 0 and 10');
                this.classList.add('is-invalid');
            } else {
                this.setCustomValidity('');
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
    }

    // Phone number validation
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            if (!PHONE_PATTERN.test(this.value) && this.value.length > 0) {
                this.setCustomValidity('Please enter a valid 10-digit phone number');
                this.classList.add('is-invalid');
            } else {
                this.setCustomValidity('');
                this.classList.remove('is-invalid');
                if (this.value.length === 10) {
                    this.classList.add('is-valid');
                }
            }
        });
    }

    // Date validation for drive deadlines
    const deadlineInput = document.getElementById('deadline');
    if (deadlineInput) {
        deadlineInput.addEventListener('change', function() {
            const today = new Date().toISOString().split('T')[0];
            if (this.value < today) {
                alert('Deadline cannot be in the past');
                this.value = today;
            }
        });
        
        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        deadlineInput.setAttribute('min', today);
    }

    // Confirmation dialogs for critical actions
    const deleteLinks = document.querySelectorAll('[data-confirm]');
    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            const message = this.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(message)) {
                event.preventDefault();
            }
        });
    });

    // Form submission loading state
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
                
                // Re-enable after timeout in case of validation errors
                setTimeout(function() {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, FORM_SUBMIT_TIMEOUT);
            }
        });
    });

    // Character counter for textareas
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(function(textarea) {
        const maxLength = textarea.getAttribute('maxlength');
        const counter = document.createElement('div');
        counter.className = 'form-text text-end';
        counter.innerHTML = `<span id="${textarea.id}_count">0</span> / ${maxLength} characters`;
        textarea.parentNode.appendChild(counter);
        
        textarea.addEventListener('input', function() {
            document.getElementById(`${this.id}_count`).textContent = this.value.length;
        });
    });
});
