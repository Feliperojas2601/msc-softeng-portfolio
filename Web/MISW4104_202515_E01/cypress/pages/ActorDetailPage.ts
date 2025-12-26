import { BasePage } from './BasePage';

export class ActorDetailPage extends BasePage {
    private selectors = {
        actorName: 'h2.actor-name',
        actorPhoto: 'img.actor-photo',
        actorBirthDate: 'p.birth-date',
        actorNationality: '.actor-info h3',
        actorBiography: 'p.biography',
        moviesList: '.row.g-4',
        movieCard: 'app-movie-card',
        movieTitle: 'app-movie-card h6.card-title',
        moviesTitle: 'h4.movies-title',
        loader: 'app-loader',
    };

    navigate(actorId: number) {
        this.visit(`/actor/${actorId}`);
    }

    verifyActorName(name: string) {
        this.verifyElementContainsText(this.selectors.actorName, name);
    }

    verifyActorPhotoVisible() {
        cy.get(this.selectors.actorPhoto).should('be.visible');
    }

    verifyBirthDate(date: string) {
        this.verifyElementContainsText(this.selectors.actorBirthDate, date);
    }

    verifyNationality(nationality: string) {
        this.verifyElementContainsText(
            this.selectors.actorNationality,
            nationality,
        );
    }

    verifyBiography(biography: string) {
        this.verifyElementContainsText(
            this.selectors.actorBiography,
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

    navigateToFirstActorAndVerifyInfo(actorListPage: any) {
        actorListPage.getFirstActorId().then((actorId: number) => {
            cy.wait(2000);
            cy.get(this.selectors.actorName).should('be.visible');
            this.verifyActorPhotoVisible();
            cy.get(this.selectors.actorNationality).should('be.visible');
            cy.get(this.selectors.actorBiography).should('be.visible');
        });
    }

    navigateToFirstActorAndVerifyMovies(actorListPage: any) {
        actorListPage.getFirstActorId().then((actorId: number) => {
            cy.wait(2000);
            this.verifyMoviesListVisible();
        });
    }

    navigateToFirstActorAndClickFirstMovie(actorListPage: any) {
        actorListPage.getFirstActorId().then((actorId: number) => {
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
