/**
 * Status message feedback component.
 * Safely displays status messages using textContent and toggles CSS status classes.
 */

/**
 * Updates the message container with text and applies appropriate visual styling.
 * @param {HTMLElement} el
 * @param {string} text
 * @param {'success' | 'error'} type
 */
export function showMessage(el, text, type) {
  if (!el) return;

  el.textContent = text || '';
  el.className = '';

  if (type === 'success') {
    el.classList.add('success');
  } else if (type === 'error') {
    el.classList.add('error');
  }
}
