import { ActorListPage } from '../../pages/ActorListPage';

describe('HU01: Consultar el listado de actores', () => {
    let actorListPage: ActorListPage;

    // Given
    beforeEach(() => {
        actorListPage = new ActorListPage();
    });

    it('CP01_HU01 - Debe mostrar el listado de actores correctamente', () => {
        // When: Navigate to actors list page
        actorListPage.navigate();
        cy.wait(2000);

        // Then: Verify page and actors are displayed
        actorListPage.verifyPageTitle();
        actorListPage.getActorCount().should('have.length.at.least', 1);
    });

    it('CP02_HU01 - Debe filtrar actores por nombre correctamente', () => {
        // When: Navigate and search for first actor
        actorListPage.navigate();
        cy.wait(2000);

        // Then: Search and verify first actor is visible
        actorListPage.searchAndVerifyFirstActor();
    });

    it('CP03_HU01 - Debe navegar al detalle del actor al hacer clic', () => {
        // When: Navigate and click on first actor
        actorListPage.navigate();
        cy.wait(2000);
        actorListPage.clickFirstActor();

        // Then: Verify navigation to detail page
        actorListPage.verifyUrlContains('/actor/');
    });
});
