import { BasePage } from './BasePage';

export class GenreListPage extends BasePage {
    private selectors = {
        pageTitle: 'app-genres-list-page h2.text-primary',
        genreTable: 'table.table',
        genreRow: 'tr.genre-row',
        genreName: 'tr.genre-row td:first-child',
        genreDescription: 'tr.genre-row td:last-child',
        arrow: 'span.arrow',
        loader: 'app-loader',
    };

    navigate() {
        this.visit('/genres');
    }

    verifyPageTitle() {
        this.verifyElementContainsText(this.selectors.pageTitle, 'Listado de géneros');
    }

    getGenreCount() {
        return cy.get(this.selectors.genreRow);
    }

    clickGenreByName(name: string) {
        cy.contains('tr.genre-row', name).click();
    }

    verifyGenreVisible(name: string) {
        cy.contains('tr.genre-row', name).should('be.visible');
    }

    verifyGenreNotVisible(name: string) {
        cy.contains('tr.genre-row', name).should('not.exist');
    }

    verifyGenreDescription(genreName: string, description: string) {
        cy.contains('tr.genre-row', genreName)
            .find('td:last-child')
            .should('contain', description);
    }

    getFirstGenreName() {
        return cy
            .get(this.selectors.genreRow)
            .first()
            .find('td:first-child')
            .invoke('text')
            .then((text) => text.replace('▶', '').trim());
    }

    clickFirstGenre() {
        cy.get(this.selectors.genreRow).first().click();
    }
}
