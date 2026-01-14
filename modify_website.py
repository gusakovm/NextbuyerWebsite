#!/usr/bin/env python3
"""
Tilda Website Modifier
Replaces fonts with Inter and adds custom form handlers to index.html
"""

import re
from pathlib import Path

def replace_fonts(content):
    """Replace Manrope and TTHovesPro with Inter"""

    print("  - Replacing Google Fonts CDN link...")
    # Replace Google Fonts CDN
    content = re.sub(
        r'family=Manrope:wght@[^&]+&subset=[^&]+',
        'family=Inter:wght@300;400;500;600;700',
        content
    )

    print("  - Replacing CSS variables...")
    # Replace CSS variables
    content = re.sub(
        r"--t-headline-font:\s*'Manrope',\s*Arial,\s*sans-serif",
        "--t-headline-font:'Inter',Arial,sans-serif",
        content
    )
    content = re.sub(
        r"--t-text-font:\s*'Manrope',\s*Arial,\s*sans-serif",
        "--t-text-font:'Inter',Arial,sans-serif",
        content
    )

    print("  - Replacing Manrope font-family declarations...")
    # Replace all Manrope declarations
    content = re.sub(
        r"font-family:\s*'Manrope',\s*Arial,\s*sans-serif",
        "font-family:'Inter',Arial,sans-serif",
        content,
        flags=re.IGNORECASE
    )

    print("  - Replacing TTHovesPro font-family declarations...")
    # Replace all TTHovesPro declarations
    content = re.sub(
        r"font-family:\s*'TTHovesPro',\s*Arial,\s*sans-serif",
        "font-family:'Inter',Arial,sans-serif",
        content,
        flags=re.IGNORECASE
    )

    print("  - Replacing TTHovesPro in Tilda Zero data attributes...")
    # Replace TTHovesPro in data-field attributes (Tilda Zero blocks)
    content = re.sub(
        r'data-field-fieldfontfamily-value="TTHovesPro"',
        'data-field-fieldfontfamily-value="Inter"',
        content
    )
    content = re.sub(
        r'data-field-buttonfontfamily-value="TTHovesPro"',
        'data-field-buttonfontfamily-value="Inter"',
        content
    )
    content = re.sub(
        r'data-field-inputfontfamily-value="TTHovesPro"',
        'data-field-inputfontfamily-value="Inter"',
        content
    )

    print("  - Replacing TTHovesPro in CSS (without Arial fallback)...")
    # Replace TTHovesPro without Arial fallback (in style blocks)
    content = re.sub(
        r"font-family:\s*'TTHovesPro'",
        "font-family:'Inter'",
        content
    )

    return content

def add_contact_buttons_handler(content):
    """Add handler for Contact us buttons to scroll to first form"""

    contact_handler = '''<script>
// Contact us buttons handler - scroll to first form
(function() {
    'use strict';

    var CONTACT_ELEM_IDS = ['1712930274148', '1713892925926'];
    var FIRST_FORM_REC = '739844601';

    function scrollToFirstForm() {
        var firstForm = document.getElementById('rec' + FIRST_FORM_REC);
        if (!firstForm) {
            console.log('[Nextbuyer] First form not found');
            return;
        }

        // Scroll to form
        firstForm.scrollIntoView({ behavior: 'smooth', block: 'center' });

        // Wait for scroll, then focus email input
        setTimeout(function() {
            var emailInput = firstForm.querySelector('input[type="email"], input[name="email"], input[placeholder*="email" i]');
            if (emailInput) {
                emailInput.focus();
                console.log('[Nextbuyer] Focused on email input');
            }
        }, 800);
    }

    function initContactButtons() {
        console.log('[Nextbuyer] Initializing Contact us buttons...');

        CONTACT_ELEM_IDS.forEach(function(elemId) {
            var elem = document.querySelector('[data-elem-id="' + elemId + '"]');
            if (!elem) {
                elem = document.querySelector("[data-elem-id='" + elemId + "']");
            }

            if (!elem) {
                console.log('[Nextbuyer] Contact button not found:', elemId);
                return;
            }

            elem.style.cursor = 'pointer';
            elem.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('[Nextbuyer] Contact us clicked:', elemId);
                scrollToFirstForm();
            });

            console.log('[Nextbuyer] Contact button handler attached:', elemId);
        });
    }

    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        setTimeout(initContactButtons, 500);
    } else {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(initContactButtons, 500);
        });
    }
})();
</script>
'''

    anchor = "<!-- Stat -->"
    if anchor in content:
        print("  - Inserting Contact us buttons handler...")
        content = content.replace(anchor, contact_handler + '\n' + anchor)
    else:
        print("  ⚠️  WARNING: Could not find insertion point for Contact handler")

    return content

