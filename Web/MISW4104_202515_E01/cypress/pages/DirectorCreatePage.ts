import { BasePage } from './BasePage';

export class DirectorCreatePage extends BasePage {
    private selectors = {
        pageTitle: 'app-director-create-page h2',
        nameInput: 'name',
        birthDateInput: 'birthDate',
        nationalityInput: 'nationality',
        photoInput: 'photo',
        biographyInput: 'biography',
        cancelButton: 'button:contains("Cancelar")',
        submitButton: 'button[type="submit"]',
    };

    navigate() {
        this.visit('/director/create');
    }

    verifyPageTitle() {
        this.verifyElementContainsText(
            this.selectors.pageTitle,
            'Crear director',
        );
    }

    fillDirectorForm(directorData: {
        name: string;
        birthDate: string;
        nationality: string;
        photo: string;
        biography: string;
    }) {
        this.fillFormControl(this.selectors.nameInput, directorData.name);
        this.fillFormControl(
            this.selectors.birthDateInput,
            directorData.birthDate,
        );
        this.fillFormControl(
            this.selectors.nationalityInput,
            directorData.nationality,
        );
        this.fillFormControl(this.selectors.photoInput, directorData.photo);
        this.fillFormControl(
            this.selectors.biographyInput,
            directorData.biography,
        );
    }

    clickSubmit() {
        this.clickElement(this.selectors.submitButton);
    }

    clickCancel() {
        this.clickElement(this.selectors.cancelButton);
    }

    fillDirectorName(name: string) {
        this.fillFormControl(this.selectors.nameInput, name);
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
            `app-input-field[formcontrolname="${this.selectors.nameInput}"] input[type="text"]`,
        ).should('have.value', '');
    }
}
