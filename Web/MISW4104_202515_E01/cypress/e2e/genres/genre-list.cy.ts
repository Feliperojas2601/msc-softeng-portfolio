import { GenreListPage } from '../../pages/GenreListPage';

describe('HU05: Consultar el listado de géneros', () => {
    let genreListPage: GenreListPage;

    // Given
    beforeEach(() => {
        genreListPage = new GenreListPage();
    });

    it('CP01_HU05 - Debe mostrar el listado de géneros correctamente', () => {
        // When: Navigate to genres list page
        genreListPage.navigate();
        cy.wait(2000);

        // Then: Verify page and genres are displayed
        genreListPage.verifyPageTitle();
        genreListPage.getGenreCount().should('have.length.at.least', 1);
    });
});
