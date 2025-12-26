import { DirectorListPage } from '../../pages/DirectorListPage';
import { DataGenerators } from '../../support/dataGenerators';

describe('HU03: Consultar el listado de directores', () => {
    let directorListPage: DirectorListPage;

    // Given
    beforeEach(() => {
        directorListPage = new DirectorListPage();
    });

    it('CP01_HU03 - Debe mostrar el listado de directores correctamente', () => {
        // When: Navigate to directors list page
        directorListPage.navigate();
        cy.wait(2000);

        // Then: Verify page and directors are displayed
        directorListPage.verifyPageTitle();
        directorListPage.getDirectorCount().should('have.length.at.least', 1);
    });

    it('CP02_HU03 - Debe filtrar directores por nombre correctamente', () => {
        // When: Navigate and search for first director
        directorListPage.navigate();
        cy.wait(2000);

        // Then: Search and verify first director is visible
        directorListPage.searchAndVerifyFirstDirector();
    });

    it('CP03_HU03 - Debe navegar al detalle del director al hacer clic', () => {
        // When: Navigate and click on first director
        directorListPage.navigate();
        cy.wait(2000);
        directorListPage.clickFirstDirector();

        // Then: Verify navigation to detail page
        directorListPage.verifyUrlContains('/director/');
    });

});
