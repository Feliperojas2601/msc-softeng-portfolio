import { BasePage } from './BasePage';

export class GenreCreatePage extends BasePage {
    private selectors = {
        pageTitle: 'app-genre-create-page h2',
        typeInput: 'type',
        descriptionInput: 'description',
        cancelButton: 'button:contains("Cancelar")',
        submitButton: 'button[type="submit"]',
    };

    navigate() {
        this.visit('/genres/create');
    }

    verifyPageTitle() {
        this.verifyElementContainsText(
            this.selectors.pageTitle,
            'Crear género',
        );
    }

    fillGenreForm(genreData: { type: string; }) {
        this.fillFormControl(this.selectors.typeInput, genreData.type);
    }

    clickSubmit() {
        this.clickElement(this.selectors.submitButton);
    }

    clickCancel() {
        this.clickElement(this.selectors.cancelButton);
    }

    fillGenreType(type: string) {
        this.fillFormControl(this.selectors.typeInput, type);
    }

    verifySubmitButtonShowsErrors() {
        cy.get(this.selectors.submitButton).click();
        cy.get('.invalid-feedback.d-block')
            .should('be.visible')
            .and('contain', 'Este campo es requerido');
        cy.get('form.ng-invalid').should('exist');
        cy.get('input.is-invalid').should('have.length.at.least', 1);
    }

    verifyFormIsEmpty() {
        cy.get(
            `app-input-field[formcontrolname="${this.selectors.typeInput}"] input[type="text"]`,
        ).should('have.value', '');
    }
}
