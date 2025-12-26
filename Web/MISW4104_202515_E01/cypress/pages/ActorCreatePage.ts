import { BasePage } from './BasePage';

export class ActorCreatePage extends BasePage {
    private selectors = {
        pageTitle: 'app-actor-create-page h2',
        nameInput: 'name',
        birthDateInput: 'birthDate',
        nationalityInput: 'nationality',
        photoInput: 'photo',
        biographyInput: 'biography',
        cancelButton: 'button:contains("Cancelar")',
        submitButton: 'button[type="submit"]',
    };

    navigate() {
        this.visit('/actor/create');
    }

    verifyPageTitle() {
        this.verifyElementContainsText(this.selectors.pageTitle, 'Crear actor');
    }

    fillActorForm(actorData: {
        name: string;
        birthDate: string;
        nationality: string;
        photo: string;
        biography: string;
    }) {
        this.fillFormControl(this.selectors.nameInput, actorData.name);
        this.fillFormControl(
            this.selectors.birthDateInput,
            actorData.birthDate,
        );
        this.fillFormControl(
            this.selectors.nationalityInput,
            actorData.nationality,
        );
        this.fillFormControl(this.selectors.photoInput, actorData.photo);
        this.fillFormControl(
            this.selectors.biographyInput,
            actorData.biography,
        );
    }

    clickSubmit() {
        this.clickElement(this.selectors.submitButton);
    }

    clickCancel() {
        this.clickElement(this.selectors.cancelButton);
    }

    fillActorName(name: string) {
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
