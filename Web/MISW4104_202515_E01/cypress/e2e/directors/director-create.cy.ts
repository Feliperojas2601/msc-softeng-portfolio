import { DirectorCreatePage } from '../../pages/DirectorCreatePage';
import { DirectorListPage } from '../../pages/DirectorListPage';
import { DataGenerators } from '../../support/dataGenerators';

describe('HU12: Crear un director', () => {
    let directorCreatePage: DirectorCreatePage;
    let directorListPage: DirectorListPage;
    let newDirectorData: any;

    // Given
    beforeEach(() => {
        directorCreatePage = new DirectorCreatePage();
        directorListPage = new DirectorListPage();
        newDirectorData = DataGenerators.generateDirector();
    });

    it('CP01_HU12 - Debe crear un director exitosamente con datos válidos', () => {
        // When: Fill form and submit
        directorCreatePage.navigate();
        directorCreatePage.verifyPageTitle();
        directorCreatePage.fillDirectorForm(newDirectorData);
        directorCreatePage.clickSubmit();
        cy.wait(3000);

        // Then: Verify director appears in the list
        directorListPage.navigate();
        cy.wait(2000);
        directorListPage.verifyDirectorExists(newDirectorData.name);
    });

    it('CP02_HU12 - No debe permitir crear director sin campos obligatorios', () => {
        // When: Navigate to create form without filling required fields
        directorCreatePage.navigate();
        directorCreatePage.verifyPageTitle();

        // Then: Submit button should show validation errors
        directorCreatePage.verifySubmitButtonShowsErrors();
    });

    it('CP03_HU12 - Debe reestablecer el formulario al cancelar', () => {
        // When: Fill form and cancel
        directorCreatePage.navigate();
        directorCreatePage.fillDirectorName(newDirectorData.name);
        directorCreatePage.clickCancel();

        // Then: Form fields should be cleared
        directorCreatePage.verifyFormIsEmpty();
    });

});
