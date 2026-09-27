/**
 * API client module for Movie Service.
 * Centralizes all HTTP communications with the backend API.
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
const BASE_URL = `${API_URL.replace(/\/+$/, '')}/movies/`;

/**
 * Parses DRF error responses into a human-readable string.
 * @param {Record<string, string | string[]>} data
 * @returns {string}
 */
function parseErrors(data) {
  if (!data || typeof data !== 'object') {
    return 'Error inesperado del servidor.';
  }
  return Object.entries(data)
    .map(([field, msgs]) => `${field}: ${[].concat(msgs).join(', ')}`)
    .join(' | ');
}

/**
 * Executes a network fetch with network failure handling.
 * @param {string} url
 * @param {RequestInit} [options]
 * @returns {Promise<Response>}
 */
async function request(url, options) {
  try {
    return await fetch(url, options);
  } catch {
    throw new Error('No se pudo conectar con el servidor.');
  }
}

/**
 * Retrieves the list of movies.
 * @returns {Promise<Array<{id: number, title: string, director: string, genre: string, duration_minutes: number}>>}
 */
export async function getMovies() {
  const res = await request(BASE_URL);
  if (!res.ok) {
    throw new Error('No se pudo cargar el catálogo.');
  }
  return res.json();
}

/**
 * Registers a new movie in the catalog.
 * @param {{title: string, director: string, genre: string, duration_minutes: number}} movie
 * @returns {Promise<{id: number, title: string, director: string, genre: string, duration_minutes: number}>}
 */
export async function createMovie(movie) {
  const res = await request(BASE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(movie),
  });

  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(parseErrors(data) || `Error ${res.status}: ${res.statusText}`);
  }
  return data;
}
