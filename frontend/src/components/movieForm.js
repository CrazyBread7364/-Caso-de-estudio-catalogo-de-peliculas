/**
 * Movie form component handler.
 * Encapsulates reading, resetting, and toggling state of the form.
 */

/**
 * Reads and parses values from the movie registration form.
 * @param {HTMLFormElement} form
 * @returns {{ title: string, director: string, genre: string, duration_minutes: number }}
 */
export function readMovieForm(form) {
  const formData = new FormData(form);
  return {
    title: (formData.get('title') || '').toString().trim(),
    director: (formData.get('director') || '').toString().trim(),
    genre: (formData.get('genre') || '').toString().trim(),
    duration_minutes: Number(formData.get('duration_minutes')),
  };
}

/**
 * Resets form input values and restores focus to the first editable input.
 * @param {HTMLFormElement} form
 */
export function resetMovieForm(form) {
  form.reset();
  const firstInput = form.querySelector('input:not([type="hidden"])');
  if (firstInput) {
    firstInput.focus();
  }
}

/**
 * Toggles the disabled state of the submit button and inputs to prevent duplicate submissions.
 * @param {HTMLFormElement} form
 * @param {boolean} disabled
 */
export function setFormDisabled(form, disabled) {
  const submitBtn = form.querySelector('button[type="submit"]');
  if (submitBtn) {
    submitBtn.disabled = Boolean(disabled);
  }
}
