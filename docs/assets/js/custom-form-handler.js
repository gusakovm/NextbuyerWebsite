// Custom form handler to redirect Tilda forms to api.cdoc.cc
(function() {
    'use strict';

    // Wait for DOM to be ready
    function initFormHandler() {
        // Find all Tilda forms
        var forms = document.querySelectorAll('.t-form, .t-form__inputsbox');

        if (forms.length === 0) {
            console.log('No Tilda forms found');
            return;
        }

        console.log('Found ' + forms.length + ' Tilda forms');

        // Override the default Tilda form submission
        var originalSubmit = window.tildaForm ? window.tildaForm.submit : null;

        if (window.tildaForm) {
            window.tildaForm.submit = function(recid, formid, formoptions) {
                console.log('Intercepting form submission:', {recid: recid, formid: formid});

                // Get form data
                var form = document.querySelector('#rec' + recid + ' form');
                if (!form) {
                    console.error('Form not found for recid:', recid);
                    return;
                }

                var formData = new FormData(form);
                var data = {};
                formData.forEach(function(value, key) {
                    data[key] = value;
                });

                // Send to custom endpoint
                fetch('https://api.cdoc.cc/nextbuyer-step1', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                })
                .then(function(response) {
                    if (response.ok) {
                        console.log('Form submitted successfully to api.cdoc.cc');
                        // Show success message
                        if (window.t_forms__showSuccessPopup) {
                            window.t_forms__showSuccessPopup(recid, formid);
                        }
                    } else {
                        console.error('Form submission failed:', response.status);
                        // Show error message
                        if (window.t_forms__showErrorPopup) {
                            window.t_forms__showErrorPopup(recid, formid);
                        }
                    }
                })
                .catch(function(error) {
                    console.error('Form submission error:', error);
                    if (window.t_forms__showErrorPopup) {
                        window.t_forms__showErrorPopup(recid, formid);
                    }
                });

                // Prevent default Tilda submission
                return false;
            };
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initFormHandler);
    } else {
        // DOM already loaded
        initFormHandler();
    }

    // Also try to initialize after a delay to catch dynamically loaded forms
    setTimeout(initFormHandler, 2000);
})();
