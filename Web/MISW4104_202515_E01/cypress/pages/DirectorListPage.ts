import { BasePage } from './BasePage';

export class DirectorListPage extends BasePage {
    private selectors = {
        pageTitle: 'app-director-list-page h2.text-primary',
        searchInput: 'input[placeholder="Búsqueda"]',
        directorCard: 'app-person-card',
        directorName: 'app-person-card h5.card-title',
        directorNationality: 'app-person-card p.card-text.text-muted',
        loader: 'app-loader',
        movieToggle: 'button.btn-link',
        movieCard: 'app-movie-card',
    };

    navigate() {
        this.visit('/director');
    }

    verifyPageTitle() {
        this.verifyElementContainsText(
            this.selectors.pageTitle,
            'Directores destacados',
        );
    }

    searchDirector(name: string) {
        cy.get(this.selectors.searchInput).type(name);
    }

    getDirectorCount() {
        return cy.get(this.selectors.directorCard);
    }

    clickDirectorByName(name: string) {
        cy.contains('app-person-card h5.card-title', name).click();
    }

    verifyDirectorExists(name: string) {
        cy.contains('app-person-card h5.card-title', name).should('exist');
    }

    verifyDirectorVisible(name: string) {
        cy.contains('app-person-card h5.card-title', name).should('be.visible');
    }

    verifyDirectorNotVisible(name: string) {
        cy.contains('app-person-card h5.card-title', name).should('not.exist');
    }

    clickMoviesToggle(directorName: string) {
        cy.contains('app-person-card', directorName)
            .find('button.btn-link')
            .click();
    }

    verifyMoviesVisible(directorName: string) {
        cy.contains('app-person-card', directorName)
            .find('app-movie-card')
            .should('be.visible');
    }

    getFirstDirectorName() {
        return cy
            .get(this.selectors.directorName)
            .first()
            .invoke('text')
            .then((text) => text.trim());
    }

    searchAndVerifyFirstDirector() {
        this.getFirstDirectorName().then((directorName) => {
            this.searchDirector(directorName);
            cy.wait(500);
            this.verifyDirectorVisible(directorName);
            this.getDirectorCount().should('have.length.at.least', 1);
        });
    }

    clickFirstDirector() {
        this.getFirstDirectorName().then((directorName) => {
            this.clickDirectorByName(directorName);
        });
    }

    getFirstDirectorId() {
        return cy
            .get(this.selectors.directorName)
            .first()
            .click()
            .then(() => {
                return cy.url().then((url) => {
                    return Number(url.split('/').pop());
                });
            });
    }
}
