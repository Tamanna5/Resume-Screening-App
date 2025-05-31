document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips if using Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Character counter for resume textarea
    const resumeTextarea = document.getElementById('resume_text');
    if (resumeTextarea) {
        const maxLength = 20000;
        resumeTextarea.setAttribute('maxlength', maxLength);
        
        // Create character counter
        const counterDiv = document.createElement('div');
        counterDiv.className = 'form-text text-muted text-end';
        counterDiv.id = 'charCounter';
        counterDiv.innerHTML = `0/${maxLength} characters`;
        resumeTextarea.parentNode.appendChild(counterDiv);
        
        // Update counter on input
        resumeTextarea.addEventListener('input', function() {
            const remaining = this.value.length;
            counterDiv.innerHTML = `${remaining}/${maxLength} characters`;
        });
    }
    
    // Add file size validation
    const fileInput = document.getElementById('resume_file');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const maxSize = 10 * 1024 * 1024; // 10MB
            const fileSize = this.files[0]?.size || 0;
            
            if (fileSize > maxSize) {
                alert('The selected file is too large. Maximum file size is 10MB.');
                this.value = ''; // Clear the input
            }
            
            // Show file name
            const fileLabel = document.createElement('div');
            if (this.files[0]) {
                fileLabel.className = 'alert alert-info mt-2';
                fileLabel.innerHTML = `Selected file: <strong>${this.files[0].name}</strong>`;
                
                // Remove any previous file label
                const previousLabel = document.querySelector('.alert-info');
                if (previousLabel) {
                    previousLabel.remove();
                }
                
                this.parentNode.appendChild(fileLabel);
            }
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert-warning, .alert-danger');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});
