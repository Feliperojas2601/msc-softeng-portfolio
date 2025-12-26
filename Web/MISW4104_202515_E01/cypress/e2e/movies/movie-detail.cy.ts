import { MovieDetailPage } from '../../pages/MovieDetailPage';
import { MovieListPage } from '../../pages/MovieListPage';

describe('HU08: Consultar información detallada de una película', () => {
    let movieDetailPage: MovieDetailPage;
    let movieListPage: MovieListPage;

    // Given
    beforeEach(() => {
        movieDetailPage = new MovieDetailPage();
        movieListPage = new MovieListPage();
    });

    it('CP01_HU08 - Debe mostrar toda la información de la película correctamente', () => {
        // When: Navigate to movies list
        movieListPage.navigate();
        cy.wait(2000);

        // Then: Verify movie detail information
        movieDetailPage.navigateToFirstMovieAndVerifyInfo(movieListPage);
    });

    it('CP02_HU08 - Debe mostrar información del director', () => {
        // When: Navigate to movies list
        movieListPage.navigate();
        cy.wait(2000);

        // Then: Verify director section is visible
        movieDetailPage.navigateToFirstMovieAndVerifyDirector(movieListPage);
    });

    it('CP03_HU08 - Debe mostrar los actores de la película si existen', () => {
        // When: Navigate to movies list
        movieListPage.navigate();
        cy.wait(2000);

        // Then: Verify actors section is visible
        movieDetailPage.navigateToFirstMovieAndVerifyActors(movieListPage);
    });
});
