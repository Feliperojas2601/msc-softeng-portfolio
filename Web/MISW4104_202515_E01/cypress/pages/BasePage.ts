export class BasePage {
    protected baseUrl: string;

    constructor() {
        this.baseUrl = Cypress.config('baseUrl') || 'http://localhost:4200';
    }

    visit(path: string = '') {
        cy.visit(`${this.baseUrl}${path}`);
    }

    waitForElement(selector: string, timeout: number = 10000) {
        cy.get(selector, { timeout }).should('be.visible');
    }

    verifyElementContainsText(selector: string, text: string) {
        cy.get(selector).should('contain', text);
    }

    clickElement(selector: string) {
        cy.get(selector).click();
    }

    typeInField(selector: string, text: string) {
        cy.get(selector).clear().type(text);
    }

    fillFormControl(controlName: string, value: string) {
        cy.get(`app-input-field[formcontrolname="${controlName}"]`)
            .find('input, textarea')
            .first()
            .should('be.visible')
            .clear({ force: true })
            .type(value, { force: true });
    }

    verifyUrlContains(path: string) {
        cy.url().should('include', path);
    }

    waitForLoader() {
        cy.get('[data-testid="loader"]', { timeout: 10000 }).should(
            'not.exist',
        );
    }

    interceptApiCall(
        method: 'GET' | 'POST' | 'PUT' | 'DELETE',
        url: string,
        alias: string,
        response?: any,
    ) {
        if (response) {
            cy.intercept(method, url, response).as(alias);
        } else {
            cy.intercept(method, url).as(alias);
        }
    }

    waitForApiCall(alias: string) {
        cy.wait(`@${alias}`);
    }
}
