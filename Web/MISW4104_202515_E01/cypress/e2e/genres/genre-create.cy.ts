import { GenreCreatePage } from '../../pages/GenreCreatePage';
import { GenreListPage } from '../../pages/GenreListPage';
import { DataGenerators } from '../../support/dataGenerators';

describe('HU13: Crear un género', () => {
    let genreCreatePage: GenreCreatePage;
    let genreListPage: GenreListPage;
    let newGenreData: any;

    // Given
    beforeEach(() => {
        genreCreatePage = new GenreCreatePage();
        genreListPage = new GenreListPage();
        newGenreData = DataGenerators.generateGenre();
    });

    it('CP01_HU13 - Debe crear un género exitosamente con datos válidos', () => {
        // When: Fill form and submit
        genreCreatePage.navigate();
        genreCreatePage.verifyPageTitle();
        genreCreatePage.fillGenreForm(newGenreData);
        genreCreatePage.clickSubmit();
        cy.wait(3000);

        // Then: Verify genre appears in the list
        genreListPage.navigate();
        cy.wait(2000);
        genreListPage.verifyGenreVisible(newGenreData.type);
    });

    it('CP02_HU13 - No debe permitir crear género sin campos obligatorios', () => {
        // When: Navigate to create form without filling required fields
        genreCreatePage.navigate();
        genreCreatePage.verifyPageTitle();

        // Then: Submit button should show validation errors
        genreCreatePage.verifySubmitButtonShowsErrors();
    });

    it('CP03_HU13 - Debe reestablecer el formulario al cancelar', () => {
        // When: Fill form and cancel
        genreCreatePage.navigate();
        genreCreatePage.fillGenreType(newGenreData.type);
        genreCreatePage.clickCancel();

        // Then: Form fields should be cleared
        genreCreatePage.verifyFormIsEmpty();
    });
});
