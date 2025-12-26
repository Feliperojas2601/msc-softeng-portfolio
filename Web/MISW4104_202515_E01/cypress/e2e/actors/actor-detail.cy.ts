import { ActorDetailPage } from '../../pages/ActorDetailPage';
import { ActorListPage } from '../../pages/ActorListPage';

describe('HU02: Consultar información detallada de un actor', () => {
    let actorDetailPage: ActorDetailPage;
    let actorListPage: ActorListPage;

    // Given
    beforeEach(() => {
        actorDetailPage = new ActorDetailPage();
        actorListPage = new ActorListPage();
    });

    it('CP01_HU02 - Debe mostrar toda la información del actor correctamente', () => {
        // When: Navigate to actors list
        actorListPage.navigate();
        cy.wait(2000);

        // Then: Verify actor detail information
        actorDetailPage.navigateToFirstActorAndVerifyInfo(actorListPage);
    });

    it('CP02_HU02 - Debe mostrar las películas del actor si existen', () => {
        // When: Navigate to actors list
        actorListPage.navigate();
        cy.wait(2000);

        // Then: Verify movies list is visible
        actorDetailPage.navigateToFirstActorAndVerifyMovies(actorListPage);
    });

    it('CP03_HU02 - Debe navegar al detalle de película al hacer clic en una película', () => {
        // When: Navigate to actors list
        actorListPage.navigate();
        cy.wait(2000);
        actorDetailPage.navigateToFirstActorAndClickFirstMovie(actorListPage);

        // Then: Verify navigation to movie detail
        actorDetailPage.verifyUrlContains('/movie/');
    });
});
