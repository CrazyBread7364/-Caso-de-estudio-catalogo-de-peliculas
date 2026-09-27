import './style.css';
import { getMovies, createMovie } from './api/movieApi.js';
import { readMovieForm, resetMovieForm, setFormDisabled } from './components/movieForm.js';
import { renderMovieTable } from './components/movieTable.js';
import { showMessage } from './components/message.js';

// DOM Element references
const form = document.getElementById('movie-form');
const tbody = document.getElementById('movie-list');
const messageEl = document.getElementById('message');

/**
 * Fetches and renders the catalog of movies.
 */
async function loadMovies() {
  try {
    const movies = await getMovies();
    renderMovieTable(tbody, movies);
  } catch (err) {
    showMessage(messageEl, err.message, 'error');
  }
}

// Form submission handler
if (form) {
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    setFormDisabled(form, true);

    try {
      const movie = readMovieForm(form);
      const created = await createMovie(movie);
      showMessage(
        messageEl,
        `Película "${created.title}" registrada con ID ${created.id}.`,
        'success'
      );
      resetMovieForm(form);
      await loadMovies();
    } catch (err) {
      showMessage(messageEl, err.message, 'error');
    } finally {
      setFormDisabled(form, false);
    }
  });
}

// Initial bootstrap call
loadMovies();