def add_form_handler(content):
    """Add custom form handler before tilda-stat"""

    form_handler = '''<style>
/* Toast notification styles */
.nb-toast {
    position: fixed;
    top: 24px;
    left: 50%;
    transform: translateX(-50%);
    padding: 12px 24px;
    border-radius: 8px;
    font-family: 'Inter', Arial, sans-serif;
    font-size: 14px;
    font-weight: 500;
    color: #fff;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 999999;
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
}
.nb-toast.show {
    opacity: 1;
}
.nb-toast.success {
    background: #10b981;
}
.nb-toast.error {
    background: #ef4444;
}
.nb-toast.info {
    background: #3b82f6;
}
</style>
<script>
// Custom form handler for Nextbuyer email capture forms
(function() {
    'use strict';

    var TARGET_RECS = ['739844601', '739844630'];

    // Toast notification function
    function showToast(message, type) {
        type = type || 'info';

        // Remove existing toast if any
        var existingToast = document.getElementById('nb-toast');
        if (existingToast) {
            existingToast.remove();
        }

        // Create toast element
        var toast = document.createElement('div');
        toast.id = 'nb-toast';
        toast.className = 'nb-toast ' + type;
        toast.textContent = message;
        document.body.appendChild(toast);

        // Show toast with animation
        setTimeout(function() {
            toast.classList.add('show');
        }, 10);

        // Hide and remove after 3 seconds
        setTimeout(function() {
            toast.classList.remove('show');
            setTimeout(function() {
                if (toast.parentNode) {
                    toast.remove();
                }
            }, 300);
        }, 3000);
    }

    function initFormHandler() {
        console.log('[Nextbuyer] Initializing custom form handler...');

        TARGET_RECS.forEach(function(recid) {
            var rec = document.getElementById('rec' + recid);
            if (!rec) {
                console.log('[Nextbuyer] Record not found:', recid);
                return;
            }

            // Find submit button in this record
            var submitBtn = rec.querySelector('button[type="submit"], .t-submit');
            if (!submitBtn) {
                console.log('[Nextbuyer] Submit button not found in:', recid);
                return;
            }

            console.log('[Nextbuyer] Attaching handler to rec' + recid);

            // Attach click handler with capture phase (fires before Tilda)
            submitBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();

                console.log('[Nextbuyer] Form submission intercepted for rec' + recid);

                // Get email input
                var emailInput = rec.querySelector('input[type="email"], input[name="email"], input[placeholder*="email" i]');
                if (!emailInput) {
                    console.error('[Nextbuyer] Email input not found');
                    showToast('Form error. Please try again.', 'error');
                    return false;
                }

                var email = emailInput.value.trim();
                if (!email) {
                    showToast('Please enter your email address.', 'info');
                    return false;
                }

                // Simple email validation
                if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                    showToast('Please enter a valid email address.', 'error');
                    return false;
                }

                console.log('[Nextbuyer] Sending to API:', {email: email});

                // Disable button
                submitBtn.disabled = true;
                var originalText = submitBtn.textContent;
                submitBtn.textContent = 'Sending...';

                // Send to custom endpoint
                fetch('https://api.cdoc.cc/nextbuyer-step1', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({email: email})
                })
                .then(function(response) {
                    if (response.ok) {
                        console.log('[Nextbuyer] Submission successful');
                        showToast('Thank you! Your submission has been received.', 'success');
                        emailInput.value = '';
                    } else {
                        console.error('[Nextbuyer] API error:', response.status);
                        showToast('Submission failed. Please try again later.', 'error');
                    }
                })
                .catch(function(error) {
                    console.error('[Nextbuyer] Network error:', error);
                    showToast('Network error. Please check your connection.', 'error');
                })
                .finally(function() {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                });

                return false;
            }, true); // true = capture phase, fires before bubbling

            console.log('[Nextbuyer] Handler attached to rec' + recid);
        });
    }

    // Wait for DOM and forms to be ready
    function tryInit() {
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            // DOM is ready, wait a bit for Tilda to render forms
            setTimeout(initFormHandler, 500);
        } else {
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(initFormHandler, 500);
            });
        }
    }

    tryInit();
})();
</script>
'''

    # Insert before tilda-stat comment
    anchor = "<!-- Stat -->"
    if anchor in content:
        print("  - Inserting form handler script before tilda-stat...")
        content = content.replace(anchor, form_handler + '\n' + anchor)
    else:
        print("  ⚠️  WARNING: Could not find insertion point for form handler")

    return content

def main():
    index_file = Path('docs/index.html')
    original_file = Path('docs/index.html.original')
    backup_file = Path('docs/index.html.backup')

    print("="*70)
    print("Tilda Website Modifier")
    print("="*70)

    # Read from original (clean) file
    if original_file.exists():
        print(f"\n📖 Reading clean version from {original_file}...")
        content = original_file.read_text(encoding='utf-8')
    else:
        print(f"\n📖 Reading {index_file}...")
        content = index_file.read_text(encoding='utf-8')

    original_size = len(content)

    # Create backup
    print(f"💾 Creating backup at {backup_file}...")
    backup_file.write_text(content, encoding='utf-8')

    # Apply transformations
    print(f"\n🔤 Replacing fonts with Inter...")
    content = replace_fonts(content)

    print(f"\n🔘 Adding Contact us buttons handler...")
    content = add_contact_buttons_handler(content)

    print(f"\n📝 Adding custom form handler...")
    content = add_form_handler(content)

    # Write modified file
    print(f"\n💿 Writing modified file to {index_file}...")
    index_file.write_text(content, encoding='utf-8')

    new_size = len(content)

    print("\n" + "="*70)
    print("✅ Complete!")
    print("="*70)
    print(f"Original size: {original_size:,} bytes")
    print(f"New size:      {new_size:,} bytes")
    print(f"Difference:    {new_size - original_size:+,} bytes")
    print(f"\nBackup saved to: {backup_file}")
    print("\nNext steps:")
    print("  1. Run verification commands (see plan)")
    print("  2. Test locally: cd docs && python3 -m http.server 8000")
    print("  3. Commit and push to deploy")

if __name__ == '__main__':
    main()
