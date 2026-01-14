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

def add_form_handler(content):
    """Add custom form handler before tilda-stat"""

    form_handler = '''<script>
// Custom form handler for Nextbuyer email capture forms
(function() {
    'use strict';

    function waitForTildaForm() {
        if (typeof window.tildaForm !== 'undefined') {
            initCustomFormHandler();
        } else {
            setTimeout(waitForTildaForm, 100);
        }
    }

    function initCustomFormHandler() {
        var originalSubmit = window.tildaForm.submit;

        window.tildaForm.submit = function(recid, formid, formoptions) {
            console.log('Form submission:', {recid: recid});

            // Only intercept our 2 email capture forms
            if (recid !== '739844601' && recid !== '739844630') {
                if (originalSubmit) {
                    return originalSubmit.call(this, recid, formid, formoptions);
                }
                return;
            }

            var form = document.querySelector('#rec' + recid + ' form');
            if (!form) {
                form = document.querySelector('#rec' + recid);
            }

            if (!form) {
                console.error('Form not found:', recid);
                alert('Form submission error. Please try again.');
                return false;
            }

            var formData = new FormData(form);
            var data = {};
            formData.forEach(function(value, key) {
                data[key] = value;
            });

            console.log('Sending to custom endpoint:', data);

            fetch('https://api.cdoc.cc/nextbuyer-step1', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(function(response) {
                if (response.ok) {
                    alert('Thank you! Your submission has been received.');
                    if (form.reset) form.reset();
                } else {
                    alert('Submission failed. Please try again later.');
                }
            })
            .catch(function(error) {
                console.error('Submission error:', error);
                alert('Network error. Please check your connection.');
            });

            return false;
        };

        console.log('Custom form handler initialized');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', waitForTildaForm);
    } else {
        waitForTildaForm();
    }
})();
</script>
'''

    # Insert before tilda-stat
    anchor = "window.tildastatcookie='no';"
    if anchor in content:
        print("  - Inserting form handler script before tilda-stat...")
        content = content.replace(anchor, form_handler + '\n' + anchor)
    else:
        print("  ⚠️  WARNING: Could not find insertion point for form handler")

    return content

def main():
    index_file = Path('docs/index.html')
    backup_file = Path('docs/index.html.backup')

    print("="*70)
    print("Tilda Website Modifier")
    print("="*70)

    # Read file
    print(f"\n📖 Reading {index_file}...")
    content = index_file.read_text(encoding='utf-8')
    original_size = len(content)

    # Create backup
    print(f"💾 Creating backup at {backup_file}...")
    backup_file.write_text(content, encoding='utf-8')

    # Apply transformations
    print(f"\n🔤 Replacing fonts with Inter...")
    content = replace_fonts(content)

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
