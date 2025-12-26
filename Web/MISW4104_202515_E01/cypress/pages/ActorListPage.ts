import { BasePage } from './BasePage';

export class ActorListPage extends BasePage {
    private selectors = {
        pageTitle: 'app-actor-list-page h2.text-primary',
        searchInput: 'input[placeholder="Búsqueda"]',
        actorCard: 'app-person-card',
        actorName: 'app-person-card h5.card-title',
        actorNationality: 'app-person-card p.card-text.text-muted',
        loader: 'app-loader',
        movieToggle: 'button.btn-link',
        movieCard: 'app-movie-card',
    };

    navigate() {
        this.visit('/actor');
    }

    verifyPageTitle() {
        this.verifyElementContainsText(
            this.selectors.pageTitle,
            'Actores destacados',
        );
    }

    searchActor(name: string) {
        cy.get(this.selectors.searchInput).type(name);
    }

    getActorCount() {
        return cy.get(this.selectors.actorCard);
    }

    clickActorByName(name: string) {
        cy.contains('app-person-card h5.card-title', name).click();
    }

    verifyActorExists(name: string) {
        cy.contains('app-person-card h5.card-title', name).should('exist');
    }

    verifyActorVisible(name: string) {
        cy.contains('app-person-card h5.card-title', name).should('be.visible');
    }

    verifyActorNotVisible(name: string) {
        cy.contains('app-person-card h5.card-title', name).should('not.exist');
    }

    clickMoviesToggle(actorName: string) {
        cy.contains('app-person-card', actorName)
            .find('button.btn-link')
            .click();
    }

    verifyMoviesVisible(actorName: string) {
        cy.contains('app-person-card', actorName)
            .find('app-movie-card')
            .should('be.visible');
    }

    getFirstActorName() {
        return cy
            .get(this.selectors.actorName)
            .first()
            .invoke('text')
            .then((text) => text.trim());
    }

    searchAndVerifyFirstActor() {
        this.getFirstActorName().then((actorName) => {
            this.searchActor(actorName);
            cy.wait(500);
            this.verifyActorVisible(actorName);
            this.getActorCount().should('have.length.at.least', 1);
        });
    }

    clickFirstActor() {
        this.getFirstActorName().then((actorName) => {
            this.clickActorByName(actorName);
        });
    }

    getFirstActorId() {
        return cy
            .get(this.selectors.actorName)
            .first()
            .click()
            .then(() => {
                return cy.url().then((url) => {
                    return Number(url.split('/').pop());
                });
            });
    }
}
