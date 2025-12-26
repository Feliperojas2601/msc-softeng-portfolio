import { MovieDetailPage } from '../../pages/MovieDetailPage';
import { MovieListPage } from '../../pages/MovieListPage';
import { DataGenerators } from '../../support/dataGenerators';

describe('HU16: Crear una reseña', () => {
    let movieDetailPage: MovieDetailPage;
    let movieListPage: MovieListPage;
    let reviewData: any;

    // Given
    beforeEach(() => {
        movieDetailPage = new MovieDetailPage();
        movieListPage = new MovieListPage();
        reviewData = {
            text: DataGenerators.generateReviewText(),
            score: DataGenerators.generateRating(),
            creator: DataGenerators.generatePersonName(),
        };
    });

    it('CP01_HU16 - Debe crear una reseña exitosamente con datos válidos', () => {
        // When: Navigate to first movie and create a review
        movieListPage.navigate();
        cy.wait(2000);
        movieListPage.getFirstMovieId();
        cy.wait(2000);

        movieDetailPage.verifyReviewsVisible();
        movieDetailPage.createReview(
            reviewData.text,
            reviewData.score,
            reviewData.creator
        );

        // Then: Verify the review was created successfully
        movieDetailPage.verifyReviewCreated(
            reviewData.text,
            reviewData.creator
        );
    });
});