import { MovieListPage } from '../../pages/MovieListPage';

describe('HU07: Consultar el listado de películas', () => {
    let movieListPage: MovieListPage;

    // Given
    beforeEach(() => {
        movieListPage = new MovieListPage();
    });

    it('CP01_HU07 - Debe mostrar el listado de películas correctamente', () => {
        // When: Navigate to movies list page
        movieListPage.navigate();
        cy.wait(2000);

        // Then: Verify page and movies are displayed
        movieListPage.verifyPageTitle();
        movieListPage.getMovieCount().should('have.length.at.least', 1);
    });

    it('CP02_HU07 - Debe filtrar películas por título correctamente', () => {
        // When: Navigate and search for first movie
        movieListPage.navigate();
        cy.wait(2000);

        // Then: Search and verify first movie is visible
        movieListPage.searchAndVerifyFirstMovie();
    });

    it('CP03_HU07 - Debe navegar al detalle al hacer clic en película', () => {
        // When: Navigate and click on first movie
        movieListPage.navigate();
        cy.wait(2000);
        movieListPage.clickFirstMovie();

        // Then: Verify navigation to detail page
        movieListPage.verifyUrlContains('/movie/');
    });
});
