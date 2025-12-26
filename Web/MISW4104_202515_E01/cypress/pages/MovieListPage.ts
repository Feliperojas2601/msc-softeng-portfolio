import { BasePage } from './BasePage';

export class MovieListPage extends BasePage {
    private selectors = {
        pageTitle: 'app-movie-list-page h2.text-primary',
        searchInput: 'input[placeholder="Búsqueda"]',
        genreFilter: 'button.btn-tertiary.dropdown-toggle',
        movieCard: 'app-movie-card',
        movieTitle: 'app-movie-card h6.card-title',
        moviePoster: 'app-movie-card img.card-img-top',
        movieRating: 'app-movie-card .star',
        loader: 'app-loader',
    };

    navigate() {
        this.visit('/movie');
    }

    verifyPageTitle() {
        this.verifyElementContainsText(
            this.selectors.pageTitle,
            'Películas increíbles',
        );
    }

    searchMovie(title: string) {
        cy.get(this.selectors.searchInput).type(title);
    }

    filterByGenre(genre: string) {
        this.clickElement(this.selectors.genreFilter);
        cy.contains(genre).click();
    }

    getMovieCount() {
        return cy.get(this.selectors.movieCard);
    }

    clickMovieByTitle(title: string) {
        cy.contains('app-movie-card h6.card-title', title).click();
    }

    verifyMovieVisible(title: string) {
        cy.contains('app-movie-card h6.card-title', title).should('be.visible');
    }

    verifyMovieNotVisible(title: string) {
        cy.contains('app-movie-card h6.card-title', title).should('not.exist');
    }

    getFirstMovieTitle() {
        return cy
            .get(this.selectors.movieTitle)
            .first()
            .invoke('text')
            .then((text) => text.trim());
    }

    searchAndVerifyFirstMovie() {
        this.getFirstMovieTitle().then((movieTitle) => {
            this.searchMovie(movieTitle);
            cy.wait(500);
            this.verifyMovieVisible(movieTitle);
            this.getMovieCount().should('have.length.at.least', 1);
        });
    }

    clickFirstMovie() {
        this.getFirstMovieTitle().then((movieTitle) => {
            this.clickMovieByTitle(movieTitle);
        });
    }

    getFirstMovieId() {
        return cy
            .get(this.selectors.movieCard)
            .first()
            .click()
            .then(() => {
                return cy.url().then((url) => {
                    return Number(url.split('/').pop());
                });
            });
    }
}
