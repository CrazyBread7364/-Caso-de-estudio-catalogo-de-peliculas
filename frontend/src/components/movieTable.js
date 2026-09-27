/**
 * Movie table renderer component.
 * Safely renders movie rows into the DOM using standard DOM APIs (no innerHTML).
 */

/**
 * Renders the movie catalog into the provided tbody element.
 * @param {HTMLTableSectionElement} tbody
 * @param {Array<{ id: number, title: string, director: string, genre: string, duration_minutes: number }>} movies
 */
export function renderMovieTable(tbody, movies) {
  tbody.replaceChildren();

  if (!Array.isArray(movies) || movies.length === 0) {
    const emptyRow = tbody.insertRow();
    const emptyCell = emptyRow.insertCell();
    emptyCell.colSpan = 5;
    emptyCell.textContent = 'Aún no hay películas registradas.';
    emptyCell.className = 'empty-table-message';
    return;
  }

  for (const movie of movies) {
    const row = tbody.insertRow();

    const cellId = row.insertCell();
    cellId.textContent = movie.id ?? '';

    const cellTitle = row.insertCell();
    cellTitle.textContent = movie.title ?? '';

    const cellDirector = row.insertCell();
    cellDirector.textContent = movie.director ?? '';

    const cellGenre = row.insertCell();
    cellGenre.textContent = movie.genre ?? '';

    const cellDuration = row.insertCell();
    cellDuration.textContent = movie.duration_minutes ?? '';
  }
}
