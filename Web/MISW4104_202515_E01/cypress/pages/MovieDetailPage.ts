import { BasePage } from './BasePage';

export class MovieDetailPage extends BasePage {
    private selectors = {
        movieTitle: 'h3.movie-title',
        moviePoster: '.movie-poster-container img.img-fluid',
        movieCountry: '.info-item strong',
        movieReleaseDate: '.info-item',
        movieDuration: '.info-item',
        movieRating: '.rating-container .star',
        moviePlatform: '.platforms-badge .badge',
        movieTrailer: 'a.btn-link',
        directorSection: '.director-section',
        directorName: '.director-section h6.person-name',
        directorPhoto: '.director-section .person-photo img',
        actorsSection: '.actors-section',
        actorCard: '.actors-section .d-flex.align-items-center',
        actorName: '.actors-section h6.person-name',
        actorPhoto: '.actors-section .person-photo img',
        reviewsSection: '.reviews-section',
        reviewCard: '.review-card',
        reviewText: '.review-text',
        reviewCreator: '.text-muted.fst-italic',
        reviewStars: '.review-stars',
        addReviewButton: '.new-review-section button.btn-primary',
        reviewFormContainer: '.review-form-container',
        reviewTextInput: 'app-input-field[formcontrolname="text"] textarea',
        reviewScoreInput: 'app-input-field[formcontrolname="score"] input',
        reviewCreatorInput: 'app-input-field[formcontrolname="creator"] input',
        submitReviewButton: 'form button[type="submit"]',
        cancelReviewButton: 'form button[type="button"]',
        loader: 'app-loader',
    };

    navigate(movieId: number) {
        this.visit(`/movie/${movieId}`);
    }

    verifyMovieTitle(title: string) {
        this.verifyElementContainsText(this.selectors.movieTitle, title);
    }

    verifyMoviePosterVisible() {
        cy.get(this.selectors.moviePoster).should('be.visible');
    }

    verifyCountry(country: string) {
        this.verifyElementContainsText(this.selectors.movieCountry, country);
    }

    verifyReleaseDate(date: string) {
        this.verifyElementContainsText(this.selectors.movieReleaseDate, date);
    }

    verifyDuration(duration: string) {
        this.verifyElementContainsText(this.selectors.movieDuration, duration);
    }

    verifyDirector(name: string) {
        this.verifyElementContainsText(this.selectors.directorName, name);
    }

    clickDirector() {
        cy.get(this.selectors.directorName).click();
    }

    verifyActorsVisible() {
        cy.get(this.selectors.actorsSection).should('be.visible');
    }

    getActorCount() {
        return cy.get(this.selectors.actorCard);
    }

    clickActor(name: string) {
        cy.contains(this.selectors.actorName, name).click();
    }

    verifyReviewsVisible() {
        cy.get(this.selectors.reviewsSection).should('be.visible');
    }

    getReviewCount() {
        return cy.get(this.selectors.reviewCard);
    }

    getFirstMovieId() {
        return cy
            .get('app-movie-card')
            .first()
            .click()
            .then(() => {
                return cy.url().then((url) => {
                    return Number(url.split('/').pop());
                });
            });
    }

    navigateToFirstMovieAndVerifyInfo(movieListPage: any) {
        movieListPage.getFirstMovieId().then((movieId: number) => {
            cy.wait(2000);
            cy.get(this.selectors.movieTitle).should('be.visible');
            this.verifyMoviePosterVisible();
            cy.get(this.selectors.movieCountry).should('be.visible');
            cy.get(this.selectors.movieDuration).should('be.visible');
        });
    }

    navigateToFirstMovieAndVerifyDirector(movieListPage: any) {
        movieListPage.getFirstMovieId().then((movieId: number) => {
            cy.wait(2000);
            cy.get(this.selectors.directorSection).should('be.visible');
        });
    }

    navigateToFirstMovieAndVerifyActors(movieListPage: any) {
        movieListPage.getFirstMovieId().then((movieId: number) => {
            cy.wait(2000);
            this.verifyActorsVisible();
        });
    }

    clickAddReviewButton() {
        cy.get(this.selectors.addReviewButton).click();
    }

    verifyReviewFormVisible() {
        cy.get(this.selectors.reviewFormContainer).should('be.visible');
    }

    fillReviewText(text: string) {
        cy.get(this.selectors.reviewTextInput).clear().type(text);
    }

    fillReviewScore(score: number) {
        cy.get(this.selectors.reviewScoreInput).clear().type(score.toString());
    }

    fillReviewCreator(creator: string) {
        cy.get(this.selectors.reviewCreatorInput).clear().type(creator);
    }

    submitReview() {
        cy.get(this.selectors.submitReviewButton).click();
    }

    verifyReviewCreated(text: string, creator: string) {
        // Wait for form to close and review to be added
        cy.get(this.selectors.reviewFormContainer).should('not.exist');
        
        // Verify the review exists in the reviews section
        cy.get(this.selectors.reviewsSection).within(() => {
            cy.contains(this.selectors.reviewText, text).should('be.visible');
            cy.contains('.text-muted.fst-italic', creator).should('be.visible');
        });
    }

    createReview(text: string, score: number, creator: string) {
        this.clickAddReviewButton();
        this.verifyReviewFormVisible();
        this.fillReviewText(text);
        this.fillReviewScore(score);
        this.fillReviewCreator(creator);
        this.submitReview();
        cy.wait(2000);
        this.verifyReviewCreated(text, creator);
    }
}
