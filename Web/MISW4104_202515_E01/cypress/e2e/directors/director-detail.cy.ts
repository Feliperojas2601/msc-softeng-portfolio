import { DirectorDetailPage } from '../../pages/DirectorDetailPage';
import { DirectorListPage } from '../../pages/DirectorListPage';

describe('HU04: Consultar información detallada de un director', () => {
    let directorDetailPage: DirectorDetailPage;
    let directorListPage: DirectorListPage;

    // Given
    beforeEach(() => {
        directorDetailPage = new DirectorDetailPage();
        directorListPage = new DirectorListPage();
    });

    it('CP01_HU04 - Debe mostrar toda la información del director correctamente', () => {
        // When: Navigate to directors list
        directorListPage.navigate();
        cy.wait(2000);

        // Then: Verify director detail information
        directorDetailPage.navigateToFirstDirectorAndVerifyInfo(directorListPage);
    });

    it('CP02_HU04 - Debe mostrar las películas del director si existen', () => {
        // When: Navigate to directors list
        directorListPage.navigate();
        cy.wait(2000);

        // Then: Verify movies list is visible
        directorDetailPage.navigateToFirstDirectorAndVerifyMovies(directorListPage);
    });

    it('CP03_HU04 - Debe navegar al detalle de película al hacer clic en una película', () => {
        // When: Navigate to directors list
        directorListPage.navigate();
        cy.wait(2000);
        directorDetailPage.navigateToFirstDirectorAndClickFirstMovie(directorListPage);

        // Then: Verify navigation to movie detail
        directorDetailPage.verifyUrlContains('/movie/');
    });
});
