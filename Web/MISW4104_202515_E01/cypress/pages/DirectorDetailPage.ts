import { BasePage } from './BasePage';

export class DirectorDetailPage extends BasePage {
    private selectors = {
        directorName: 'h2.director-name',
        directorPhoto: 'img.director-photo',
        directorBirthDate: 'p.birth-date',
        directorNationality: '.director-info h3',
        directorBiography: 'p.biography',
        moviesList: '.row.g-4',
        movieCard: 'app-movie-card',
        movieTitle: 'app-movie-card h6.card-title',
        moviesTitle: 'h4.movies-title',
        loader: 'app-loader',
    };

    navigate(directorId: number) {
        this.visit(`/director/${directorId}`);
    }

    verifyDirectorName(name: string) {
        this.verifyElementContainsText(this.selectors.directorName, name);
    }

    verifyDirectorPhotoVisible() {
        cy.get(this.selectors.directorPhoto).should('be.visible');
    }

    verifyBirthDate(date: string) {
        this.verifyElementContainsText(this.selectors.directorBirthDate, date);
    }

    verifyNationality(nationality: string) {
        this.verifyElementContainsText(
            this.selectors.directorNationality,
            nationality,
        );
    }

    verifyBiography(biography: string) {
        this.verifyElementContainsText(
            this.selectors.directorBiography,
            biography,
        );
    }

    verifyMoviesListVisible() {
        cy.get(this.selectors.moviesList).should('be.visible');
    }

    getMovieCount() {
        return cy.get(this.selectors.movieCard);
    }

    verifyMovieInList(movieTitle: string) {
        cy.contains(this.selectors.movieTitle, movieTitle).should('be.visible');
    }

    clickMovie(movieTitle: string) {
        cy.contains(this.selectors.movieTitle, movieTitle).click();
    }

    navigateToFirstDirectorAndVerifyInfo(directorListPage: any) {
        directorListPage.getFirstDirectorId().then((directorId: number) => {
            cy.wait(2000);
            cy.get(this.selectors.directorName).should('be.visible');
            this.verifyDirectorPhotoVisible();
            cy.get(this.selectors.directorNationality).should('be.visible');
            cy.get(this.selectors.directorBiography).should('be.visible');
        });
    }

    navigateToFirstDirectorAndVerifyMovies(directorListPage: any) {
        directorListPage.getFirstDirectorId().then((directorId: number) => {
            cy.wait(2000);
            this.verifyMoviesListVisible();
        });
    }

    navigateToFirstDirectorAndClickFirstMovie(directorListPage: any) {
        directorListPage.getFirstDirectorId().then((directorId: number) => {
            cy.wait(2000);
            cy.get('body').then(($body) => {
                if ($body.find('app-movie-card').length > 0) {
                    cy.get(this.selectors.movieTitle)
                        .first()
                        .invoke('text')
                        .then((movieTitle) => {
                            this.clickMovie(movieTitle.trim());
                        });
                } 
            });
        });
    }
}
