/**
 * CampusVote — Custom JavaScript
 * Student Election Management System
 *
 * Handles: alert auto-dismiss, form validation,
 * candidate selection, and confirmation modals.
 */

document.addEventListener('DOMContentLoaded', function () {

    // --- Auto-dismiss alerts after 5 seconds ---
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        }, 5000);
    });

    // --- Candidate card selection ---
    const candidateCards = document.querySelectorAll('.candidate-card');
    candidateCards.forEach(function (card) {
        card.addEventListener('click', function () {
            // Remove selected class from all cards
            candidateCards.forEach(function (c) {
                c.classList.remove('selected');
            });
            // Add selected class to clicked card
            card.classList.add('selected');
            // Check the hidden radio button
            const radio = card.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = true;
            }
            // Enable submit button
            const submitBtn = document.getElementById('vote-submit-btn');
            if (submitBtn) {
                submitBtn.disabled = false;
            }
        });
    });

    // --- Vote confirmation modal ---
    const voteForm = document.getElementById('vote-form');
    if (voteForm) {
        voteForm.addEventListener('submit', function (e) {
            const selected = document.querySelector(
                '.candidate-card.selected'
            );
            if (!selected) {
                e.preventDefault();
                const errorDiv = document.getElementById('vote-error');
                if (errorDiv) {
                    errorDiv.textContent =
                        'Please select a candidate before voting.';
                    errorDiv.classList.remove('d-none');
                }
                return;
            }
        });
    }

    // --- Form validation feedback ---
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // --- Confirm delete actions ---
    const deleteButtons = document.querySelectorAll(
        '[data-confirm-delete]'
    );
    deleteButtons.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            const message = btn.getAttribute('data-confirm-delete');
            if (!confirm(message || 'Are you sure you want to delete this?')) {
                e.preventDefault();
            }
        });
    });

});