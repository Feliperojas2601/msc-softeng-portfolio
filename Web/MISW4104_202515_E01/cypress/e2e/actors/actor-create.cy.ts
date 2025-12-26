import { ActorCreatePage } from '../../pages/ActorCreatePage';
import { ActorListPage } from '../../pages/ActorListPage';
import { DataGenerators } from '../../support/dataGenerators';

describe('HU11: Crear un actor', () => {
    let actorCreatePage: ActorCreatePage;
    let actorListPage: ActorListPage;
    let newActorData: any;

    // Given
    beforeEach(() => {
        actorCreatePage = new ActorCreatePage();
        actorListPage = new ActorListPage();
        newActorData = DataGenerators.generateActor();
    });

    it('CP01_HU11 - Debe crear un actor exitosamente con datos válidos', () => {
        // When: Fill form and submit
        actorCreatePage.navigate();
        actorCreatePage.verifyPageTitle();
        actorCreatePage.fillActorForm(newActorData);
        actorCreatePage.clickSubmit();
        cy.wait(3000);

        // Then: Verify actor appears in the list
        actorListPage.navigate();
        cy.wait(2000);
        actorListPage.verifyActorExists(newActorData.name);
    });

    it('CP02_HU11 - No debe permitir crear actor sin campos obligatorios', () => {
        // When: Navigate to create form without filling required fields
        actorCreatePage.navigate();
        actorCreatePage.verifyPageTitle();

        // Then: Submit button should show validation errors
        actorCreatePage.verifySubmitButtonShowsErrors();
    });

    it('CP03_HU11 - Debe reestablecer el formulario al cancelar', () => {
        // When: Fill form and cancel
        actorCreatePage.navigate();
        actorCreatePage.fillActorName(newActorData.name);
        actorCreatePage.clickCancel();

        // Then: Form fields should be cleared
        actorCreatePage.verifyFormIsEmpty();
    });
});
